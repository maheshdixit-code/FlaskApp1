from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method =="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('hello_world'))
    allToDo = Todo.query.all()
    return render_template('index.html',allToDo=allToDo)

@app.route('/show')
def product():
    allToDo = Todo.query.all()
    print(allToDo)
    return 'this is product page'

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        ToDo = Todo.query.filter_by(sno=sno).first()
        ToDo.title=title
        ToDo.desc=desc
        db.session.add(ToDo)
        db.session.commit()
        return redirect('/')

    ToDo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',ToDo=ToDo)

@app.route('/delete/<int:sno>')
def delete(sno):
    ToDo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(ToDo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True,port=1234)