from flask import Flask, render_template, request
import datetime
import os
import serialization_utils
from date_utils import Date
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key_here'
users = {
    'admin': 'password123',
    'user1': 'mypassword',
    'anu':'2004',
}

students = [
    {'id': '4432', 'name': 'puji', 'class': 'ds', 'books_issued': 0, 'issue_date': '00-00-0', 'return_date': '00-00-0', 'fine': 0},
    {'id': '4335', 'name': 'anusha', 'class': 'ds', 'books_issued': 0, 'issue_date': '00-00-0', 'return_date': '00-00-0', 'fine': 0}
]

books = [
    {'id': '2000', 'title': 'Book One', 'author': 'Author One', 'available': True},
    {'id': '1002', 'title': 'Book Two', 'author': 'Author Two', 'available': True}
]


class Student:
    def __init__(self, name="", enroll_no="", cls="", books_issued=0, date_of_issue="", date_of_return=""):
        self.name = name
        self.enroll_no = enroll_no
        self.cls = cls
        self.books_issued = books_issued
        self.date_of_issue = date_of_issue
        self.date_of_return = date_of_return

    def create(self):
        self.name = request.form.get("name")
        self.enroll_no = request.form.get("enroll_no")
        self.cls = request.form.get("class")
        self.books_issued = int(request.form.get("books_issued", 0))
        self.date_of_issue = request.form.get("date_of_issue")
        self.date_of_return = request.form.get("date_of_return")

    def display(self):
        return f"""
        <div class="student">
            <h3>Student name: {self.name}</h3>
            <p>Student roll number: {self.enroll_no}</p>
            <p>Class: {self.cls}</p>
            <p>No of books issued: {self.books_issued}</p>
            <p>Date of issue: {self.date_of_issue}</p>
            <p>Date of return: {self.date_of_return}</p>
        </div>
        """

    def to_dict(self):
        return {
            'name': self.name,
            'enroll_no': self.enroll_no,
            'class': self.cls,
            'books_issued': self.books_issued,
            'date_of_issue': self.date_of_issue,
            'date_of_return': self.date_of_return
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get('name', ""),
            enroll_no=data.get('enroll_no', ""),
            cls=data.get('class', ""),
            books_issued=data.get('books_issued', 0),
            date_of_issue=data.get('date_of_issue', ""),
            date_of_return=data.get('date_of_return', "")
        )
    
    def f_fine(self):
        return f"<p>Fine to be paid: {self.fine}</p>"

    def doi(self):
        today = datetime.date.today()
        self.doi.day = today.day
        self.doi.month = today.month
        self.doi.year = today.year

    def dor(self):
        today = datetime.date.today()
        self.dor.day = today.day
        self.dor.month = today.month
        self.dor.year = today.year

    def get_nob(self):
        self.nob += 1

    def set_nob(self):
        self.nob -= 1

    def ret_roll(self):
        return self.enroll_no

    def return_book(self, book_name, return_date):
        for issued_book in self.books_issued:
            if issued_book["book_name"] == book_name:
                issued_book["return_date"] = return_date
                break

    def calc_fine(self):
        issue_date = datetime.date(self.doi.year, self.doi.month, self.doi.day)
        return_date = datetime.date(self.dor.year, self.dor.month, self.dor.day)
        delta = (return_date - issue_date).days
        if delta > 10:
            self.fine = (delta - 10) * 5


    def issue_book(self, book_name, issue_date):
        self.books_issued.append({"book_name": book_name, "issue_date": issue_date})

    def get_books_issued(self):
        return self.books_issued


