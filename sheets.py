import os
import io
from datetime import datetime
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GoogleSheetsClient:
    def __init__(self):
        creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not creds_path:
            raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON non défini dans .env")

        self.creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)

        gc = gspread.authorize(self.creds)
        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        if not sheet_id:
            raise ValueError("GOOGLE_SHEET_ID non défini dans .env")

        spreadsheet = gc.open_by_key(sheet_id)
        try:
            self.worksheet = spreadsheet.worksheet("Notes de frais")
        except gspread.WorksheetNotFound:
            self.worksheet = spreadsheet.sheet1

        self.drive_service = build("drive", "v3", credentials=self.creds)

    def upload_image_to_drive(
        self, image_bytes: bytes, media_type: str, filename: str
    ) -> str:
        ext_map = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
        }
        ext = ext_map.get(media_type, ".jpg")
        safe_filename = filename.replace("/", "-") + ext

        file_metadata = {"name": safe_filename}
        media = MediaIoBaseUpload(io.BytesIO(image_bytes), mimetype=media_type)

        uploaded = (
            self.drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        file_id = uploaded.get("id")
        self.drive_service.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"},
        ).execute()

        return f"https://drive.google.com/uc?id={file_id}"

    def append_expense(self, data: dict, image_url: str = None) -> None:
        montant = data.get("montant_ttc")
        tva = data.get("tva")

        row = [
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            data.get("type_document") or "",
            data.get("fournisseur") or "",
            data.get("date") or "",
            montant if montant is not None else "",
            tva if tva is not None else "",
            data.get("devise") or "EUR",
            data.get("description") or "",
            data.get("confiance") or "",
            f'=IMAGE("{image_url}")' if image_url else "",
        ]
        self.worksheet.append_row(row, value_input_option="USER_ENTERED")


if __name__ == "__main__":
    client = GoogleSheetsClient()
    test_data = {
        "type_document": "restaurant",
        "fournisseur": "TEST — Bistrot Paul",
        "date": "01/01/2026",
        "montant_ttc": 42.50,
        "tva": 7.08,
        "devise": "EUR",
        "description": "Déjeuner client — test intégration",
        "confiance": "haute",
    }
    client.append_expense(test_data)
    print("Ligne de test ajoutée avec succès.")
