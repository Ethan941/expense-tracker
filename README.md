
# 🧾 Expense Tracker AI — Extraction automatique de notes de frais

Projet d’**IA appliquée** et de **Data Engineering** permettant d’extraire automatiquement les informations importantes depuis un justificatif de dépense : ticket de caisse, facture, reçu, note de restaurant ou document professionnel.

L’objectif est de transformer un document non structuré en données propres, vérifiables et exploitables.

---

## 🎯 Objectif du projet

La gestion des notes de frais est souvent manuelle, répétitive et source d’erreurs.

Ce projet vise à automatiser ce processus grâce à une chaîne de traitement complète :

```txt
Image / justificatif
        ↓
Extraction IA
        ↓
Données structurées JSON
        ↓
Validation utilisateur
        ↓
Export vers Google Sheets / Drive
```

Le projet montre comment utiliser l’IA pour automatiser une tâche métier réelle, tout en structurant les données pour qu’elles puissent être exploitées dans un système d’information.

---

## 🧠 Problématique IA / Data Engineering

Ce projet répond à une problématique fréquente en entreprise :

> Comment transformer des documents non structurés en données fiables, propres et exploitables ?

Les justificatifs de dépenses contiennent souvent des informations importantes mais difficiles à exploiter automatiquement :

- nom du fournisseur ;
- date ;
- montant total ;
- TVA ;
- devise ;
- type de dépense ;
- description ;
- niveau de confiance.

L’objectif est de construire un workflow capable d’extraire ces informations et de les convertir en format structuré.

---

## 🛠️ Technologies utilisées

- Python
- FastAPI
- IA générative / LLM
- API Groq ou autre modèle IA
- JSON
- Google Sheets API
- Google Drive API
- HTML
- CSS
- JavaScript
- HTMX
- Variables d’environnement
- Git / GitHub

---

## 📁 Structure du projet

```txt
expense-tracker/
│
├── app.py                  # Application principale FastAPI
├── backend.py              # Logique d’extraction IA
├── sheets.py               # Intégration Google Sheets / Drive
├── context.txt             # Contexte envoyé au modèle IA
├── prompt.txt              # Prompt d’extraction
├── requirements.txt        # Dépendances Python
├── .env.example            # Exemple de variables d’environnement
├── README.md
│
├── static/
│   ├── index.html          # Interface utilisateur
│   ├── style.css           # Styles CSS
│   └── app.js              # Logique front-end
│
└── uploads/                # Dossier temporaire pour les justificatifs
```

---

## 🔎 Fonctionnalités principales

- Upload d’un justificatif de dépense
- Analyse automatique du document par IA
- Extraction des champs importants
- Transformation des données en JSON structuré
- Affichage des résultats dans une interface utilisateur
- Possibilité de vérifier ou corriger les données extraites
- Export des informations vers Google Sheets
- Archivage du document dans Google Drive
- Automatisation d’un processus administratif réel

---

## 📌 Champs extraits

| Champ | Description |
|---|---|
| `type_document` | Type du justificatif : restaurant, transport, hôtel, facture, autre |
| `fournisseur` | Nom du commerçant ou de l’entreprise |
| `date` | Date du justificatif |
| `montant_ttc` | Montant total TTC |
| `montant_ht` | Montant hors taxe si disponible |
| `tva` | Montant de TVA si disponible |
| `devise` | Devise utilisée |
| `description` | Résumé de la dépense |
| `categorie` | Catégorie de dépense |
| `confiance` | Niveau de confiance de l’extraction |

---

## 🧪 Exemple de sortie JSON

```json
{
  "type_document": "restaurant",
  "fournisseur": "Bistrot Montmartre",
  "date": "12/06/2026",
  "montant_ttc": 28.50,
  "montant_ht": 23.75,
  "tva": 4.75,
  "devise": "EUR",
  "categorie": "repas professionnel",
  "description": "Déjeuner client",
  "confiance": "haute"
}
```

---

## ⚙️ Installation

### 1. Cloner le repository

```bash
git clone https://github.com/Ethan941/expense-tracker.git
cd expense-tracker
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

Sur macOS / Linux :

```bash
source .venv/bin/activate
```

Sur Windows :

```bash
.venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d’environnement

Créer un fichier `.env` à partir du fichier `.env.example`.

Exemple :

```env
GROQ_API_KEY="votre_cle_api"
GOOGLE_SHEET_ID="id_du_google_sheet"
GOOGLE_SERVICE_ACCOUNT_JSON="chemin/vers/credentials.json"
```

### 5. Lancer l’application

```bash
uvicorn app:app --reload
```

Puis ouvrir dans le navigateur :

```txt
http://localhost:8000
```

---

## 📊 Workflow du projet

```txt
1. L’utilisateur ajoute un justificatif
2. Le fichier est envoyé au backend FastAPI
3. L’IA analyse le document
4. Les informations importantes sont extraites
5. Les données sont converties en JSON
6. L’utilisateur vérifie les informations
7. Les données sont envoyées vers Google Sheets
8. Le document est archivé dans Google Drive
```

---

## ✅ Compétences démontrées

- Création d’une API avec FastAPI
- Utilisation d’un modèle IA pour l’extraction d’informations
- Structuration de données en JSON
- Automatisation d’un workflow métier
- Intégration avec Google Sheets
- Intégration avec Google Drive
- Gestion de fichiers
- Gestion de variables d’environnement
- Construction d’un projet IA appliquée
- Logique Data Engineering orientée automatisation

---

## 🚀 Améliorations possibles

- Ajouter une validation des données avec Pydantic
- Ajouter une base PostgreSQL
- Ajouter une authentification utilisateur
- Ajouter un historique des dépenses
- Ajouter des tests unitaires
- Déployer l’application en ligne
- Ajouter une interface plus moderne
- Ajouter un système de correction manuelle
- Ajouter un score de confiance par champ extrait
- Ajouter un dashboard de suivi des dépenses

---

## 📌 Statut du projet

Projet en cours de développement.

L’objectif est de renforcer progressivement l’architecture du projet pour en faire une vraie application d’IA appliquée à un cas métier concret.

---

## 👤 Auteur

**Ethan Pandor**  
Étudiant en Bachelor Data & IA à HETIC  
Recherche stage ou alternance en Data Science / Data Engineering / IA appliquée
