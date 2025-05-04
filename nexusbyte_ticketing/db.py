import psycopg2

# Function to connect to the database
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",  # or your host
            database="nexusbyte_ticketing",  # replace with your actual DB name
            user="postgres",  # replace with your actual user
            password="2025Nexus"  # replace with your password
        )
        return conn
    except Exception as e:
        print("❌ Connection failed:", e)
        return None

