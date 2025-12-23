import os
import subprocess
import sys

def migrate_data():
    print("Starting migration from SQLite to PostgreSQL...")
    
    # Check for DATABASE_URL
    if not os.environ.get('DATABASE_URL'):
        print("ERROR: DATABASE_URL environment variable is not set.")
        print("Run it like this: $env:DATABASE_URL='your_postgres_url'; python migrate_to_postgres.py")
        return

    # 1. Dump data from SQLite database
    dump_file = "sqlite_data_dump.json"
    print(f"Dumping data from SQLite to {dump_file}...")
    
    try:
        # Exclude contenttypes and permissions to avoid conflicts
        dump_cmd = [
            sys.executable, "manage.py", "dumpdata", 
            "--database=sqlite", 
            "--exclude=contenttypes", 
            "--exclude=auth.Permission", 
            "--indent=2",
            "-o", dump_file
        ]
        subprocess.run(dump_cmd, check=True)
        print("Data dumped successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error dumping data: {e}")
        return

    # 2. Run migrations on Postgres (default database)
    print("Running migrations on PostgreSQL...")
    try:
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("Migrations applied to PostgreSQL.")
    except subprocess.CalledProcessError as e:
        print(f"Error applying migrations: {e}")
        return

    # 3. Load data into Postgres
    print(f"Loading data from {dump_file} into PostgreSQL...")
    try:
        # We use --database=default explicitly
        subprocess.run([sys.executable, "manage.py", "loaddata", dump_file], check=True)
        print("Data loaded into PostgreSQL successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error loading data: {e}")
        print("\nFix: If you get IntegrityErrors, you might need to run: python manage.py flush --database=default first.")

    # 4. Cleanup
    if os.path.exists(dump_file):
        print(f"Migration complete. Kept {dump_file} for backup.")

if __name__ == "__main__":
    migrate_data()
