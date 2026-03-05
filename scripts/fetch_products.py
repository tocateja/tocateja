import requests
import json
import os

USER_ID = "336797287"
API_URL = f"https://api.wallapop.com/api/v3/users/{USER_ID}/items?published=true&language=es_ES"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "DeviceOS": "0",
    "Accept-Language": "es-ES,es;q=0.9",
}

def fetch_products():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()

        items = data.get("data", {}).get("items", [])
        products = []

        for item in items:
            content = item.get("content", item)
            images = content.get("images", [])
            image_url = images[0].get("urls", {}).get("big", "") if images else ""

            products.append({
                "id": content.get("id", ""),
                "title": content.get("title", "Sin título"),
                "price": content.get("price", {}).get("amount", 0),
                "currency": content.get("price", {}).get("currency", "EUR"),
                "status": content.get("flags", {}).get("sold", False) and "sold" or "available",
                "image": image_url,
                "url": f"https://es.wallapop.com/item/{content.get('slug', content.get('id', ''))}",
                "location": content.get("location", {}).get("city", "Pamplona"),
                "condition": content.get("extra_conditions", {}).get("condition_str", ""),
            })

        output = {"productos": products, "total": len(products)}
        output_path = os.path.join(os.path.dirname(__file__), "..", "productos.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(products)} productos guardados en productos.json")

    except Exception as e:
        print(f"❌ Error: {e}")
        # Si falla, no sobreescribir el JSON existente
        raise

if __name__ == "__main__":
    fetch_products()
