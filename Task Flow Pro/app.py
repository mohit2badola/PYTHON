from flask import Flask, request, jsonify, render_template, redirect, session, send_file
from flask_cors import CORS
from functools import wraps
import sqlite3
from datetime import datetime
import csv
import io
import os

app = Flask(__name__)
app.secret_key = "5793381cc502066f960d08c2cd4ed3bb"
app.config['SESSION_PERMANENT'] = False
CORS(app, supports_credentials=True)

# ---------------- DATABASE ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'task.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        priority TEXT DEFAULT 'Medium',
        due_date TEXT,
        category TEXT DEFAULT 'Personal',
        status TEXT DEFAULT 'To Do',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    # Activity log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        task_id INTEGER,
        details TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

def log_activity(user_id, action, task_id=None, details=""):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO activity_log (user_id, action, task_id, details) VALUES (?, ?, ?, ?)",
            (user_id, action, task_id, details)
        )
        conn.commit()
        conn.close()
    except:
        pass

# ---------------- ADMIN DECORATOR ----------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT is_admin FROM users WHERE id=?", (session["user_id"],))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not user["is_admin"]:
            return "Access Denied. Admin privileges required.", 403
        
        return f(*args, **kwargs)
    return decorated_function

# ---------------- AUTH ROUTES ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (data["username"], data["password"])
            )
            conn.commit()
            user_id = cursor.lastrowid
            log_activity(user_id, "user_signup", details=f"User {data['username']} created account")
        except:
            conn.close()
            return "User already exists"
        
        conn.close()
        return redirect("/login")
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (data["username"], data["password"])
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            log_activity(user["id"], "user_login", details=f"User {user['username']} logged in")
            return redirect("/")
        else:
            return "Invalid credentials"
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        log_activity(session["user_id"], "user_logout", details="User logged out")
    session.clear()
    return redirect("/login")

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("index.html")

# ---------------- TASK ROUTES ----------------
@app.route("/get-tasks")
def get_tasks():
    if "user_id" not in session:
        return jsonify([])
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id=? ORDER BY id DESC", (session["user_id"],))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/add-task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return {"error": "Not logged in"}, 401
    
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO tasks (user_id, title, description, priority, due_date, category, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        session["user_id"], 
        data.get("title", ""), 
        data.get("description", ""),
        data.get("priority", "Medium"),
        data.get("due_date", ""),
        data.get("category", "Personal"),
        "To Do"
    ))
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    log_activity(session["user_id"], "task_created", task_id, f"Task: {data.get('title')}")
    return {"message": "Task added"}

@app.route("/update-task/<int:id>", methods=["PUT"])
def update_task(id):
    if "user_id" not in session:
        return {"error": "Not logged in"}, 401
    
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT title FROM tasks WHERE id=? AND user_id=?", (id, session["user_id"]))
    task = cursor.fetchone()
    
    if task:
        cursor.execute(
            "UPDATE tasks SET status=? WHERE id=? AND user_id=?",
            (data.get("status"), id, session["user_id"])
        )
        conn.commit()
        log_activity(session["user_id"], "task_updated", id, f"Task: {task['title']} status changed to {data.get('status')}")
    
    conn.close()
    return {"message": "Task updated"}

@app.route("/edit-task/<int:id>", methods=["PUT"])
def edit_task(id):
    if "user_id" not in session:
        return {"error": "Not logged in"}, 401
    
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE tasks 
        SET title=?, description=?, priority=?, due_date=?, category=? 
        WHERE id=? AND user_id=?
    """, (data.get("title"), data.get("description"), data.get("priority"), 
          data.get("due_date"), data.get("category"), id, session["user_id"]))
    
    conn.commit()
    conn.close()
    
    log_activity(session["user_id"], "task_edited", id, f"Task edited: {data.get('title')}")
    return {"message": "Task updated"}

@app.route("/delete-task/<int:id>", methods=["DELETE"])
def delete_task(id):
    if "user_id" not in session:
        return {"error": "Not logged in"}, 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT title FROM tasks WHERE id=? AND user_id=?", (id, session["user_id"]))
    task = cursor.fetchone()
    
    if task:
        cursor.execute("DELETE FROM tasks WHERE id=? AND user_id=?", (id, session["user_id"]))
        conn.commit()
        log_activity(session["user_id"], "task_deleted", id, f"Task deleted: {task['title']}")
    
    conn.close()
    return {"message": "Task deleted"}

# ---------------- STATISTICS ROUTE ----------------
@app.route("/get-stats")
def get_stats():
    if "user_id" not in session:
        return jsonify({}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id=?", (session["user_id"],))
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id=? AND status='Completed'", (session["user_id"],))
    completed = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id=? AND due_date=date('now')", (session["user_id"],))
    due_today = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total': total,
        'completed': completed,
        'progress': total - completed,
        'due_today': due_today,
        'completion_rate': round((completed/total)*100, 1) if total > 0 else 0
    })

# ---------------- EXPORT ROUTES ----------------
@app.route("/export-today-tasks")
def export_today_tasks():
    if "user_id" not in session:
        return "Not logged in", 401
    
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT title, status, priority, due_date, category 
        FROM tasks 
        WHERE user_id=? AND due_date=?
    """, (session["user_id"], today))
    
    tasks = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Title', 'Status', 'Priority', 'Due Date', 'Category'])
    
    for task in tasks:
        writer.writerow([task['title'], task['status'], task['priority'], task['due_date'], task['category']])
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'tasks_{today}.csv'
    )

