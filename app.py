import os
import base64
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from backend import ExpenseAgent
from sheets import GoogleSheetsClient

load_dotenv()

app = FastAPI(title="Expense Tracker")
app.mount("/static", StaticFiles(directory="static"), name="static")

ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 Mo

agent = ExpenseAgent()
sheets_client = GoogleSheetsClient()


@app.get("/", response_class=HTMLResponse)
async def index():
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME:
        return HTMLResponse(
            content=_error_html(
                f"Type non supporté : {file.content_type}. Utilisez JPEG, PNG ou WebP."
            ),
            status_code=400,
        )

    image_bytes = await file.read()

    if len(image_bytes) > MAX_SIZE_BYTES:
        return HTMLResponse(
            content=_error_html("Fichier trop volumineux (max 10 Mo)."),
            status_code=400,
        )

    data = agent.extract_from_bytes(image_bytes, file.content_type)
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    image_data_uri = f"data:{file.content_type};base64,{image_b64}"

    return HTMLResponse(content=_form_html(data, image_data_uri, file.content_type))


@app.post("/api/submit", response_class=HTMLResponse)
async def submit(
    type_document: str = Form(""),
    fournisseur: str = Form(""),
    date: str = Form(""),
    montant_ttc: str = Form(""),
    tva: str = Form(""),
    devise: str = Form("EUR"),
    description: str = Form(""),
    confiance: str = Form(""),
    image_file: UploadFile = File(None),
):
    def to_float(val: str):
        try:
            return float(val.replace(",", ".")) if val.strip() else None
        except ValueError:
            return None

    data = {
        "type_document": type_document or None,
        "fournisseur": fournisseur or None,
        "date": date or None,
        "montant_ttc": to_float(montant_ttc),
        "tva": to_float(tva),
        "devise": devise or "EUR",
        "description": description or None,
        "confiance": confiance or None,
    }

    image_url = None
    if image_file and image_file.filename:
        try:
            image_bytes = await image_file.read()
            date_safe = (data.get("date") or "unknown").replace("/", "-")
            image_url = sheets_client.upload_image_to_drive(
                image_bytes,
                image_file.content_type or "image/jpeg",
                f"note_frais_{date_safe}_{data.get('fournisseur') or 'inconnu'}",
            )
        except Exception:
            pass  # L'upload échoue silencieusement, la ligne est quand même ajoutée

    sheets_client.append_expense(data, image_url)
    return HTMLResponse(content=_success_html(data, image_url))


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return HTMLResponse(
        content=_error_html(f"Erreur serveur : {exc}"),
        status_code=500,
    )


# ── Fragments HTML ────────────────────────────────────────────────────────────

def _form_html(data: dict, image_data_uri: str, media_type: str) -> str:
    confiance = data.get("confiance") or ""
    badge_cls = {"haute": "badge-success", "moyen": "badge-warning", "basse": "badge-danger"}.get(
        confiance, "badge-secondary"
    )

    def opt(values, selected):
        return "\n".join(
            f'<option value="{v}" {"selected" if v == selected else ""}>{v.capitalize()}</option>'
            for v in values
        )

    montant_str = str(data.get("montant_ttc")) if data.get("montant_ttc") is not None else ""
    tva_str = str(data.get("tva")) if data.get("tva") is not None else ""

    return f"""
<div class="card result-card">
  <div class="card-header">
    <h3>Données extraites</h3>
    <span class="badge {badge_cls}">Confiance : {confiance}</span>
  </div>
  <form id="expense-form" method="post" action="/api/submit">

    <div class="form-grid">
      <div class="form-group">
        <label>Type de document</label>
        <select name="type_document">
          {opt(["restaurant", "transport", "hôtel", "autre"], data.get("type_document"))}
        </select>
      </div>
      <div class="form-group">
        <label>Fournisseur</label>
        <input type="text" name="fournisseur" value="{data.get('fournisseur') or ''}">
      </div>
      <div class="form-group">
        <label>Date</label>
        <input type="text" name="date" value="{data.get('date') or ''}" placeholder="JJ/MM/AAAA">
      </div>
      <div class="form-group">
        <label>Montant TTC (€)</label>
        <input type="number" name="montant_ttc" value="{montant_str}" step="0.01" min="0">
      </div>
      <div class="form-group">
        <label>TVA (€)</label>
        <input type="number" name="tva" value="{tva_str}" step="0.01" min="0">
      </div>
      <div class="form-group">
        <label>Devise</label>
        <input type="text" name="devise" value="{data.get('devise') or 'EUR'}">
      </div>
      <div class="form-group full-width">
        <label>Description</label>
        <input type="text" name="description" value="{data.get('description') or ''}">
      </div>
      <div class="form-group">
        <label>Confiance</label>
        <select name="confiance">
          {opt(["haute", "moyen", "basse"], confiance)}
        </select>
      </div>
    </div>

    <div class="form-actions">
      <button type="submit" id="submit-btn" class="btn btn-primary">
        &#8679; Envoyer vers Google Sheets
      </button>
    </div>
  </form>
</div>
"""


def _success_html(data: dict, image_url: str = None) -> str:
    montant = data.get("montant_ttc")
    montant_str = f"{montant:.2f} €" if montant is not None else "—"
    image_link = f'<a href="{image_url}" target="_blank" class="link">Voir l\'image</a>' if image_url else "Non uploadée"

    return f"""
<div class="card confirmation success">
  <div class="icon">&#10003;</div>
  <h3>Note de frais enregistrée</h3>
  <ul class="details">
    <li><span>Fournisseur</span><strong>{data.get('fournisseur') or '—'}</strong></li>
    <li><span>Montant</span><strong>{montant_str}</strong></li>
    <li><span>Date</span><strong>{data.get('date') or '—'}</strong></li>
    <li><span>Image</span><strong>{image_link}</strong></li>
  </ul>
  <button class="btn btn-secondary" onclick="resetApp()">Nouvelle note de frais</button>
</div>
"""


def _error_html(message: str) -> str:
    return f"""
<div class="card confirmation error">
  <div class="icon">&#10007;</div>
  <h3>Erreur</h3>
  <p>{message}</p>
  <button class="btn btn-secondary" onclick="resetApp()">Réessayer</button>
</div>
"""
