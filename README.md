# Outfit service

Builds one scored outfit from a user's processed wardrobe. This FastAPI service fetches items over HTTP and stores suggestion exposure counts in Redis; it owns no garment database and loads no ML model.

[Project overview](../../README.md) · [Wardrobe API](../wardrobe-service/README.md) · [Model behavior](../ml-inference/README.md)

## Selection and scoring

1. Validate the access JWT and forward it to wardrobe when fetching the owner's items.
2. Keep only `ready` items with embeddings and supported categories.
3. Build combinations with one top, one bottom and one pair of shoes. Outerwear and one accessory are optional. Both `outer` and `outerwear` categories are accepted.
4. Consider all combinations up to 500; for larger inventories, sample 500 combinations without constructing the full Cartesian product.
5. Rank by mean pairwise normalized cosine similarity: `(cosine + 1) / 2`, yielding a score in `[0, 1]`.
6. Within the highest-ranked `top_n` candidates, choose using `score / (1 + shown_count)`, then increment that outfit's exposure counter.

The returned score is the original visual score, not the history-adjusted selection score. It is not a calibrated probability, color-rule engine or professional styling assessment. Sampling and history mean repeated requests can produce different results.

Counters use `outfit_shown:<sorted item UUIDs>` keys with a seven-day TTL refreshed on display. They track suggestions, not confirmed real-world wear.

## HTTP API

```http
GET /outfits/suggest?top_n=5
Authorization: Bearer <access_token>
```

The public gateway is `http://localhost:8080`. `top_n` is an integer from 1 to 20, default 5. It controls the candidate pool for rotation; the endpoint returns **one outfit**, not `top_n` outfits.

Response shape:

```json
{
  "items": [
    {
      "id": "00000000-0000-4000-8000-000000000001",
      "user_id": "00000000-0000-4000-8000-000000000002",
      "category": "top",
      "image_url": "http://localhost:8080/items/00000000-0000-4000-8000-000000000001/image",
      "subcategory": "t-shirt",
      "style": "casual",
      "color_hex": "#f5f5f5"
    }
  ],
  "score": 0.69,
  "message": null
}
```

The item above illustrates the item schema; a normal outfit includes at least top, bottom and shoes. Embeddings are not returned in suggestions. An incomplete wardrobe returns HTTP 200 with `items: []`, `score: null` and an explanatory `message`.

Invalid authentication returns 401 and invalid `top_n` returns 422. A missing `ITEMS_URL` or wardrobe connection failure returns 503. Wardrobe HTTP error statuses are propagated. Redis history is required for suggestion selection.

## Configuration

Settings: [app/core/config.py](app/core/config.py). Unlike the Pydantic-based APIs, this configuration reads process environment variables and does not load a local `.env` itself.

| Variable | Root Compose value / purpose |
| --- | --- |
| `ITEMS_URL` | `http://wardrobe:8000/items/`; owner item-list endpoint |
| `REDIS_URL` | `redis://outfit-redis:6379/0`; exposure history |
| `SECRET_KEY` | Same JWT secret as auth/wardrobe |
| `ALGORITHM` | `HS256` |
| `CORS_ORIGINS` | Comma-separated browser origins from root configuration |

The wardrobe HTTP request has a 30-second timeout. Redis clients are closed at the end of each request. There are no migrations for this service.

## Run and health

From the project root:

```bash
python scripts/setup.py
docker compose up --build -d --wait --wait-timeout 900
docker compose logs -f outfit
curl http://localhost:8080/health/outfit
```

Uvicorn listens internally on port **8003**. `/health/live` checks the process and `/health/ready` checks Redis; readiness does not fetch wardrobe or validate inventory completeness. The gateway maps `/health/outfit` to readiness.

For native development, export the settings above with host-reachable addresses, then run `uvicorn app.main:app --reload --port 8003` from this directory. Root Compose does not publish internal Redis/API ports.

## Checks

Use an isolated Python 3.12 environment. From the root:

```bash
python -m pip install -r backend/outfit-service/requirements.txt -r requirements-test.txt
cd backend/outfit-service
python -m pytest -q
python -m compileall -q app
```

Tests cover ready filtering, required categories, outerwear, bounded generation, actual similarity scores, history rotation and empty inventories. A real integration check needs three processed garment photos; see the [root smoke commands](../../README.md#development-and-checks).
