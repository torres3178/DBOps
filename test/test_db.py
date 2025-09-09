import psycopg2
import time

TEST_DSN = "postgresql://test:secret@127.0.0.1:55432/testdb"

def test_users_table_roundtrip():
    # Wait until DB is ready
    for _ in range(30):
        try:
            psycopg2.connect(TEST_DSN).close()
            break
        except Exception:
            time.sleep(1)

    with psycopg2.connect(TEST_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (username, email) VALUES ('alice', 'a@example.com') RETURNING id")
            new_id = cur.fetchone()[0]
            cur.execute("SELECT username, email FROM users WHERE id=%s", (new_id,))
            row = cur.fetchone()
            assert row[0] == 'alice'
            assert row[1] == 'a@example.com'
