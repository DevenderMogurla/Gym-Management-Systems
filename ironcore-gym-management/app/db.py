import sqlite3
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        gender TEXT,
        joined_on TEXT NOT NULL DEFAULT (date('now')),
        status TEXT NOT NULL DEFAULT 'Active'
    );
    CREATE TABLE IF NOT EXISTS trainers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        phone TEXT,
        email TEXT
    );
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        duration_months INTEGER NOT NULL,
        price REAL NOT NULL,
        description TEXT
    );
    CREATE TABLE IF NOT EXISTS memberships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        plan_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        payment_status TEXT NOT NULL DEFAULT 'Pending',
        FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE,
        FOREIGN KEY(plan_id) REFERENCES plans(id) ON DELETE RESTRICT
    );
    """)

    # Seed example data once, so the dashboard is useful immediately.
    if db.execute("SELECT COUNT(*) FROM plans").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO plans (name, duration_months, price, description) VALUES (?, ?, ?, ?)",
            [
                ("Starter", 1, 999, "Access to gym floor and standard equipment."),
                ("Quarterly", 3, 2499, "Three months of training access."),
                ("Annual Elite", 12, 8999, "Full-year access with priority support.")
            ],
        )
    if db.execute("SELECT COUNT(*) FROM trainers").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO trainers (full_name, specialty, phone, email) VALUES (?, ?, ?, ?)",
            [
                ("Arjun Rao", "Strength & Conditioning", "9876543210", "arjun@example.com"),
                ("Priya Sharma", "Yoga & Mobility", "9876501234", "priya@example.com")
            ],
        )
    if db.execute("SELECT COUNT(*) FROM members").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO members (full_name, email, phone, gender, status) VALUES (?, ?, ?, ?, ?)",
            [
                ("Rahul Kumar", "rahul@example.com", "9000011111", "Male", "Active"),
                ("Sneha Reddy", "sneha@example.com", "9000022222", "Female", "Active"),
                ("Kiran Das", "kiran@example.com", "9000033333", "Male", "Inactive")
            ],
        )
    db.commit()
    close_db()
