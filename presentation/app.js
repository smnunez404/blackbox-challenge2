const evidenceUrl = "/data/evidence.json";
const listEl = document.querySelector("#evidence-list");
const detailEl = document.querySelector("#evidence-detail");
const countEl = document.querySelector("#evidence-count");
const searchEl = document.querySelector("#evidence-search");
const filterEl = document.querySelector("#command-filter");
let evidence = [];
let selectedId = null;

function esc(value) {
  return String(value).replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[ch]));
}

function renderDetail(item) {
  if (!item) return;
  selectedId = item.id;
  detailEl.innerHTML = `<p class="eyebrow">${esc(item.version)} · ${esc(item.id)}</p>
    <h3>${esc(item.command)} <span class="status-code ${item.status >= 400 ? "bad" : ""}">Código HTTP ${esc(item.status)}</span></h3>
    <p>${esc(item.note)}</p>
    <p class="detail-meta">${esc(item.compare || "Evidencia del corpus público")}</p>
    <div class="code-panels">
      <div class="code-panel"><span>Solicitud · POST /msg</span><pre>${esc(JSON.stringify(item.request, null, 2))}</pre></div>
      <div class="code-panel"><span>Respuesta · datos recibidos</span><pre>${esc(JSON.stringify(item.response, null, 2))}</pre></div>
    </div>`;
  renderList();
}

function renderList() {
  const q = searchEl.value.trim().toLowerCase();
  const command = filterEl.value;
  const filtered = evidence.filter(item => {
    const haystack = `${item.id} ${item.version} ${item.command} ${JSON.stringify(item.request)} ${JSON.stringify(item.response)} ${item.note}`.toLowerCase();
    return (!q || haystack.includes(q)) && (!command || item.command === command);
  });
  countEl.textContent = `${filtered.length} de ${evidence.length} ejemplos encontrados`;
  if (!filtered.length) {
    listEl.innerHTML = `<p class="evidence-footnote">No hay coincidencias. Prueba otro comando o código.</p>`;
    return;
  }
  listEl.innerHTML = filtered.map(item => {
    const msg = item.request?.m || "";
    const brief = msg.replace(/;\d+$/, "").replaceAll(";", " · ");
    return `<button class="evidence-item ${item.id === selectedId ? "selected" : ""}" type="button" data-id="${esc(item.id)}">
      <span class="evidence-id">${esc(item.id)}</span><span><span class="evidence-summary">${esc(brief)}</span><br><span class="evidence-command">${esc(item.version)}</span></span>
      <span class="status-code ${item.status >= 400 ? "bad" : ""}">${esc(item.status)}</span></button>`;
  }).join("");
  listEl.querySelectorAll("[data-id]").forEach(button => button.addEventListener("click", () => {
    const item = evidence.find(row => String(row.id) === button.dataset.id);
    renderDetail(item);
  }));
}

fetch(evidenceUrl, { credentials: "omit", cache: "force-cache" })
  .then(response => { if (!response.ok) throw new Error("evidencia no disponible"); return response.json(); })
  .then(rows => { evidence = rows; renderList(); renderDetail(rows[0]); })
  .catch(() => { countEl.textContent = "No se pudo cargar la muestra"; listEl.textContent = "Recarga la página para intentar abrir el archivo estático de evidencia."; });

searchEl.addEventListener("input", renderList);
filterEl.addEventListener("change", renderList);
