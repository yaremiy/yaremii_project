from flask_login import login_user, current_user
from flask_testing import TestCase
from app.account.models import User
from app.task.models import Task, Category
from app import create_app, db

class BaseTest(TestCase):

    def create_app(self):
        return create_app(config_name='test')


    def setUp(self):
        db.create_all()
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)


class UserTest(BaseTest):

    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Portfolio', response.data)


    def test_save_user(self):
        user = User(username='default', email='default@mail.com', password='password')
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email='default@mail.com').first()
        self.assertIsNotNone(user)


    def test_register(self):
        with self.client:
            self.client.post(
                '/register',
                data=dict(username='test', email='default@mail.com', password='password', confirm_password='password'),
                follow_redirects=True
            )
        user = User.query.filter_by(email='default@mail.com').first()
        self.assertIsNotNone(user)


    def test_login(self):
        user = User(username='user', email='default@mail.com', password='password')
        db.session.add(user)
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email='default@mail.com', password='password'),
                follow_redirects=True
            )
        self.assertTrue(current_user.is_authenticated)
        self.assertIn(b'Account info', response.data)


    def test_logout(self):
        login_user(User(username='user', email='default@mail.com', password='password'))
        with self.client:
            response = self.client.get(
                '/logout',
                follow_redirects=True
            )
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b'You have been logged out', response.data)


class TaskTest(BaseTest):

    def test_read(self):
        user = User(username='default', email='default@mail.com', password='password')
        task = Task(title='Default title', description='Default description', owner_id=1)
        db.session.add_all([user, task])
        login_user(User.query.filter_by(id=1).first())
        with self.client:
            response = self.client.get('/tasks/1', follow_redirects=True)
            self.assertIn(b'Default title', response.data)


    def test_create(self):
        user = User(username='default', email='default@mail.com', password='password')
        category = Category(name='Default')
        db.session.add_all([user, category])
        login_user(user)
        data = {
            'title': 'Write flask tests',  
            'description': 'New description', 
            'deadline': '2022-12-15',
            'priority': 'low',
            'progress': 'todo',
            'category': 1
        }
        with self.client:
            response = self.client.post('/tasks/create', data=data, 
                        follow_redirects=True)
            self.assertIn(b'New task created', response.data)
            self.assertIn(b'Write flask tests', response.data)


    def test_update(self):
        user = User(username='default', email='default@mail.com', password='password')
        category = Category(name='Default')
        task = Task(title='Default title', description='Default description', owner_id=1)
        db.session.add_all([user, category, task])
        login_user(User.query.filter_by(id=1).first())
        data = {
            'title': 'Updated title',  
            'description': 'Updated description', 
            'deadline': '2022-12-19',
            'priority': 'medium',
            'progress': 'done',
            'category': 1
        }
        with self.client:
            response = self.client.post('/tasks/1/update', data=data, 
                        follow_redirects=True)
            self.assertIn(b'Task has been updated', response.data)
            self.assertIn(b'Updated title', response.data)


    def test_delete(self):
        user = User(username='default', email='default@mail.com', password='password')
        task = Task(title='Default title', description='Default description', owner_id=1)
        db.session.add_all([user, task])
        login_user(User.query.filter_by(id=1).first())
        with self.client:
            response = self.client.get('/tasks/1/delete', follow_redirects=True)
            self.assertIn(b'Task has been deleted', response.data)
            task = Task.query.filter_by(id=1).first()
            self.assertIsNone(task)
