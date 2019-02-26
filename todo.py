from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
from flask import redirect, render_template, url_for, request



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////sqlite/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    """if todo.complete == True:
        todo.complete = False

    else:
        todo.complete = True"""

    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add", methods = ["POST"])
def add():
    title = request.form.get("title")
    newTodo = Todo(title= title, complete = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


class Todo(db.Model):
    
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80), unique = True)
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    
    db.create_all()
    app.run(debug=True)