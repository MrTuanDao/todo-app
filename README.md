folder tree:
```
todo-app/
├── app.py              # Backend logic (sử dụng SQLAlchemy)
├── templates/          # HTML templates
│   └── index.html      # Trang chính (giữ nguyên)
├── static/             # File tĩnh (CSS, JS)
│   └── style.css       # CSS (giữ nguyên)
└── instance/           # Thư mục chứa database SQLite
    └── todo.db         # File cơ sở dữ liệu
```

Version: 1.0.0:
    - Thêm task, xóa task, edit task