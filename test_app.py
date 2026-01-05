
import pytest
from app import app, db, Expense
from datetime import date

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_create_expense(client):
    """Test creating a new expense."""
    response = client.post('/add', data={
        'title': 'Test Expense',
        'description': 'This is a test expense.',
        'amount': '10.50',
        'category': 'Testing',
        'spent_on': '2024-01-01'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        expense = Expense.query.filter_by(title='Test Expense').first()
        assert expense is not None
        assert expense.description == 'This is a test expense.'
        assert expense.amount == 10.50
        assert expense.category == 'Testing'
        assert expense.spent_on == date(2024, 1, 1)

def test_update_expense(client):
    """Test updating an existing expense."""
    with app.app_context():
        # First, create an expense to update
        expense = Expense(
            title='Original Title',
            description='Original Description',
            amount=20.00,
            category='Original Category',
            spent_on=date(2024, 1, 2)
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    # Now, update the expense
    response = client.post(f'/edit/{expense_id}', data={
        'title': 'Updated Title',
        'description': 'Updated Description',
        'amount': '30.50',
        'category': 'Updated Category',
        'spent_on': '2024-01-03'
    }, follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        updated_expense = db.session.get(Expense, expense_id)
        assert updated_expense.title == 'Updated Title'
        assert updated_expense.description == 'Updated Description'
        assert updated_expense.amount == 30.50
        assert updated_expense.category == 'Updated Category'
        assert updated_expense.spent_on == date(2024, 1, 3)

def test_delete_expense(client):
    """Test deleting an expense."""
    with app.app_context():
        # First, create an expense to delete
        expense = Expense(
            title='Expense to Delete',
            description='This expense will be deleted.',
            amount=50.00,
            category='Deletion',
            spent_on=date(2024, 1, 4)
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    # Now, delete the expense
    response = client.post(f'/delete/{expense_id}', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        deleted_expense = db.session.get(Expense, expense_id)
        assert deleted_expense is None
