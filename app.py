import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Cấu hình database SQLite với đường dẫn tuyệt đối
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo SQLAlchemy
db = SQLAlchemy(app)

# Khởi tạo Flask-Migrate
migrate = Migrate(app, db)

# Định nghĩa model Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Thêm cột created_at

# Trang chính
@app.route('/')
def index():
    filter_status = request.args.get('filter', 'all')
    sort = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')

    # Xây dựng truy vấn
    query = Task.query
    if filter_status == 'completed':
        query = query.filter_by(completed=True)
    elif filter_status == 'incomplete':
        query = query.filter_by(completed=False)

    # Xử lý sắp xếp
    if sort == 'created_at':
        query = query.order_by(Task.created_at.desc() if order == 'desc' else Task.created_at.asc())

    tasks = query.all()
    return render_template('index.html', tasks=tasks, filter_status=filter_status, sort=sort, order=order)

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
    return render_template('index.html', tasks=Task.query.all(), edit_task=task, filter_status='all', sort='created_at', order='desc')

if __name__ == '__main__':
    app.run(debug=True)