class Book:
    def __init__(self):
        self.qty = 0
        self.total_books = 0
        self.name = ""
        self.author = ""
        self.price = 0.0
        self.bno = 0

    def get_qty(self):
        self.qty += 1

    def set_qty(self):
        self.qty -= 1

    def create(self):
        self.name = request.form.get("name")
        self.bno = int(request.form.get("bno"))
        self.price = float(request.form.get("price"))
        self.author = request.form.get("author")
        self.qty = int(request.form.get("qty"))
        self.calc_tot(self.qty)

    def display(self):
        return f"""
        <div class="book">
            <h3>Book name: {self.name}</h3>
            <p>Book number: {self.bno}</p>
            <p>Author name: {self.author}</p>
            <p>Book quantity: {self.qty}</p>
            <p>Book price: {self.price}</p>
        </div>
        """

    def calc_tot(self, x):
        self.total_books += x

    def tot_book(self):
        return f"<p>Available books in the library: {self.total_books}</p>"

    def ret_bno(self):
        return self.bno

    def set_price(self, x):
        self.price = x

    def to_dict(self):
        return {
            'qty': self.qty,
            'total_books': self.total_books,
            'name': self.name,
            'author': self.author,
            'price': self.price,
            'bno': self.bno
        }

    @classmethod
    def from_dict(cls, data):
        book = cls()
        book.qty = data['qty']
        book.total_books = data['total_books']
        book.name = data['name']
        book.author = data['author']
        book.price = data['price']
        book.bno = data['bno']
        return book

class LibraryManagementSystem:
    def __init__(self):
        self.student_file = 'students.dat'
        self.book_file = 'books.dat'

    def save_data(self, filename, data):
        serialized_data = [item.to_dict() if isinstance(item, (Student, Book)) else item for item in data]
        serialization_utils.save(filename, serialized_data)

    def load_data(self, filename):
        if os.path.exists(filename):
            data = serialization_utils.load(filename)
            objects = []
            for item in data:
                if isinstance(item, dict):
                    if 'enroll_no' in item:
                        objects.append(Student.from_dict(item))
                    elif 'bno' in item:
                        objects.append(Book.from_dict(item))
                else:
                    objects.append(item)
            return objects
        return []
    def search_student(self):
        enroll_no = int(request.form.get("enroll_no"))
        students = self.load_data(self.student_file)
        for student in students:
            if student.ret_roll() == enroll_no:
                return student.display()
        return "Student record not found"

    def modify_student(self, enroll_no, updated_data):
        students = self.load_data(self.student_file)
        for student in students:
            if student.ret_roll() == enroll_no:
                student.name = updated_data['name']
                student.cls = updated_data['class']
                student.books_issued = updated_data['books_issued']
                student.date_of_issue = updated_data['date_of_issue']
                student.date_of_return = updated_data['date_of_return']
                break
        self.save_data(self.student_file, students)
        return "Record updated!"
    def delete_student(self, enroll_no):
        students = self.load_data(self.student_file)
        students = [student for student in students if student.ret_roll() != enroll_no]
        self.save_data(self.student_file, students)
        return "Record deleted!"

    def add_student(self):
        student = Student()
        student.create()
        students = self.load_data(self.student_file)
        students.append(student)
        self.save_data(self.student_file, students)
        return "Student record added."
    
    def display_all_students(self):
        students_data = self.load_data(self.student_file)
        return students_data


    def search_book(self):
        book_no = int(request.form.get("bno"))
        books = self.load_data(self.book_file)
        for book in books:
            if book.ret_bno() == book_no:
                return book.display()
        return "Book not found"

    def modify_book(self):
        books = self.load_data(self.book_file)
        # Modify the book data as needed
        self.save_data(self.book_file, books)

    def delete_book(self):
        book_no = int(request.form.get("bno"))
        books = self.load_data(self.book_file)
        books = [book for book in books if book.ret_bno() != book_no]
        self.save_data(self.book_file, books)
        return "Record deleted!"

    def add_book(self):
        book = Book()
        book.create()
        books = self.load_data(self.book_file)
        books.append(book)
        self.save_data(self.book_file, books)
        return "Book record added."
    
    def display_all_books(self):
        books = self.load_data(self.book_file)
        return [book.display() for book in books]

    def issue_book(self):
        enroll_no = int(input("Enter student number: "))
        students = self.load_data(self.student_file)
        for student in students:
            if student.ret_roll() == enroll_no:
                student.set_doi()
                student.increment_nob()
                book = self.search_book()
                if book:
                    book.set_qty()
                    student.issue_book(book.name, student.doi)  # Record issued book and date
                    self.save_data(self.student_file, students)
                    self.save_data(self.book_file, self.load_data(self.book_file))
                    print("Book issued")
                    return
        print("Student not found")

    def return_book(self):
        enroll_no = int(request.form.get("enroll_no"))
        students = self.load_data(self.student_file)
        for student in students:
            if student.ret_roll() == enroll_no:
                student.dor()
                student.calc_fine()
                student.set_nob()
                self.save_data(self.student_file, students)
                book = self.search_book()
                if book:
                    book.get_qty()
                    self.save_data(self.book_file, self.load_data(self.book_file))
                    return f"Book returned\nFine to be paid: {student.f_fine()}"
        return "Student not found"