@app.route("/export-all-tasks")
def export_all_tasks():
    if "user_id" not in session:
        return "Not logged in", 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, status, priority, due_date, category, created_at 
        FROM tasks 
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (session["user_id"],))
    
    tasks = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Title', 'Status', 'Priority', 'Due Date', 'Category', 'Created At'])
    
    for task in tasks:
        writer.writerow([task['title'], task['status'], task['priority'], task['due_date'], task['category'], task['created_at']])
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'all_tasks_{datetime.now().strftime("%Y%m%d")}.csv'
    )

# ---------------- ACTIVITY ROUTE ----------------
@app.route("/get-activity")
def get_activity():
    if "user_id" not in session:
        return jsonify([]), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT action, details, timestamp 
        FROM activity_log 
        WHERE user_id=? 
        ORDER BY timestamp DESC 
        LIMIT 20
    """, (session["user_id"],))
    
    logs = cursor.fetchall()
    conn.close()
    return jsonify([dict(log) for log in logs])

# ================ ADMIN PANEL ROUTES ================

@app.route("/admin")
@admin_required
def admin_panel():
    """Main admin dashboard"""
    return render_template("admin.html")

@app.route("/admin/users")
@admin_required
def admin_get_users():
    """Get all users with their task counts"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.id, u.username, u.created_at, u.is_admin,
               COUNT(t.id) as total_tasks,
               SUM(CASE WHEN t.status = 'Completed' THEN 1 ELSE 0 END) as completed_tasks
        FROM users u
        LEFT JOIN tasks t ON u.id = t.user_id
        GROUP BY u.id
        ORDER BY u.created_at DESC
    """)
    
    users = cursor.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route("/admin/user/<int:user_id>")
@admin_required
def admin_get_user_details(user_id):
    """Get detailed information about a specific user"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, created_at, is_admin FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    cursor.execute("""
        SELECT id, title, status, priority, due_date, category, created_at, completed_at
        FROM tasks 
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,))
    
    tasks = cursor.fetchall()
    
    cursor.execute("""
        SELECT action, details, timestamp
        FROM activity_log
        WHERE user_id=?
        ORDER BY timestamp DESC
        LIMIT 50
    """, (user_id,))
    
    activities = cursor.fetchall()
    conn.close()
    
    return jsonify({
        "user": dict(user),
        "tasks": [dict(task) for task in tasks],
        "activities": [dict(activity) for activity in activities]
    })

@app.route("/admin/all-tasks")
@admin_required
def admin_get_all_tasks():
    """Get all tasks from all users"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT t.*, u.username as owner_name
        FROM tasks t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.created_at DESC
        LIMIT 100
    """)
    
    tasks = cursor.fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

@app.route("/admin/delete-user/<int:user_id>", methods=["DELETE"])
@admin_required
def admin_delete_user(user_id):
    """Delete a user and all their tasks"""
    if user_id == session["user_id"]:
        return jsonify({"error": "Cannot delete your own admin account"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE user_id=?", (user_id,))
    cursor.execute("DELETE FROM activity_log WHERE user_id=?", (user_id,))
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User deleted successfully"})

@app.route("/admin/stats")
@admin_required
def admin_get_stats():
    """Get overall admin statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'")
    completed_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT priority, COUNT(*) FROM tasks GROUP BY priority")
    priority_stats = dict(cursor.fetchall())
    
    cursor.execute("SELECT category, COUNT(*) FROM tasks GROUP BY category")
    category_stats = dict(cursor.fetchall())
    
    cursor.execute("""
        SELECT al.*, u.username
        FROM activity_log al
        JOIN users u ON al.user_id = u.id
        ORDER BY al.timestamp DESC
        LIMIT 20
    """)
    recent_activity = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        "total_users": total_users,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": round((completed_tasks/total_tasks)*100, 1) if total_tasks > 0 else 0,
        "priority_stats": priority_stats,
        "category_stats": category_stats,
        "recent_activity": [dict(activity) for activity in recent_activity]
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    print("TaskFlow Pro Server Starting...")
    app.run(debug=True)