"""Local-only, fictional appointment API for a QA portfolio. Python 3.11+."""
import json
import re
import sqlite3
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEMO_TOKENS = {"demo-patient-1": 1, "demo-patient-2": 2}


def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def initialize(path):
    with connect(path) as db:
        db.executescript((ROOT / "sql/schema.sql").read_text())


def make_server(db_path, port=8000):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, status, payload):
            raw = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            self.route()

        def do_POST(self):
            self.route()

        def route(self):
            path = urlsplit(self.path).path
            if self.command == "GET" and path == "/health":
                return self.reply(200, {"status": "ok"})
            token = self.headers.get("Authorization", "")
            patient = DEMO_TOKENS.get(token.removeprefix("Bearer ")) if token.startswith("Bearer ") else None
            if patient is None:
                return self.reply(401, {"error": "Demo bearer token required"})
            if self.command == "GET" and path == "/appointments":
                with connect(db_path) as db:
                    rows = db.execute("SELECT * FROM appointments WHERE patient_id=? ORDER BY id", (patient,)).fetchall()
                return self.reply(200, [dict(row) for row in rows])
            match = re.fullmatch(r"/appointments/(\d+)/cancel", path)
            if self.command == "POST" and match:
                with connect(db_path) as db:
                    # Owner-scoped update prevents cancelling another patient's appointment.
                    changed = db.execute("UPDATE appointments SET status='cancelled' WHERE id=? AND patient_id=?", (int(match[1]), patient)).rowcount
                return self.reply(200 if changed else 404, {"status": "cancelled"} if changed else {"error": "Appointment not found"})
            if self.command != "POST" or path != "/appointments":
                return self.reply(404, {"error": "Route not found"})
            if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
                return self.reply(415, {"error": "Use application/json"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 8192:
                    raise ValueError()
                body = json.loads(self.rfile.read(length))
            except (ValueError, UnicodeDecodeError):
                return self.reply(400, {"error": "Invalid JSON body or length"})
            if not isinstance(body, dict) or set(body) != {"provider_id", "visit_date"}:
                return self.reply(400, {"error": "Exactly provider_id and visit_date are required"})
            if type(body["provider_id"]) is not int or body["provider_id"] < 1:
                return self.reply(400, {"error": "provider_id must be a positive integer"})
            try:
                value = body["visit_date"]
                if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError()
                visit = date.fromisoformat(value)
                if visit <= date.today():
                    raise ValueError()
            except ValueError:
                return self.reply(400, {"error": "visit_date must be a future date in YYYY-MM-DD format"})
            try:
                with connect(db_path) as db:
                    if not db.execute("SELECT 1 FROM providers WHERE id=?", (body["provider_id"],)).fetchone():
                        return self.reply(404, {"error": "Provider not found"})
                    cursor = db.execute("INSERT INTO appointments(patient_id, provider_id, visit_date) VALUES(?,?,?)", (patient, body["provider_id"], value))
                    new_id = cursor.lastrowid
            except sqlite3.IntegrityError:
                return self.reply(409, {"error": "Provider already booked for this date"})
            return self.reply(201, {"id": new_id, "patient_id": patient, **body, "status": "scheduled"})

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="portal.db")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    initialize(args.db)
    server = make_server(args.db, args.port)
    print(f"Fictional demo API: http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
