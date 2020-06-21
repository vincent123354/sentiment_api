from flask import Flask, request
from flask import render_template
from flask import redirect, flash
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Float)

    def __init__(self, content):
        self.content = content
        self.done = TextBlob(content).polarity

    def __repr__(self):
        return '<Content {}>'.format(self.content)


db.create_all()


@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if content:
        task = Task(content)
        db.session.add(task)
        db.session.commit()
        return redirect('/')
    else:
        flash('testing')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run()
