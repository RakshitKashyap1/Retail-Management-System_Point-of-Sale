import os
import sys
import subprocess
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ONLINE_DB_URL = os.environ.get('ONLINE_DATABASE_URL')
LOCAL_DB_URL = os.environ.get('LOCAL_DATABASE_URL')

def run_command(command, env):
    """Helper to run shell commands with specific environment variables."""
    try:
        subprocess.run(command, env=env, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Error details: {e}")
        sys.exit(1)

def pull_from_online():
    """
    Replicates ONLINE -> LOCAL.
    1. Dump Online
    2. Flush Local
    3. Load into Local
    """
    print("\n🔄 STARTING PULL (ONLINE -> LOCAL)...")
    
    if not ONLINE_DB_URL or not LOCAL_DB_URL:
        print("❌ Error: Missing DATABASE_URL configurations in .env")
        return

    dump_file = "temp_online_dump.json"
    
    # 1. Dump Online
    print("⬇️  Step 1: Dumping data from ONLINE database...")
    env_online = os.environ.copy()
    env_online['DATABASE_URL'] = ONLINE_DB_URL
    
    dump_cmd = [
        sys.executable, 'manage.py', 'dumpdata',
        '--exclude', 'contenttypes',
        '--exclude', 'auth.Permission',
        '--exclude', 'admin.LogEntry',
        '--exclude', 'sessions.Session',
        '--indent', '2',
        '-o', dump_file
    ]
    # We use subprocess.run directly here avoiding shell=True for list args on some OS if simpler, 
    # but the helper uses shell=True. Let's stick to the helper pattern if we passed a string, 
    # but for list args in python, shell=True can be tricky with quoting.
    # Let's use subprocess directly for safety with env vars.
    try:
        subprocess.run(dump_cmd, env=env_online, check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to dump online data.")
        return

    # 2. Flush Local
    print("🧹 Step 2: Flushing LOCAL database...")
    env_local = os.environ.copy()
    env_local['DATABASE_URL'] = LOCAL_DB_URL
    try:
        subprocess.run([sys.executable, 'manage.py', 'flush', '--no-input'], env=env_local, check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to flush local database.")
        return

    # 3. Load into Local
    print("💾 Step 3: Loading data into LOCAL database...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'loaddata', dump_file], env=env_local, check=True)
        print("✅ PULL COMPLETE: Local database is now in sync with Online.")
    except subprocess.CalledProcessError:
        print("❌ Failed to load data locally.")
    
    if os.path.exists(dump_file):
        os.remove(dump_file)

def push_to_online():
    """
    Replicates LOCAL -> ONLINE.
    1. Dump Local
    2. Flush Online
    3. Load into Online
    """
    print("\n🚀 STARTING PUSH (LOCAL -> ONLINE)...")
    print("⚠️  WARNING: This will OVERWRITE data on the Online database!")
    confirm = input("Are you sure you want to proceed? (type 'yes' to confirm): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return

    if not ONLINE_DB_URL or not LOCAL_DB_URL:
        print("❌ Error: Missing DATABASE_URL configurations in .env")
        return

    dump_file = "temp_local_dump.json"

    # 1. Dump Local
    print("⬇️  Step 1: Dumping data from LOCAL database...")
    env_local = os.environ.copy()
    env_local['DATABASE_URL'] = LOCAL_DB_URL
    
    dump_cmd = [
        sys.executable, 'manage.py', 'dumpdata',
        '--exclude', 'contenttypes',
        '--exclude', 'auth.Permission',
        '--exclude', 'admin.LogEntry',
        '--exclude', 'sessions.Session',
        '--indent', '2',
        '-o', dump_file
    ]
    try:
        subprocess.run(dump_cmd, env=env_local, check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to dump local data.")
        return

    # 2. Flush Online
    print("🧹 Step 2: Flushing ONLINE database...")
    env_online = os.environ.copy()
    env_online['DATABASE_URL'] = ONLINE_DB_URL
    try:
        subprocess.run([sys.executable, 'manage.py', 'flush', '--no-input'], env=env_online, check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to flush online database. Check permissions/connection.")
        return

    # 3. Load into Online
    print("☁️  Step 3: Uploading data to ONLINE database...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'loaddata', dump_file], env=env_online, check=True)
        print("✅ PUSH COMPLETE: Online database is now in sync with Local.")
    except subprocess.CalledProcessError:
        print("❌ Failed to load data online.")

    if os.path.exists(dump_file):
        os.remove(dump_file)

def main():
    parser = argparse.ArgumentParser(description="Synchronize Online and Local Databases")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--pull', action='store_true', help='Pull data FROM Online TO Local (Overwrite Local)')
    group.add_argument('--push', action='store_true', help='Push data FROM Local TO Online (Overwrite Online)')
    
    args = parser.parse_args()

    if args.pull:
        pull_from_online()
    elif args.push:
        push_to_online()

if __name__ == "__main__":
    main()
