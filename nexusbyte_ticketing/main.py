from db import connect_db

def main():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id SERIAL PRIMARY KEY,
                subject TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("✅ Table created or already exists.")

        # Example insert (you can remove or change this later)
        cursor.execute("""
            INSERT INTO tickets (subject, description)
            VALUES (%s, %s)
        """, ("Example Ticket", "This is just a test."))
        conn.commit()
        print("🎫 Sample ticket added.")

        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
