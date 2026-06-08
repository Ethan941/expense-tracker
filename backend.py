import os
import base64
import json
import sys
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

EXPECTED_FIELDS = [
    "type_document", "fournisseur", "date", "montant_ttc",
    "tva", "devise", "description", "confiance"
]


class ExpenseAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY non défini dans .env")
        self.client = Groq(api_key=api_key)
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, "context.txt"), "r", encoding="utf-8") as f:
            self.system_prompt = f.read().strip()
        with open(os.path.join(base_dir, "prompt.txt"), "r", encoding="utf-8") as f:
            self.user_prompt = f.read().strip()

    def extract_from_bytes(self, image_bytes: bytes, media_type: str) -> dict:
        image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

        response = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{image_b64}"
                            },
                        },
                        {"type": "text", "text": self.user_prompt},
                    ],
                },
            ],
            max_tokens=1024,
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        result = {field: data.get(field, None) for field in EXPECTED_FIELDS}

        for field in ("montant_ttc", "tva"):
            val = result[field]
            if val is not None:
                try:
                    result[field] = float(val)
                except (ValueError, TypeError):
                    result[field] = None

        return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backend.py <chemin_image>")
        sys.exit(1)

    image_path = sys.argv[1]
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }
    media_type = mime_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    agent = ExpenseAgent()
    result = agent.extract_from_bytes(image_bytes, media_type)
    print(json.dumps(result, indent=2, ensure_ascii=False))
