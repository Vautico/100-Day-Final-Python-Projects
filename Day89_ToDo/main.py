from flask import Flask, redirect, render_template, request, url_for


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(30), default="Not started")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    due_date: Mapped[str] = mapped_column(String(20), default="")
    notes: Mapped[str] = mapped_column(String(500), default="")

    @property
    def progress_percent(self):
        return clamp_progress(self.progress)

    @property
    def progress_color(self):
        if self.progress_percent < 34:
            return "#dc3545"
        if self.progress_percent < 67:
            return "#ffc107"
        return "#198754"


def clamp_progress(value):
    try:
        progress = int(value)
    except (TypeError, ValueError):
        return 0

    return max(0, min(progress, 100))


def task_from_form(task=None):
    if task is None:
        task = Task()

    task.name = request.form.get("task", "").strip()
    task.status = request.form.get("status", "Not started")
    task.progress = clamp_progress(request.form.get("progress"))
    task.due_date = request.form.get("due_date", "").strip()
    task.notes = request.form.get("notes", "").strip()
    return task

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    tasks = db.session.execute(db.select(Task).order_by(Task.id.desc())).scalars().all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=["POST"])
def create_task():
    task = task_from_form()

    if task.name:
        db.session.add(task)
        db.session.commit()

    return redirect(url_for("home"))


@app.route('/update/<int:task_id>', methods=["POST"])
def update_task(task_id):
    task = db.get_or_404(Task, task_id)
    task_from_form(task)

    if task.name:
        db.session.commit()
    else:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for("home"))


@app.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
