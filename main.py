from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///alltasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    duedate = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
# with app.app_context():
#     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        duedate = request.form['duedate']
        status = request.form['status']
        task = Task(title=title, desc=desc, duedate=duedate, status=status)
        db.session.add(task)
        db.session.commit()
    
    tasklist = Task.query.all() 
    return render_template('index.html', tasklist = tasklist)

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/list")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        task = Task.query.filter_by(id=id).first()
        task.title = title
        task.desc = desc
        db.session.add(task)
        db.session.commit()
        return redirect("/list")
        
    task = Task.query.filter_by(id=id).first()
    return render_template('update.html', task=task)

@app.route('/list/<int:i>', methods=['GET', 'POST'])
def list_all(i):
    tasklist2 = []
    tasklist = Task.query.all() 
    length_task = len(tasklist)
    for t in range((i-1)*3, 3*i):
        if(length_task > t):
            tasklist2.append(tasklist[t])
    return render_template('list.html', tasklist = tasklist, tasklist2 = tasklist2, k=i)

@app.route('/search', methods=['GET', 'POST'])
def search_one():
    flag = 0
    if request.method=='POST':
        id = request.form['id']
        task = Task.query.filter_by(id=id).first()
        flag = 1
        return render_template('index.html', task = task, flag=flag)
    else:
        return render_template('index.html', flag=flag)
    
@app.route('/addtask')
def add_task():
    return render_template('addtask.html')

if __name__ == "__main__":
    app.run(debug=True)