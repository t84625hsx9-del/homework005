from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Подключение к PostgreSQL (данные берем из окружения)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_note = Note(content=request.form['content'])
        db.session.add(new_note)
        db.session.commit()
        return redirect('/')
    
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

if __name__ == "__main__":
    app.run()