// ADD BOOK
document.getElementById("bookForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const author = document.getElementById("author").value;

    const response = await fetch("/add_book", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            author: author
        })
    });
    const data = await response.json();

    alert(data.message || "Book Added Successfully!");

    document.getElementById("bookForm").reset();

    loadBooks();
});


// ADD STUDENT
document.getElementById("studentForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;

    const response = await fetch("/add_student", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            email: email
        })
    });

    const data = await response.json();

    alert(data.message || "Student Added Successfully!");

    document.getElementById("studentForm").reset();

    loadStudents();
});


// LOAD BOOKS
async function loadBooks() {

    const response = await fetch("/books");
    const books = await response.json();

    const bookList = document.getElementById("bookList");

    bookList.innerHTML = "";

    books.forEach(function(book) {

        const li = document.createElement("li");

        li.textContent =
            book.id + ". " +
            book.title + " by " +
            book.author + " (" +
            (book.available ? "Available" : "Borrowed") +
            ")";

        bookList.appendChild(li);
    });
}


//LOAD STUDENTS 
async function loadStudents() {

    const response = await fetch("/students");
    const students = await response.json();

    const studentList = document.getElementById("studentList");

    studentList.innerHTML = "";

    students.forEach(function(student) {

        const li = document.createElement("li");

        li.textContent =
            student.id + ". " +
            student.name + " (" +
            student.email + ")";

        studentList.appendChild(li);
    });
}


// BORROW BOOK
document.getElementById("borrowForm").addEventListener("submit", async function(e) {

    e.preventDefault();

    const studentId =
        document.getElementById("studentId").value;

    const bookId =
        document.getElementById("bookId").value;

    const response = await fetch("/borrow_book", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            student_id: parseInt(studentId),
            book_id: parseInt(bookId)
        })
    });

    const data = await response.json();

    alert(
        data.message +
        "\nDue Date: " +
        data.due_date
    );

    loadBooks();
    loadBorrowed();
});


//RETURN BOOK
document.getElementById("returnForm").addEventListener("submit", async function(e) {

    e.preventDefault();

    const borrowId =
        document.getElementById("borrowId").value;

    const response = await fetch("/return_book", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            borrow_id: parseInt(borrowId)
        })
    });

    const data = await response.json();

    alert(
        data.message +
        "\nFine: ₹" +
        data.fine
    );

    loadBooks();
    loadBorrowed();
});


// LOAD BORROW RECORDS
async function loadBorrowed() {

    const response = await fetch("/borrowed");
    const records = await response.json();

    const borrowList =
        document.getElementById("borrowList");

    borrowList.innerHTML = "";

    records.forEach(function(record) {

        const li = document.createElement("li");

        li.textContent =
            "Borrow ID: " + record.id +
            ", Student: " + record.student_id +
            ", Book: " + record.book_id +
            ", Borrowed: " + record.borrow_date +
            ", Due: " + record.due_date +
            ", Returned: " +
            (record.return_date || "Not yet") +
            ", Fine: ₹" + record.fine;

        borrowList.appendChild(li);
    });
}
loadBooks();
loadStudents();
loadBorrowed();