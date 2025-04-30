from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Cấu hình database SQLite với đường dẫn tuyệt đối
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo SQLAlchemy
db = SQLAlchemy(app)

# Định nghĩa model Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Tạo database
with app.app_context():
    db.create_all()

# Trang chính
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Thêm task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    if title:
        new_task = Task(title=title, completed=False)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

# Hoàn thành task
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    return redirect(url_for('index'))

# Xóa task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Sửa task
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        title = request.form['title']
        if title:
            task.title = title
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', tasks=Task.query.all(), edit_task=task)

if __name__ == '__main__':
    app.run(debug=True)