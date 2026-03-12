from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table
conn = get_db_connection()
conn.execute('''
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY,
name TEXT,
age INTEGER,
course TEXT,
grade TEXT
)
''')
conn.commit()
conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)


@app.route('/add', methods=('GET','POST'))
def add():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        grade = request.form['grade']

        conn = get_db_connection()
        conn.execute(
        'INSERT INTO students (name,age,course,grade) VALUES (?,?,?,?)',
        (name,age,course,grade))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete(id):

    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id=?',(id,))
    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/update/<int:id>', methods=('GET','POST'))
def update(id):

    conn = get_db_connection()
    student = conn.execute(
    'SELECT * FROM students WHERE id=?',(id,)
    ).fetchone()

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        grade = request.form['grade']

        conn.execute(
        'UPDATE students SET name=?,age=?,course=?,grade=? WHERE id=?',
        (name,age,course,grade,id)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    conn.close()

    return render_template('update.html', student=student)


app.run(debug=True)