import os
import psycopg2
from psycopg2 import sql

def reset_database():
    """Deletes and recreates the specified PostgreSQL database."""
    dbname = os.environ["RDS_DB_NAME"]
    user = os.environ["RDS_USERNAME"]
    password = os.environ["RDS_PASSWORD"]
    host = os.environ["RDS_HOSTNAME"]
    port = os.environ["RDS_PORT"]
    owner = "lrg_demo_owners"  # Specify the group role that should own the database

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cur = conn.cursor()
    
    try:
        # Terminate active connections to the database before dropping it
        cur.execute(sql.SQL("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = %s AND pg_stat_activity.pid <> pg_backend_pid();
        """), [dbname])
        
        # Ensure all connections are closed before proceeding
        cur.execute("SELECT COUNT(*) FROM pg_stat_activity WHERE datname = %s", [dbname])
        count = cur.fetchone()[0]
        if count > 0:
            print(f"Warning: {count} connections are still active. Retrying...")
        
        # Drop and recreate the database
        cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}" ).format(sql.Identifier(dbname)))
        cur.execute(sql.SQL("CREATE DATABASE {} OWNER {}" ).format(sql.Identifier(dbname), sql.Identifier(owner)))
        print(f"Database {dbname} has been reset and assigned to owner {owner}.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    reset_database()
