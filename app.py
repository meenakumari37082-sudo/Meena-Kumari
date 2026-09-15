from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import date, timedelta
app = Flask(__name__)
# MySQL connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Meena@2005",
        database="library_db"
    )
# Home page
@app.route("/")
def home():
    return render_template("index.html")
# Add Book
@app.route("/add_book", methods=["POST"])
def add_book():
    data = request.json
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO books (title, author) VALUES (%s, %s)",
        (data["title"], data["author"])
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Book added successfully"})
# Show Books
@app.route("/books")
def books():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(result)
# Add Student
@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.form
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO students (name, email) VALUES (%s, %s)",
        (data["name"], data["email"])
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Student added successfully"})
# Show Students
@app.route("/students")
def students():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(result)
# Borrow Book
@app.route("/borrow_book", methods=["POST"])
def borrow_book():
    data = request.json
    student_id = data["student_id"]
    book_id = data["book_id"]
    db = connect_db()
    cursor = db.cursor()
    # Check book
    cursor.execute(
        "SELECT * FROM books WHERE book_id = %s",
        (book_id,)
    )
    book = cursor.fetchone()
    if book is None:
        cursor.close()
        db.close()
        return jsonify({"message": "Book not found"})
    # Borrow date
    borrow_date = date.today()
    # Due date after 7 days
    due_date = borrow_date + timedelta(days=7)
    cursor.execute("""
        INSERT INTO borrow_records
        (student_id, book_id, borrow_date, due_date)
        VALUES (%s, %s, %s, %s)
    """, (student_id, book_id, borrow_date, due_date))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({
        "message": "Book borrowed successfully",
        "due_date": str(due_date)
    })
# Return Book
@app.route("/return_book", methods=["POST"])
def return_book():
    data = request.json
    borrow_id = data["borrow_id"]
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM borrow_records WHERE borrow_id = %s",
        (borrow_id,)
    )
    record = cursor.fetchone()
    if record is None:
        cursor.close()
        db.close()
        return jsonify({
            "message": "Borrow record not found",
            "fine": 0
        })
    return_date = date.today()
    # Fine ₹10 per late day
    late_days = (return_date - record["due_date"]).days

    if late_days > 0:
        fine = late_days * 10
    else:
        fine = 0
    cursor.execute("""
        UPDATE borrow_records
        SET return_date = %s,
            fine = %s
        WHERE borrow_id = %s
    """, (return_date, fine, borrow_id))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({
        "message": "Book returned successfully",
        "fine": fine
    })
# Borrow Records
@app.route("/borrowed")
def borrowed():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM borrow_records
    """)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(result)
# Run application
if __name__ == "__main__":
    app.run(debug=True)