from datetime import date, timedelta
import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for
from .db import get_db

bp = Blueprint("main", __name__)

@bp.get("/")
def dashboard():
    db = get_db()
    stats = {
        "members": db.execute("SELECT COUNT(*) FROM members").fetchone()[0],
        "active_members": db.execute("SELECT COUNT(*) FROM members WHERE status='Active'").fetchone()[0],
        "trainers": db.execute("SELECT COUNT(*) FROM trainers").fetchone()[0],
        "plans": db.execute("SELECT COUNT(*) FROM plans").fetchone()[0],
    }
    recent = db.execute("SELECT * FROM members ORDER BY id DESC LIMIT 5").fetchall()
    upcoming = db.execute("""
        SELECT m.full_name, p.name AS plan_name, ms.end_date
        FROM memberships ms
        JOIN members m ON m.id=ms.member_id
        JOIN plans p ON p.id=ms.plan_id
        WHERE ms.end_date >= date('now')
        ORDER BY ms.end_date LIMIT 5
    """).fetchall()
    return render_template("dashboard.html", stats=stats, recent=recent, upcoming=upcoming)

@bp.route("/members", methods=["GET", "POST"])
def members():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        gender = request.form.get("gender", "").strip()
        status = request.form.get("status", "Active")
        if not name or not email:
            flash("Full name and email are required.", "error")
        else:
            try:
                db.execute("INSERT INTO members(full_name,email,phone,gender,status) VALUES(?,?,?,?,?)",
                           (name, email, phone, gender, status))
                db.commit()
                flash("Member added successfully.", "success")
                return redirect(url_for("main.members"))
            except sqlite3.IntegrityError:
                flash("That email address is already registered.", "error")
    search = request.args.get("q", "").strip()
    rows = db.execute("""
        SELECT * FROM members
        WHERE full_name LIKE ? OR email LIKE ? OR phone LIKE ?
        ORDER BY id DESC
    """, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
    return render_template("members.html", members=rows, search=search)

@bp.route("/members/<int:member_id>/edit", methods=["GET", "POST"])
def edit_member(member_id):
    db = get_db()
    member = db.execute("SELECT * FROM members WHERE id=?", (member_id,)).fetchone()
    if member is None:
        flash("Member not found.", "error")
        return redirect(url_for("main.members"))
    if request.method == "POST":
        values = (
            request.form.get("full_name", "").strip(),
            request.form.get("email", "").strip().lower(),
            request.form.get("phone", "").strip(),
            request.form.get("gender", "").strip(),
            request.form.get("status", "Active"),
            member_id
        )
        if not values[0] or not values[1]:
            flash("Full name and email are required.", "error")
        else:
            try:
                db.execute("""UPDATE members SET full_name=?,email=?,phone=?,gender=?,status=?
                              WHERE id=?""", values)
                db.commit()
                flash("Member updated successfully.", "success")
                return redirect(url_for("main.members"))
            except sqlite3.IntegrityError:
                flash("That email address is already used by another member.", "error")
    return render_template("member_form.html", member=member, title="Edit member")

@bp.post("/members/<int:member_id>/delete")
def delete_member(member_id):
    db = get_db()
    db.execute("DELETE FROM members WHERE id=?", (member_id,))
    db.commit()
    flash("Member deleted.", "success")
    return redirect(url_for("main.members"))

@bp.route("/trainers", methods=["GET", "POST"])
def trainers():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        specialty = request.form.get("specialty", "").strip()
        if not name or not specialty:
            flash("Trainer name and specialty are required.", "error")
        else:
            db.execute("INSERT INTO trainers(full_name,specialty,phone,email) VALUES(?,?,?,?)",
                       (name, specialty, request.form.get("phone","").strip(),
                        request.form.get("email","").strip().lower()))
            db.commit()
            flash("Trainer added successfully.", "success")
            return redirect(url_for("main.trainers"))
    rows = db.execute("SELECT * FROM trainers ORDER BY full_name").fetchall()
    return render_template("trainers.html", trainers=rows)

@bp.post("/trainers/<int:trainer_id>/delete")
def delete_trainer(trainer_id):
    get_db().execute("DELETE FROM trainers WHERE id=?", (trainer_id,))
    get_db().commit()
    flash("Trainer deleted.", "success")
    return redirect(url_for("main.trainers"))

@bp.route("/plans", methods=["GET", "POST"])
def plans():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        try:
            months = int(request.form.get("duration_months", "1"))
            price = float(request.form.get("price", "0"))
        except ValueError:
            months, price = 0, -1
        description = request.form.get("description", "").strip()
        if not name or months < 1 or price < 0:
            flash("Enter a plan name, positive duration, and valid price.", "error")
        else:
            db.execute("INSERT INTO plans(name,duration_months,price,description) VALUES(?,?,?,?)",
                       (name, months, price, description))
            db.commit()
            flash("Membership plan added.", "success")
            return redirect(url_for("main.plans"))
    rows = db.execute("SELECT * FROM plans ORDER BY price").fetchall()
    return render_template("plans.html", plans=rows)

@bp.post("/plans/<int:plan_id>/delete")
def delete_plan(plan_id):
    db = get_db()
    try:
        db.execute("DELETE FROM plans WHERE id=?", (plan_id,))
        db.commit()
        flash("Plan deleted.", "success")
    except sqlite3.IntegrityError:
        flash("This plan is used by a membership and cannot be deleted yet.", "error")
    return redirect(url_for("main.plans"))

@bp.route("/memberships", methods=["GET", "POST"])
def memberships():
    db = get_db()
    if request.method == "POST":
        try:
            member_id = int(request.form["member_id"])
            plan_id = int(request.form["plan_id"])
            start = date.fromisoformat(request.form["start_date"])
            end = start + timedelta(days=30 * int(db.execute(
                "SELECT duration_months FROM plans WHERE id=?", (plan_id,)
            ).fetchone()["duration_months"]))
            db.execute("""INSERT INTO memberships(member_id,plan_id,start_date,end_date,payment_status)
                          VALUES(?,?,?,?,?)""",
                       (member_id, plan_id, start.isoformat(), end.isoformat(),
                        request.form.get("payment_status", "Pending")))
            db.commit()
            flash("Membership assigned successfully.", "success")
            return redirect(url_for("main.memberships"))
        except (ValueError, KeyError, TypeError):
            flash("Please choose a valid member, plan, and start date.", "error")
    rows = db.execute("""
        SELECT ms.*, m.full_name AS member_name, p.name AS plan_name, p.price
        FROM memberships ms JOIN members m ON m.id=ms.member_id
        JOIN plans p ON p.id=ms.plan_id ORDER BY ms.id DESC
    """).fetchall()
    member_options = db.execute("SELECT id,full_name FROM members WHERE status='Active' ORDER BY full_name").fetchall()
    plan_options = db.execute("SELECT id,name,duration_months,price FROM plans ORDER BY price").fetchall()
    return render_template("memberships.html", memberships=rows, members=member_options, plans=plan_options)

@bp.post("/memberships/<int:membership_id>/delete")
def delete_membership(membership_id):
    db = get_db()
    db.execute("DELETE FROM memberships WHERE id=?", (membership_id,))
    db.commit()
    flash("Membership removed.", "success")
    return redirect(url_for("main.memberships"))

@bp.app_errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404
