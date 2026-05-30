import os
import sqlite3

def run_pure_sql_scenario():
    # Ensure we run relative to this script's location so files find each other
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "../practice_warehouse.db")
    sql_path = os.path.join(script_dir, "database_link.sql")
    
    # 1. Connect to your primary practice database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 2. Read the pure SQL script you just wrote
    with open(sql_path, "r") as sql_file:
        sql_script = sql_file.read()
    
    print("🚀 Executing Cross-Database Link Queries from database_link.sql...")
    
    # 3. Split by semicolon to isolate individual commands
    sql_commands = sql_script.split(';')
    for command in sql_commands:
        clean_command = command.strip()
        
        # 🛠️ FIXED: Skip empty strings or blocks that are just standalone SQL comments
        if not clean_command or clean_command.startswith("--"):
            continue
            
        try:
            cursor.execute(clean_command)
            
            # If the command is our golden SELECT query, grab and print the output records!
            if "SELECT" in clean_command:
                results = cursor.fetchall()
                print("\n🎯 Cross-Database Joined Results Found:")
                print("-" * 80)
                for row in results:
                    print(f"Post ID: {row[0]} | Product: {row[2]} | Stock: {row[3]}")
                print("-" * 80)
                
        except sqlite3.OperationalError as sql_err:
            print(f"❌ Failed executing block:\n{clean_command}\nReason: {sql_err}")
    
    # 4. Clean up the link connection safely
    try:
        cursor.execute("DETACH DATABASE RemoteInventoryDB;")
    except sqlite3.OperationalError:
        pass  # If it wasn't attached, ignore the error on close
        
    cursor.close()
    conn.close()
    print("✅ Scenario run complete. Connection links detached cleanly.")

if __name__ == "__main__":
    run_pure_sql_scenario()