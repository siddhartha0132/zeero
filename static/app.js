const $ = (selector) => document.querySelector(selector);

const DOC_TYPE_LABELS = {
  policy: "Policy wording",
  hospital_bill: "Hospital bill",
  discharge_summary: "Discharge summary",
  rejection_letter: "Rejection letter",
  other: "Other",
};

const TOOL_LABELS = {
  update_plan: "Updating the plan",
  list_documents: "Checking the case file",
  read_document: "Reading a document",
  search_documents: "Searching the documents",
  lookup_regulation: "Looking up IRDAI rules",
  calculate_policy_tenure: "Calculating cover period and waiting periods",
  calculate_room_rent_deduction: "Calculating the room-rent deduction",
  record_bill_assessment: "Checking every bill item",
  check_required_documents: "Building the document checklist",
  save_draft: "Writing a document",
  record_verdict: "Recording the verdict",
};

const OUTCOMES = {
  claim_likely_payable: { label: "Claim looks payable", tone: "good" },
  partially_payable: { label: "Partly payable", tone: "warn" },
  rejection_contestable: { label: "Rejection can be challenged", tone: "good" },
  rejection_likely_valid: { label: "Rejection looks valid", tone: "bad" },
  needs_more_information: { label: "Needs more information", tone: "warn" },
};

const BILL_STATUS_LABELS = {
  payable: "Payable",
  partially_payable: "Partly payable",
  not_payable: "Not payable",
  needs_review: "Needs review",
};

const CHECKLIST_STATUS = {
  uploaded: { icon: "✅", note: "uploaded" },
  keep_ready: { icon: "📎", note: "keep ready" },
  to_obtain: { icon: "⚠️", note: "get this" },
};

const inr = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

let caseId = null;
let llmReady = false;
let running = false;
let activeDraftId = null;
let latestDrafts = [];
const toolEvents = new Map();

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderMarkdown(text) {
  const inline = (line) =>
    line
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[\s(])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>");
  let html = "";
  let list = null;
  const closeList = () => {
    if (list) html += `</${list}>`;
    list = null;
  };
  for (const line of escapeHtml(text).split("\n")) {
    const heading = line.match(/^#{1,4}\s+(.*)$/);
    const bullet = line.match(/^\s*[-*•]\s+(.*)$/);
    const numbered = line.match(/^\s*\d+[.)]\s+(.*)$/);
    if (heading) {
      closeList();
      html += `<h4>${inline(heading[1])}</h4>`;
    } else if (bullet || numbered) {
      const tag = bullet ? "ul" : "ol";
      if (list !== tag) {
        closeList();
        html += `<${tag}>`;
        list = tag;
      }
      html += `<li>${inline((bullet || numbered)[1])}</li>`;
    } else if (!line.trim()) {
      closeList();
    } else {
      closeList();
      html += `<p>${inline(line)}</p>`;
    }
  }
  closeList();
  return html;
}

async function api(path, options = {}) {
  const response = await fetch(path, options);
  if (!response.ok) {
    let detail = response.statusText;
    try {
      detail = (await response.json()).detail || detail;
    } catch {
      /* body was not JSON */
    }
    throw new Error(detail);
  }
  return response.json();
}