library_system = LibraryManagementSystem()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return render_template('homepage.html')
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

@app.route('/admin_menu')
def admin_menu():
    return render_template('admin_menu.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        result = library_system.add_student()
        return render_template('result.html', result=result)
    return render_template('add_student.html')

@app.route('/search_student', methods=['POST'])
def search_student():
    result = library_system.search_student()
    return render_template('result.html', result=result)


@app.route('/modify_student', methods=['GET', 'POST'])
def modify_student():
    if request.method == 'POST':
        print(request.form)  # Print all incoming form data
        enroll_no = request.form['enroll_no']
        updated_data = {
            'name': request.form['name'],
            'class': request.form['class'],
            'books_issued': int(request.form['books_issued']),
            'date_of_issue': request.form['date_of_issue'],
            'date_of_return': request.form['date_of_return']
        }
        result = library_system.modify_student(enroll_no, updated_data)
        return render_template('result.html', result=result)
    return render_template('modify_student.html')



@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    if request.method == 'POST':
        enroll_no = request.form['enroll_no']
        result = library_system.delete_student(enroll_no)
        return render_template('result.html', result=result)
    return render_template('delete_student.html')

@app.route('/add_book_form', methods=['GET'])
def add_book_form():
    return render_template('add_book_form.html')

@app.route('/add_book', methods=['POST'])
def add_book():
    result = library_system.add_book()
    return render_template('result.html', result=result)

@app.route('/display_all_books')
def display_all_books():
    books = library_system.display_all_books()
    return render_template('display_all_books.html', items=books, title="Books")
@app.route('/display_all_students')
def display_all_students():
    students = library_system.display_all_students()
    return render_template('display_all_students.html', students=students)

@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    if request.method == 'POST':
        book_info = library_system.search_book()
        return render_template('search_book_result.html', book_info=book_info)
    return render_template('search_book.html')

@app.route('/modify_book_form', methods=['GET'])
def modify_book_form():
    return render_template('modify_book_form.html')

@app.route('/modify_book', methods=['POST'])
def modify_book():
    result = library_system.modify_book()
    return render_template('result.html', result=result)

@app.route('/delete_book_form', methods=['GET'])
def delete_book_form():
    return render_template('delete_book_form.html')

@app.route('/delete_book', methods=['POST'])
def delete_book():
    result = library_system.delete_book()
    return render_template('result.html', result=result)

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        student_id = request.form['student_id']
        book_no = request.form['book_no']
        issue_date = request.form['issue_date']
        return_date = request.form['return_date']
        
        student_found = False
        for student in students:
            if student['id'] == student_id:
                student['book_issued'] = book_no
                student['issue_date'] = issue_date
                student['return_date'] = return_date
                student['books_issued'] += 1
                student_found = True
                break
        
        if student_found:
            return render_template('issue_book_result.html', result="Book issued Successfully")
    else:
        return render_template('issue_book_form.html')
    
@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        student_id = request.form['student_id']
        for student in students:
            if student['id'] == student_id:
                student['book_issued'] = None
                student['issue_date'] = None
                student['return_date'] = None
                break
            return render_template('display_all_students.html')
        return render_template('return_book_result.html', result="Book returned successfully")

    else:
        return render_template('return_book_form.html')

if __name__ == "__main__":
    app.run(debug=True)
