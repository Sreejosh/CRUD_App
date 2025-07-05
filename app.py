from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databse.db" 
# we can ahnge the database ame from our project.db to our wish
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app) # we configured the db


# Data class
class MyTask(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(100),nullable=False)
    complete = db.Column(db.String,default=0)
    create = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) ->str:
        return f"Task {self.id}"

with app.app_context(): # to get the database set up, i mean the folders
        db.create_all()


#Home page
@app.route("/",methods=["POST","GET"])
def hello():
    #Add a task
    if request.method =="POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try: #trying to establish this task into bd
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    #See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.create).all()
        return render_template("index.html",tasks = tasks)


#delete tasks

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error {e}")
        return f"Error: {e}"


#Update the task
@app.route("/update/<int:id>",methods=["POST","GET"])
def update(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method=="POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template("edit.html",task = task)


if __name__ == "__main__":
    app.run(debug=True)