function jsonRequest(method, body) {
  return { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
}

// ---------- rendering ----------

function renderCase(state) {
  renderDocuments(state.documents);
  renderPlan(state.plan);
  renderVerdict(state.verdict);
  renderAssessment(state.bill_assessment);
  renderChecklist(state.checklist);
  renderDrafts(state.drafts);
  const hasResults = state.verdict || state.bill_assessment || state.checklist || state.drafts.length;
  $("#results-empty").hidden = Boolean(hasResults);
}

function renderDocuments(documents) {
  const list = $("#doc-list");
  list.innerHTML = documents
    .map(
      (doc) => `
      <li data-id="${escapeHtml(doc.id)}">
        <span class="doc-name">${escapeHtml(doc.filename)}</span>
        <button class="icon-button" data-action="remove" type="button" aria-label="Remove ${escapeHtml(doc.filename)}">×</button>
        <select data-action="type" aria-label="Document type">
          ${Object.entries(DOC_TYPE_LABELS)
            .map(([value, label]) => `<option value="${value}" ${value === doc.doc_type ? "selected" : ""}>${label}</option>`)
            .join("")}
        </select>
      </li>`,
    )
    .join("");
}

function renderPlan(plan) {
  const element = $("#plan");
  element.hidden = !plan.length;
  element.innerHTML = plan.map((step) => `<li class="${escapeHtml(step.status)}">${escapeHtml(step.title)}</li>`).join("");
}

function renderVerdict(verdict) {
  const element = $("#verdict");
  if (!verdict) {
    element.innerHTML = "";
    return;
  }
  const outcome = OUTCOMES[verdict.outcome] || { label: verdict.outcome, tone: "warn" };
  const money = [];
  if (verdict.claimed_amount != null) {
    money.push(`<div><span>Claimed</span><strong>${inr.format(verdict.claimed_amount)}</strong></div>`);
  }
  if (verdict.estimated_payable_amount != null) {
    money.push(
      `<div class="highlight"><span>Should be paid</span><strong>${inr.format(verdict.estimated_payable_amount)}</strong></div>`,
    );
  }
  const findings = verdict.key_findings
    .map(
      (item) => `<li>${escapeHtml(item.finding)}<br>
        ${item.clause_ref ? `<span class="ref">${escapeHtml(item.clause_ref)}</span>` : ""}
        ${item.impact ? `<span class="impact">${escapeHtml(item.impact)}</span>` : ""}</li>`,
    )
    .join("");
  const steps = verdict.next_steps
    .map(
      (item) => `<li>${escapeHtml(item.action)}
        ${item.deadline ? ` <span class="deadline">· ${escapeHtml(item.deadline)}</span>` : ""}
        ${item.who ? ` <span class="muted">(${escapeHtml(item.who)})</span>` : ""}</li>`,
    )
    .join("");
  element.innerHTML = `
    <article class="card verdict ${outcome.tone}">
      <span class="badge">${escapeHtml(outcome.label)}</span>
      <h3>${escapeHtml(verdict.headline)}</h3>
      ${money.length ? `<div class="money">${money.join("")}</div>` : ""}
      ${findings ? `<h4>Key findings</h4><ul class="findings">${findings}</ul>` : ""}
      ${steps ? `<h4>What to do next</h4><ol class="steps">${steps}</ol>` : ""}
      <p class="confidence">Agent confidence: ${escapeHtml(verdict.confidence)}</p>
    </article>`;
}

function renderAssessment(assessment) {
  const element = $("#assessment");
  if (!assessment) {
    element.innerHTML = "";
    return;
  }
  const rows = assessment.items
    .map(
      (item) => `
      <tr>
        <td>${escapeHtml(item.description)}<br><span class="chip ${escapeHtml(item.status)}">${BILL_STATUS_LABELS[item.status] || escapeHtml(item.status)}</span></td>
        <td class="num">${inr.format(item.billed)}</td>
        <td class="num">${inr.format(item.payable)}</td>
        <td class="reason">${escapeHtml(item.reason)}${item.clause_ref ? `<br><span class="ref">${escapeHtml(item.clause_ref)}</span>` : ""}</td>
      </tr>`,
    )
    .join("");
  element.innerHTML = `
    <article class="card">
      <h3>Bill check</h3>
      ${assessment.warning ? `<p class="event error">${escapeHtml(assessment.warning)}</p>` : ""}
      <div class="table-wrap">
        <table>
          <thead><tr><th>Item</th><th class="num">Billed</th><th class="num">Payable</th><th>Why</th></tr></thead>
          <tbody>${rows}</tbody>
          <tfoot><tr>
            <th>Total</th>
            <th class="num">${inr.format(assessment.billed_total)}</th>
            <th class="num">${inr.format(assessment.payable_total)}</th>
            <th class="reason">${inr.format(assessment.deduction_total)} deducted</th>
          </tr></tfoot>
        </table>
      </div>
    </article>`;
}

function renderChecklist(checklist) {
  const element = $("#checklist");
  if (!checklist) {
    element.innerHTML = "";
    return;
  }
  const items = checklist
    .map((item) => {
      const status = CHECKLIST_STATUS[item.status] || { icon: "•", note: item.status };
      return `<li><span class="status" aria-hidden="true">${status.icon}</span><span>${escapeHtml(item.item)} <small>(${status.note})</small></span></li>`;
    })
    .join("");
  element.innerHTML = `<article class="card"><h3>Documents to submit</h3><ul class="checklist">${items}</ul></article>`;
}

function renderDrafts(drafts) {
  latestDrafts = drafts;
  const element = $("#drafts");
  if (!drafts.length) {
    element.innerHTML = "";
    activeDraftId = null;
    return;
  }
  if (!drafts.some((draft) => draft.id === activeDraftId)) activeDraftId = drafts[drafts.length - 1].id;
  const draft = drafts.find((item) => item.id === activeDraftId);
  const tabs = drafts
    .map(
      (item) =>
        `<button type="button" data-draft="${escapeHtml(item.id)}" class="${item.id === activeDraftId ? "active" : ""}">${escapeHtml(item.title)}</button>`,
    )
    .join("");
  const recipient = draft.recipient.includes("@") ? draft.recipient.trim() : "";
  const mailto = recipient
    ? `mailto:${encodeURIComponent(recipient)}?subject=${encodeURIComponent(draft.title)}&body=${encodeURIComponent(draft.body)}`
    : "";
  element.innerHTML = `
    <article class="card">
      <h3>Ready-to-send documents</h3>
      <div class="tabs">${tabs}</div>
      ${draft.recipient ? `<p class="draft-meta">To: ${escapeHtml(draft.recipient)}</p>` : ""}
      <pre class="draft-body">${escapeHtml(draft.body)}</pre>
      <div class="draft-actions">
        <button type="button" class="primary" data-draft-action="copy">Copy</button>
        <button type="button" class="ghost" data-draft-action="download">Download .txt</button>
        ${mailto ? `<a class="ghost button-link" href="${escapeHtml(mailto)}">Open in email app</a>` : ""}
      </div>
      <p class="muted small">Nothing is sent automatically. Review the text, then send it yourself.</p>
    </article>`;
}

// ---------- activity feed ----------

function clearEmptyState() {
  $("#feed .empty")?.remove();
}

function scrollFeed() {
  const panel = $("#activity-panel");
  panel.scrollTop = panel.scrollHeight;
}

function appendToFeed(element) {
  clearEmptyState();
  const thinking = $("#feed .thinking");
  $("#feed").insertBefore(element, thinking);
  scrollFeed();
}

function setThinking(text) {
  let element = $("#feed .thinking");
  if (!text) {
    element?.remove();
    return;
  }
  if (!element) {
    element = document.createElement("div");
    element.className = "event thinking";
    clearEmptyState();
    $("#feed").appendChild(element);
  }
  element.textContent = text;
  scrollFeed();
}

function addMessage(role, text) {
  const element = document.createElement("div");
  element.className = `message ${role}`;
  element.innerHTML = role === "agent" ? renderMarkdown(text) : escapeHtml(text);
  appendToFeed(element);
}

function addError(message) {
  const element = document.createElement("div");
  element.className = "event error";
  element.textContent = message;
  appendToFeed(element);
}

function describeArgs(name, args) {
  if (name === "read_document") return args.doc_id;
  if (name === "search_documents") return `“${args.query}”`;
  if (name === "lookup_regulation") return args.topic?.replaceAll("_", " ");
  if (name === "save_draft") return args.title;
  return "";
}

function addToolCall(event) {
  const element = document.createElement("details");
  element.className = "event tool";
  element.innerHTML = `
    <summary><span class="label">${escapeHtml(TOOL_LABELS[event.name] || event.name)}</span>
      <span class="detail">${escapeHtml(describeArgs(event.name, event.args) || "")}</span></summary>
    <pre>${escapeHtml(JSON.stringify(event.args, null, 2))}</pre>`;
  toolEvents.set(event.id, element);
  appendToFeed(element);
}

function completeToolCall(event) {
  const element = toolEvents.get(event.id);
  if (!element) return;
  element.classList.add(event.ok ? "ok" : "failed");
  element.querySelector(".detail").textContent = `${event.ok ? "✓" : "✗"} ${event.summary}`;
}

function handleEvent(event) {
  switch (event.type) {
    case "status":
      setThinking(event.text);
      break;
    case "assistant":
      addMessage("agent", event.text);
      break;
    case "tool_call":
      setThinking("Working…");
      addToolCall(event);
      break;
    case "tool_result":
      completeToolCall(event);
      break;
    case "state":
    case "done":
      renderCase(event.case);
      break;
    case "error":
      addError(event.message);
      if (event.case) renderCase(event.case);
      break;
  }
}

// ---------- actions ----------

function setRunning(value) {
  running = value;
  $("#run").disabled = value;
  $("#chat button").disabled = value;
  $("#run").textContent = value ? "Agent is working…" : "Run the agent";
  if (!value) setThinking(null);
}

async function runAgent(body) {
  setRunning(true);
  try {
    const response = await fetch(`/api/cases/${caseId}/run`, jsonRequest("POST", body));
    if (!response.ok) {
      let detail = response.statusText;
      try {
        detail = (await response.json()).detail || detail;
      } catch {
        /* body was not JSON */
      }
      throw new Error(detail);
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      let boundary;
      while ((boundary = buffer.indexOf("\n\n")) >= 0) {
        const chunk = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 2);
        const data = chunk
          .split("\n")
          .filter((line) => line.startsWith("data: "))
          .map((line) => line.slice(6))
          .join("\n");
        if (data) handleEvent(JSON.parse(data));
      }
    }
  } catch (error) {
    addError(error.message);
  } finally {
    setRunning(false);
  }
}

