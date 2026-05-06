import sqlite3
import os

DB_PATH = '/home/badolamohit/task.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check if admin column exists, if not add it
try:
    cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
    print("✓ Added is_admin column")
except:
    print("ℹ is_admin column already exists")

# Check if admin user exists
cursor.execute("SELECT * FROM users WHERE username='admin'")
admin = cursor.fetchone()

if admin:
    print("✓ Admin user already exists")
    # Make sure admin has is_admin=1
    cursor.execute("UPDATE users SET is_admin=1 WHERE username='admin'")
else:
    # Create admin user
    cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                   ('admin', 'admin123', 1))
    print("✓ Admin user created!")

conn.commit()
conn.close()

print("\n✅ Admin setup complete!")
print("Username: admin")
print("Password: admin123")