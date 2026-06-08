# Expense Tracker — Application Agentique de Notes de Frais

Application web qui permet à un salarié de photographier un justificatif (ticket de restaurant, billet de train, facture d'hôtel) et d'en extraire automatiquement les informations via IA, avant de les synchroniser dans un Google Sheet partagé.

## Fonctionnement

```
Photo → Llama 4 Scout (Groq) → Formulaire éditable → Google Sheets + Drive
```

1. L'utilisateur dépose ou capture une photo du justificatif
2. Le modèle de vision extrait les 8 champs clés (montant, fournisseur, date, etc.)
3. Les données s'affichent dans un formulaire modifiable
4. En un clic, tout est envoyé vers Google Sheets et l'image est archivée dans Drive

## Stack technique

| Composant    | Technologie                                       |
|--------------|---------------------------------------------------|
| Modèle IA    | `meta-llama/llama-4-scout-17b-16e-instruct` (Groq) |
| Backend      | Python 3 · FastAPI                                |
| Frontend     | HTML · HTMX · CSS · JS Vanilla                    |
| Intégration  | Google Sheets API + Google Drive API (gspread)    |

## Structure du projet

```
expense-tracker/
├── app.py           # Serveur FastAPI — routes et fragments HTML
├── backend.py       # Classe ExpenseAgent — appels Groq + extraction JSON
├── sheets.py        # Classe GoogleSheetsClient — écriture Sheets + upload Drive
├── context.txt      # Prompt système du modèle
├── prompt.txt       # Prompt utilisateur envoyé avec l'image
├── requirements.txt
├── .env.example     # Variables d'environnement à renseigner
└── static/
    ├── index.html   # Interface HTMX (dark mode)
    ├── style.css
    └── app.js       # Prévisualisation image + logique HTMX
```

## Installation

### 1. Cloner et installer les dépendances

```bash
git clone https://github.com/<votre-username>/expense-tracker.git
cd expense-tracker
python3 -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Renseigner `.env` :

```env
GROQ_API_KEY="votre_clé_groq"
GOOGLE_SHEET_ID="identifiant_du_sheet"
GOOGLE_SERVICE_ACCOUNT_JSON="chemin/vers/credentials.json"
```

### 3. Configuration Google Cloud

1. Créer un projet sur [console.cloud.google.com](https://console.cloud.google.com)
2. Activer **Google Sheets API** et **Google Drive API**
3. Créer un compte de service (rôle : Éditeur), télécharger la clé JSON
4. Créer un Google Sheet, renommer la feuille en `Notes de frais`
5. Ajouter les en-têtes : `Horodatage | Type | Fournisseur | Date | Montant TTC (€) | TVA (€) | Devise | Description | Confiance | Image`
6. Partager le Sheet avec l'email du compte de service (rôle Éditeur)
7. Copier l'ID du Sheet depuis l'URL (`/d/<ID>/edit`)

> **Important** : ne jamais commiter le fichier JSON des credentials ni le `.env`.

### 4. Lancer l'application

```bash
uvicorn app:app --reload
```

Ouvrir [http://localhost:8000](http://localhost:8000)

## Exemple de réponse JSON du modèle

```json
{
  "type_document": "restaurant",
  "fournisseur": "Bistrot Paul",
  "date": "05/06/2026",
  "montant_ttc": 28.50,
  "tva": 4.75,
  "devise": "EUR",
  "description": "Déjeuner client — réunion projet",
  "confiance": "haute"
}
```

## Tester le backend seul

```bash
python backend.py chemin/vers/ticket.jpg
```

## Tester l'intégration Google Sheets

```bash
python sheets.py
```

Envoie une ligne de test dans le Sheet pour valider l'authentification.

## Champs extraits

| Champ          | Description                                              |
|----------------|----------------------------------------------------------|
| `type_document`| `restaurant` · `transport` · `hôtel` · `autre`          |
| `fournisseur`  | Nom du commerce ou de la compagnie                       |
| `date`         | Format JJ/MM/AAAA                                        |
| `montant_ttc`  | Montant total TTC en euros (décimal)                     |
| `tva`          | TVA si lisible, sinon `null`                             |
| `devise`       | EUR par défaut                                           |
| `description`  | Motif de la dépense                                      |
| `confiance`    | `haute` · `moyen` · `basse`                              |

## Clé Groq

Obtenir une clé gratuite sur [console.groq.com](https://console.groq.com)