async function newCase() {
  showCase(await api("/api/cases", { method: "POST" }));
}

// The case id lives in the URL so a refresh mid-demo keeps the documents and results.
function showCase(state) {
  caseId = state.id;
  history.replaceState(null, "", `?case=${encodeURIComponent(caseId)}`);
  toolEvents.clear();
  activeDraftId = null;
  $("#feed").innerHTML = '<p class="empty">Add documents and run the agent. Every step it takes shows up here.</p>';
  $("#upload-status").hidden = true;
  renderCase(state);
}

async function uploadFiles(fileList) {
  const files = [...fileList];
  if (!files.length) return;
  const status = $("#upload-status");
  status.hidden = false;
  status.textContent = `Reading ${files.length} file${files.length > 1 ? "s" : ""}…`;
  const form = new FormData();
  files.forEach((file) => form.append("files", file));
  try {
    const result = await api(`/api/cases/${caseId}/documents`, { method: "POST", body: form });
    renderCase(result.case);
    status.textContent = result.errors.length ? result.errors.join(" ") : `Added ${result.added.length} document(s).`;
  } catch (error) {
    status.textContent = error.message;
  }
}

async function copyDraft(draft) {
  try {
    await navigator.clipboard.writeText(draft.body);
    return true;
  } catch {
    return false;
  }
}

