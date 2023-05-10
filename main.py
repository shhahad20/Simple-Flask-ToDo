from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# the name of the database; add path if necessary
db_name = 'things_todo.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class To_do(db.Model):
    __tablename__ = 'To_do'
    ID = db.Column(db.Integer, primary_key=True)
    TXT = db.Column(db.String)
    DATE = db.Column(db.String)

with app.app_context():
    db.create_all()


dict = {}


@app.route('/', methods=['POST', 'GET'])
def hello():
    things = db.session.query(To_do).all()
    return render_template('index.html', things=things)



@app.route('/Add', methods=['POST', 'GET'])
def Add():
    if request.method == 'POST':
        thing = request.form['thing']
        date = request.form['date']
        # id = request.form[id]
        dict[thing] = date
        # dict[date] = date
        for key in dict:
            if key == "thing":
                thing = dict[key]
            if key == "date":
                date = dict[key]
        info = To_do(
            TXT=thing,
            DATE=date
        )
        db.session.add(info)
        db.session.commit()
    return redirect(url_for('hello'))


@app.route('/Delete/<int:todo_id>', methods=['POST', 'GET'])
def Delete(todo_id):
        what = To_do.query.filter_by(ID=todo_id).first()
        db.session.delete(what)
        db.session.commit()
        return redirect(url_for('hello'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

