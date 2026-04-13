# Deal Intelligence Assistant

Full-stack app for uploading financial CSVs, computing deal metrics with **pandas**, comparing multiple files, and optionally generating short explanations via the **OpenAI API** (placeholder mode when no key is set).

## Project layout

```
/backend          FastAPI app (main.py, analysis.py, routes/, utils/)
/frontend         React + Vite + Axios
/sample-data      Example CSVs for testing
```

## CSV format

The backend recognizes common column names (case-insensitive, spaces → underscores):

| Concept        | Accepted column names (any one match) |
|----------------|----------------------------------------|
| Revenue        | `revenue`, `sales`, `total_revenue`, `income`, `gross_revenue` |
| Expenses       | `expenses`, `expense`, `costs`, `cost`, `cogs`, `operating_expenses` |
| Asking price   | `asking_price`, `purchase_price`, `acquisition_cost`, `price`, `deal_price` |

- **Required:** at least one revenue column and one expenses column.
- **Optional:** asking price (repeated value per row is fine). Used for **ROI** = `(net_profit / asking_price) * 100`.
- Each **row** is treated as a period; numeric columns are coerced and **summed** for totals.

Example minimal file:

```csv
month,revenue,expenses,asking_price
2024-01,120000,78000,450000
2024-02,125000,80000,450000
```

Try the files in `sample-data/` (`deal_alpha.csv`, `deal_beta.csv`, `deal_gamma.csv`).

## Backend (FastAPI)

**Prerequisites:** Python 3.10+

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health: `GET /health`

### Endpoints

| Method | Path        | Description |
|--------|-------------|-------------|
| POST   | `/upload`   | Multipart file field `file` — validates CSV, stores in memory, returns `file_id` |
| POST   | `/analyze`  | JSON `{ "file_id": "..." }` — metrics for one file |
| POST   | `/compare`  | JSON `{ "file_ids": ["...", "..."] }` — rankings + best deal |
| POST   | `/insights` | JSON `{ "metrics": { ... }, "context": "optional" }` — OpenAI or placeholder |

**OpenAI (optional):** set `OPENAI_API_KEY`. Optional `OPENAI_MODEL` (default `gpt-4o-mini`).

**Note:** Uploaded files are kept in an **in-memory** store (cleared on server restart). For persistence, you can extend with Supabase or another database.

## Frontend (React + Vite)

**Prerequisites:** Node 18+

```bash
cd frontend
npm install
npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173). The dev server **proxies** `/upload`, `/analyze`, `/compare`, `/insights`, and `/health` to `http://127.0.0.1:8000`.

**Production / custom API URL:** set `VITE_API_URL` (e.g. `https://api.example.com`) before `npm run build`.

## Quick API test (curl)

```bash
cd backend && source .venv/bin/activate
uvicorn main:app --port 8000 &
FILE_ID=$(curl -s -F "file=@../sample-data/deal_alpha.csv" http://127.0.0.1:8000/upload | python3 -c "import sys,json; print(json.load(sys.stdin)['file_id'])")
curl -s -X POST http://127.0.0.1:8000/analyze -H "Content-Type: application/json" -d "{\"file_id\":\"$FILE_ID\"}" | python3 -m json.tool
```

## Tech stack summary

- **Backend:** Python 3, FastAPI, pandas, numpy (via dependencies), optional httpx → OpenAI.
- **Frontend:** React (Vite), Axios, functional components.

## License

Use and modify freely for your own projects.
