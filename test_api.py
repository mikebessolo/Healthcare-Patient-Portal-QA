"""Real local HTTP requests against an isolated SQLite database per test."""
import json
import sqlite3
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from app.server import connect, initialize, make_server

FUTURE = (date.today() + timedelta(days=30)).isoformat()


class PortalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / 'test.db'
        initialize(self.db)
        self.server = make_server(self.db, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def request(self, method='GET', path='/appointments', body=None, token='demo-patient-1', raw=None, content_type='application/json'):
        headers = {'Content-Type': content_type}
        if token is not None:
            headers['Authorization'] = 'Bearer ' + token
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
        request = Request(f'http://127.0.0.1:{self.server.server_port}{path}', data=data, headers=headers, method=method)
        try:
            response = urlopen(request, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            return response.status, json.load(response)

    def book(self, **changes):
        return self.request('POST', body={'provider_id': 1, 'visit_date': FUTURE, **changes})

    def test_health_without_token(self):
        self.assertEqual(self.request(path='/health', token=None), (200, {'status': 'ok'}))

    def test_missing_token(self):
        self.assertEqual(self.request(token=None)[0], 401)

    def test_invalid_token(self):
        self.assertEqual(self.request(token='wrong')[0], 401)

    def test_new_patient_empty_list(self):
        self.assertEqual(self.request(), (200, []))

    def test_booking_persists_correct_data(self):
        code, item = self.book()
        self.assertEqual(code, 201)
        with connect(self.db) as db:
            actual = dict(db.execute('SELECT * FROM appointments').fetchone())
        self.assertEqual(actual, item)

    def test_patient_only_sees_own_records(self):
        self.book()
        self.assertEqual(self.request(token='demo-patient-2'), (200, []))

    def test_unknown_provider(self):
        self.assertEqual(self.book(provider_id=99)[0], 404)

    def test_provider_type_and_boundaries(self):
        for value in [True, '1', 1.5, 0, -1, None]:
            with self.subTest(value=value):
                self.assertEqual(self.book(provider_id=value)[0], 400)

    def test_date_boundaries(self):
        for value in [date.today().isoformat(), '2000-01-01', '2099-02-30', '20990101', None, 123]:
            with self.subTest(value=value):
                self.assertEqual(self.book(visit_date=value)[0], 400)
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        self.assertEqual(self.book(visit_date=tomorrow)[0], 201)

    def test_missing_fields(self):
        self.assertEqual(self.request('POST', body={'provider_id': 1})[0], 400)

    def test_cannot_assign_patient_through_body(self):
        self.assertEqual(self.book(patient_id=2)[0], 400)

    def test_invalid_json_and_shape(self):
        for raw in [b'{broken', b'[]', b'null', b'"text"', b'\xff']:
            with self.subTest(raw=raw):
                self.assertEqual(self.request('POST', raw=raw)[0], 400)

    def test_wrong_content_type(self):
        self.assertEqual(self.request('POST', body={}, content_type='text/plain')[0], 415)

    def test_duplicate_booking(self):
        self.book()
        self.assertEqual(self.book()[0], 409)
        with connect(self.db) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM appointments').fetchone()[0], 1)

    def test_concurrent_booking_has_one_winner(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            codes = list(pool.map(lambda _: self.book()[0], range(2)))
        self.assertEqual(sorted(codes), [201, 409])

    def test_cancel_and_rebook(self):
        _, item = self.book()
        path = f'/appointments/{item["id"]}/cancel'
        self.assertEqual(self.request('POST', path)[0], 200)
        self.assertEqual(self.request()[1][0]['status'], 'cancelled')
        self.assertEqual(self.request('POST', path)[0], 200)
        self.assertEqual(self.book()[0], 201)

    def test_cannot_cancel_another_patient_record(self):
        _, item = self.book()
        self.assertEqual(self.request('POST', f'/appointments/{item["id"]}/cancel', token='demo-patient-2')[0], 404)
        self.assertEqual(self.request()[1][0]['status'], 'scheduled')

    def test_unknown_appointment(self):
        self.assertEqual(self.request('POST', '/appointments/999/cancel')[0], 404)

    def test_unknown_route(self):
        self.assertEqual(self.request(path='/missing')[0], 404)

    def test_database_rejects_orphan_and_invalid_status(self):
        for statement in [
            "INSERT INTO appointments(patient_id,provider_id,visit_date) VALUES(999,1,'2099-01-01')",
            "INSERT INTO appointments(patient_id,provider_id,visit_date,status) VALUES(1,1,'2099-01-01','bad')",
        ]:
            with self.subTest(statement=statement), connect(self.db) as db:
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute(statement)


if __name__ == '__main__':
    unittest.main()
