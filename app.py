
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timezone
from sqlalchemy import func

# Get the absolute path of the directory where the script is running
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for flash messages
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    spent_on = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Expense {self.title}>'

@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

@app.route('/api/expenses')
def api_expenses():
    expenses = db.session.query(
        Expense.category,
        func.sum(Expense.amount).label('total_amount')
    ).group_by(Expense.category).all()
    
    expense_data = [{'category': category, 'total_amount': total_amount} for category, total_amount in expenses]
    
    return jsonify(expense_data)

@app.route('/add', methods=['POST'])
def add_expense():
    title = request.form['title']
    description = request.form['description']
    amount = request.form['amount']
    category = request.form['category']
    spent_on_str = request.form['spent_on']
    spent_on = datetime.strptime(spent_on_str, '%Y-%m-%d').date()
    
    new_expense = Expense(title=title, description=description, amount=amount, category=category, spent_on=spent_on)
    db.session.add(new_expense)
    db.session.commit()
    flash('Expense added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = db.get_or_404(Expense, id)

    if request.method == 'POST':
        expense.title = request.form['title']
        expense.description = request.form['description']
        expense.amount = request.form['amount']
        expense.category = request.form['category']
        spent_on_str = request.form['spent_on']
        expense.spent_on = datetime.strptime(spent_on_str, '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', expense=expense)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = db.get_or_404(Expense, id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'danger')
    return redirect(url_for('index'))

# Function to initialize the database
def init_db():
    with app.app_context():
        db.create_all()

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
    # app.run(debug=True)
