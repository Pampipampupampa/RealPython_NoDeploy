# -*- coding:Utf8 -*-


import os
import unittest

from views import app, db
from _config import basedir
from models import User


# Database used for testing
TEST_DB = 'test.db'


class AllTests(unittest.TestCase):
    """
        Unit test.
    """

    def setUp(self):
        """
            Executing prior to each tasks.
            Create environnement where tests while be executing.
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """
            Executing after to each tasks.
            Clean environnement.
        """
        db.drop_all()

    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password),
                             follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post('register/', data=dict(name=name, password=password,
                                                    email=email, confirm=confirm),
                             follow_redirects=True)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/',
                             data=dict(name='Go to the bank',
                                       due_date='02/05/2014', priority='1',
                                       posted_date='02/04/2014', status='1'),
                             follow_redirects=True)

# TEST LOGIN PAGE

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sign in to access your tasks list.', response.data)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_users_can_login(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        response = self.login('Jérémy', 'python')
        self.assertIn(b'Welcome ! You were successfully logged in.', response.data)

    def test_invalid_form_data(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

# TEST REGISTER PAGE

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access your tasks list.', response.data)

    def test_user_registeration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    def test_user_registeration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.app.get('register/', follow_redirects=True)
        response = self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.assertIn(b'That username and/or email already exist.', response.data)

# TEST LOGOUT PAGE

    def test_logged_in_users_can_logout(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.login('Jérémy', 'python')
        response = self.logout()
        self.assertIn(b'You were logged out.', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'You were logged out.', response.data)

# TEST TASK PAGE

    def test_logged_in_users_can_access_tasks_page(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.login('Jérémy', 'python')
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    def test_users_can_add_tasks(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.login('Jérémy', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b"New entry was successfully posted, Thanks.", response.data)

    def test_users_cannot_add_tasks_when_error(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.login('Jérémy', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(name='Go to the bank',
                                                   due_date='',
                                                   priority='1',
                                                   posted_date='02/04/2014',
                                                   status='1'),
                                 follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.login('Jérémy', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        # First user have user_id == 1
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b"The task was marked as complete. Well done !", response.data)

    def test_users_can_delete_tasks(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.login('Jérémy', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        # First user have user_id == 1
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b"The task was deleted. Why not add a new one?", response.data)

    # Must failed because any user can delete any task
    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Jérémy', 'mail@monMail.com', 'python')
        self.login('Jérémy', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(b'The task was marked as complete. Well done !', response.data)


# Run all tests
if __name__ == '__main__':
    unittest.main()
