from flask import Flask, render_template, request, redirect, url_for
from database import db
from models import User
app=Flask(__name__, template_folder='templates')


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking

db.init_app(app)

with app.app_context():
    db.create_all()


#todos=[{'task':'sample todo', 'done': False}]



@app.route('/')
def index():
    todos=User.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['todo']
    new_task = User(task=task, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    todo = User.query.get_or_404(id)
    if request.method == "POST":
        todo.task = request.form['todo']
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo, index=index)

@app.route("/check/<int:id>")
def check(id):
    todo = User.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = User.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/preview/<int:id>')
def preview(id):
    todo=User.query.get_or_404(id)
    return render_template('preview.html', todo=todo)



if __name__ == '__main__':
    app.run(debug=True)