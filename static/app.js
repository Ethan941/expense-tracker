let currentFile = null;

// ── Drag & Drop ───────────────────────────────────────────────────────────

function handleDragOver(e) {
  e.preventDefault();
  document.getElementById("drop-area").classList.add("drag-over");
}

function handleDragLeave() {
  document.getElementById("drop-area").classList.remove("drag-over");
}

function handleDrop(e) {
  e.preventDefault();
  document.getElementById("drop-area").classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) loadFile(file);
}

// ── Sélection fichier ─────────────────────────────────────────────────────

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) loadFile(file);
}

function loadFile(file) {
  const allowed = ["image/jpeg", "image/png", "image/webp"];
  if (!allowed.includes(file.type)) {
    alert("Type non supporté. Utilisez JPEG, PNG ou WebP.");
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    alert("Fichier trop volumineux (max 10 Mo).");
    return;
  }

  currentFile = file;

  const reader = new FileReader();
  reader.onload = (ev) => {
    document.getElementById("preview-img").src = ev.target.result;
    document.getElementById("preview-name").textContent = file.name;
    document.getElementById("drop-area").classList.add("hidden");
    document.getElementById("preview-zone").classList.remove("hidden");
    document.getElementById("result-zone").innerHTML = "";
  };
  reader.readAsDataURL(file);
}

// ── Envoi vers /api/analyze ───────────────────────────────────────────────

function submitImage() {
  if (!currentFile) return;

  const btn = document.getElementById("analyze-btn");
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner" style="width:18px;height:18px;border-width:2px"></span> Analyse en cours…';

  const formData = new FormData();
  formData.append("file", currentFile);

  fetch("/api/analyze", { method: "POST", body: formData })
    .then((res) => {
      if (!res.ok) return res.text().then((t) => Promise.reject(t));
      return res.text();
    })
    .then((html) => {
      document.getElementById("result-zone").innerHTML = html;
      document.getElementById("result-zone").scrollIntoView({ behavior: "smooth" });
      // Attache le handler après injection du formulaire dans le DOM
      const form = document.getElementById("expense-form");
      if (form) form.addEventListener("submit", submitExpenseForm);
    })
    .catch((errHtml) => {
      document.getElementById("result-zone").innerHTML =
        errHtml || '<div class="card confirmation error"><div class="icon">✗</div><h3>Erreur réseau</h3></div>';
    })
    .finally(() => {
      btn.disabled = false;
      btn.innerHTML = "Analyser avec l'IA";
    });
}

// ── Reset ─────────────────────────────────────────────────────────────────

function resetApp() {
  currentFile = null;
  document.getElementById("file-input").value = "";
  document.getElementById("preview-img").src = "";
  document.getElementById("preview-name").textContent = "";
  document.getElementById("drop-area").classList.remove("hidden");
  document.getElementById("preview-zone").classList.add("hidden");
  document.getElementById("result-zone").innerHTML = "";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ── Soumission du formulaire vers /api/submit ─────────────────────────────

function submitExpenseForm(event) {
  event.preventDefault();

  const form = document.getElementById("expense-form");
  const btn = document.getElementById("submit-btn");

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner" style="width:18px;height:18px;border-width:2px"></span> Envoi en cours…';

  const formData = new FormData(form);

  // Ajoute le fichier image original si disponible
  if (currentFile) {
    formData.append("image_file", currentFile, currentFile.name);
  }

  fetch("/api/submit", { method: "POST", body: formData })
    .then((res) => res.text())
    .then((html) => {
      document.getElementById("result-zone").innerHTML = html;
      document.getElementById("result-zone").scrollIntoView({ behavior: "smooth" });
    })
    .catch(() => {
      document.getElementById("result-zone").innerHTML =
        '<div class="card confirmation error"><div class="icon">✗</div><h3>Erreur réseau</h3></div>';
    })
    .finally(() => {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = "&#8679; Envoyer vers Google Sheets";
      }
    });
}
