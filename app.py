from flask import Flask, render_template, jsonify import requests import random

app = Flask(name)

PLANET_API_KEY = "PLAK3786870a1d574080ad31c8deacf7d09b"

@app.route('/') def index(): return render_template('index.html')

@app.route('/random-image') def random_image(): lat = random.uniform(-60, 60) lon = random.uniform(-180, 180)

query = {
    "item_types": ["PSScene4Band"],
    "filter": {
        "type": "AndFilter",
        "config": [
            {
                "type": "DateRangeFilter",
                "field_name": "acquired",
                "config": {
                    "gte": "2024-06-01T00:00:00Z",
                    "lte": "2024-06-30T00:00:00Z"
                }
            },
            {
                "type": "GeometryFilter",
                "field_name": "geometry",
                "config": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            }
        ]
    }
}

headers = {"Authorization": f"api-key {PLANET_API_KEY}"}
res = requests.post("https://api.planet.com/data/v1/quick-search", json=query, headers=headers)

items = res.json().get("features", [])
if not items:
    return jsonify({"error": "No images found"}), 404

first = items[0]
thumb = first["_links"].get("thumbnail")
date = first["properties"].get("acquired", "Neznámé")

return jsonify({
    "image": thumb,
    "date": date,
    "location": f"{lat:.2f}, {lon:.2f}"
})

if name == 'main': app.run(debug=True)

