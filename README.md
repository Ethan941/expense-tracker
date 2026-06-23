
Ce repo est très bien aligné avec ton objectif Data Scientist : il a déjà une structure propre avec `data/raw`, `notebooks`, `reports`, `src` et `requirements.txt`, et ton README annonce déjà EDA, modèle de churn, SHAP et recommandations business. :contentReference[oaicite:4]{index=4}

---

# 3. README pour `expense-tracker`

À utiliser si tu as bien les fichiers de l’application. Si tu ne les as pas encore poussés, ajoute une phrase “projet en cours de développement”.

```md
# 🧾 Expense Tracker AI — Extraction automatique de notes de frais

Application IA permettant d’extraire automatiquement les informations importantes d’un justificatif de dépense : ticket de restaurant, facture d’hôtel, billet de train ou reçu professionnel.

Le projet combine **IA générative**, **extraction de données**, **API Python**, **validation JSON** et **automatisation vers Google Sheets / Drive**.

---

## 🎯 Objectif du projet

La gestion des notes de frais est souvent manuelle, lente et source d’erreurs.

L’objectif de cette application est d’automatiser le traitement d’un justificatif :

```txt
Image du justificatif
        ↓
Extraction IA
        ↓
Données structurées JSON
        ↓
Formulaire vérifiable
        ↓
Export Google Sheets / Drive
