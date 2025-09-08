from pathlib import Path
import csv
import requests
from openpyxl import Workbook
from utils_logger import logger

def fetch_todos(url: str) -> list[dict]:
    logger.info(f"Fetching {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

def process_todos(data: list[dict]) -> list[tuple]:
    logger.info("Processing data")
    return [
        (d.get("userId"), d.get("id"), (d.get("title") or "").strip(), bool(d.get("completed")))
        for d in data
    ]

def write_csv(rows: list[tuple], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["userId", "id", "title", "completed"])
        w.writerows(rows)

def write_excel(rows: list[tuple], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "todos"
    ws.append(["userId", "id", "title", "completed"])
    for r in rows:
        ws.append(list(r))
    wb.save(path)

def main() -> None:
    logger.info("Starting Project 3")
    url = "https://jsonplaceholder.typicode.com/todos"
    processed = process_todos(fetch_todos(url))
    out = Path("output")
    write_csv(processed, out / "todos.csv")
    write_excel(processed, out / "todos.xlsx")
    logger.info(f"Wrote {len(processed)} rows to output/")
    logger.info("Done.")

if __name__ == "__main__":
    main()