import requests
import json
import os

USER_ID = "336797287"

# Wallapop search API filtering by seller
API_URL = "https://api.wallapop.com/api/v3/general/search"

PARAMS = {
    "user_id": USER_ID,
    "order_by": "newest",
    "start": 0,
    "step": 40,
    "language": "es_ES",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-ES,es;q=0.9",
    "Origin": "https://es.wallapop.com",
    "Referer": "https://es.wallapop.com/",
    "DeviceOS": "0",
    "X-AppVersion": "84600",
}


def fetch_products():
    try:
        response = requests.get(API_URL, headers=HEADERS, params=PARAMS, timeout=15)
        print(f"Status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()

        items = (
            data.get("data", {})
            .get("section", {})
            .get("payload", {})
            .get("items", [])
        )

        if not items:
            items = data.get("items", [])
        if not items:
            items = data.get("data", {}).get("items", [])

        print(f"Found {len(items)} items")
        products = []

        for item in items:
            content = item.get("content", item)
            images = content.get("images", [])
            image_url = ""
            if images:
                img = images[0]
                image_url = (
                    img.get("urls", {}).get("big", "")
                    or img.get("urls", {}).get("medium", "")
                    or img.get("original", "")
                    or ""
                )

            price_info = content.get("price", {})
            price = price_info.get("amount", 0) if isinstance(price_info, dict) else price_info

            flags = content.get("flags", {})
            sold = flags.get("sold", False) if isinstance(flags, dict) else False

            slug = content.get("web_slug", content.get("slug", content.get("id", "")))

            products.append({
                "id": content.get("id", ""),
                "title": content.get("title", "Sin título"),
                "price": price,
                "currency": "EUR",
                "status": "sold" if sold else "available",
                "image": image_url,
                "url": f"https://es.wallapop.com/item/{slug}",
                "location": content.get("location", {}).get("city", "Pamplona") if isinstance(content.get("location"), dict) else "Pamplona",
                "condition": "",
            })

        output = {"productos": products, "total": len(products)}
        output_path = os.path.join(os.path.dirname(__file__), "..", "productos.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(products)} productos guardados en productos.json")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    fetch_products()