function downloadDraft(draft) {
  const blob = new Blob([draft.body], { type: "text/plain;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${draft.title.replace(/[^\w\- ]+/g, "").trim() || "draft"}.txt`;
  link.click();
  URL.revokeObjectURL(link.href);
}

// ---------- wiring ----------

$("#file-input").addEventListener("change", (event) => {
  uploadFiles(event.target.files);
  event.target.value = "";
});

const dropzone = $("#dropzone");
["dragenter", "dragover"].forEach((type) =>
  dropzone.addEventListener(type, (event) => {
    event.preventDefault();
    dropzone.classList.add("dragging");
  }),
);
["dragleave", "drop"].forEach((type) => dropzone.addEventListener(type, () => dropzone.classList.remove("dragging")));
dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  uploadFiles(event.dataTransfer.files);
});

$("#load-sample").addEventListener("click", async () => {
  renderCase(await api(`/api/cases/${caseId}/sample`, { method: "POST" }));
});

$("#doc-list").addEventListener("click", async (event) => {
  if (event.target.dataset.action !== "remove") return;
  const docId = event.target.closest("li").dataset.id;
  renderCase(await api(`/api/cases/${caseId}/documents/${docId}`, { method: "DELETE" }));
});

$("#doc-list").addEventListener("change", async (event) => {
  if (event.target.dataset.action !== "type") return;
  const docId = event.target.closest("li").dataset.id;
  renderCase(await api(`/api/cases/${caseId}/documents/${docId}`, jsonRequest("PATCH", { doc_type: event.target.value })));
});

$("#run").addEventListener("click", () => {
  if (running) return;
  if (!llmReady) {
    addError("No AI model is configured. Add an API key to .env and restart the server.");
    return;
  }
  const mode = document.querySelector('input[name="mode"]:checked').value;
  $("#feed").innerHTML = "";
  toolEvents.clear();
  runAgent({ mode, message: $("#notes").value });
});

$("#chat").addEventListener("submit", (event) => {
  event.preventDefault();
  const input = $("#chat-input");
  const message = input.value.trim();
  if (!message || running) return;
  input.value = "";
  addMessage("user", message);
  runAgent({ message });
});

$("#drafts").addEventListener("click", async (event) => {
  const tab = event.target.closest("[data-draft]");
  if (tab) {
    activeDraftId = tab.dataset.draft;
    renderDrafts(latestDrafts);
    return;
  }
  const action = event.target.dataset.draftAction;
  const draft = latestDrafts.find((item) => item.id === activeDraftId);
  if (!action || !draft) return;
  if (action === "copy") {
    event.target.textContent = (await copyDraft(draft)) ? "Copied ✓" : "Copy failed";
    setTimeout(() => (event.target.textContent = "Copy"), 1500);
  } else if (action === "download") {
    downloadDraft(draft);
  }
});

$("#new-case").addEventListener("click", () => {
  if (!running) newCase();
});

async function init() {
  try {
    const health = await api("/api/health");
    llmReady = health.llm_ready;
    const pill = $("#model-status");
    pill.textContent = llmReady ? `Model: ${health.model}` : "No AI model configured";
    pill.className = `pill ${llmReady ? "ok" : "off"}`;
    $("#config-banner").hidden = llmReady;
    const savedId = new URLSearchParams(location.search).get("case");
    const saved = savedId ? await api(`/api/cases/${encodeURIComponent(savedId)}`).catch(() => null) : null;
    if (saved) showCase(saved);
    else await newCase();
  } catch (error) {
    addError(`Could not reach the server: ${error.message}`);
  }
}

init();
