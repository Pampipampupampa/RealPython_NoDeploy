# -*- coding:Utf8 -*-


import os
import unittest

from project import app, db, bcrypt
from project._config import basedir
from project.models import User


# Database used for testing
TEST_DB = 'test.db'


class AllTests(unittest.TestCase):
    """
        Users unit test.
    """

# USEFUL FUNCTIONS

    def setUp(self):
        """
            Executing prior to each tasks.
            Create environnement where tests while be executing.
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    def tearDown(self):
        """
            Executing after each task.
            Clean environnement.
        """
        db.drop_all()

    def login(self, name='Jérémy', password='python'):
        return self.app.post('/', data=dict(name=name, password=password),
                             follow_redirects=True)

    def register(self, name='Jérémy', email='mail@monMail.com',
                 password='python', confirm='python'):
        return self.app.post('register/', data=dict(name=name, password=password,
                                                    email=email, confirm=confirm),
                             follow_redirects=True)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_user(self, name='Jérémy', email='mail@monMail.com',
                    password='python'):
        new_user = User(name=name, email=email,
                        password=bcrypt.generate_password_hash(password))
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
        response = self.login()
        self.assertIn(b'Invalid username or password.', response.data)

    def test_users_can_login(self):
        self.register()
        response = self.login()
        self.assertIn(b'Welcome ! You were successfully logged in.', response.data)

    def test_invalid_form_data(self):
        self.register()
        response = self.login('not me', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

# TEST REGISTER PAGE

    def test_users_can_register(self):
        new_user = User('Jérémy', 'mail@monMail.com', "python")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "Jérémy"

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access your tasks list.', response.data)

    def test_user_registeration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register()
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    def test_user_registeration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register()
        self.app.get('register/', follow_redirects=True)
        response = self.register()
        self.assertIn(b'That username and/or email already exist.', response.data)

    def test_duplicate_user_registeration_throws_error(self):
        self.register()
        response = self.register()
        self.assertIn(b'That username and/or email already exist.', response.data)

    def test_user_login_field_errors(self):
            # name empty
            response = self.app.post('/', data=dict(name='', password='python101'),
                                     follow_redirects=True)
            self.assertIn(b'This field is required.', response.data)
            # password empty
            response = self.app.post('/', data=dict(name='Jérémy', password=''),
                                     follow_redirects=True)
            self.assertIn(b'This field is required.', response.data)

    def test_string_reprsentation_of_the_user_object(self):
        db.session.add(User('Jérémy', 'mail@monMail.com', 'python'))
        db.session.commit()
        users = db.session.query(User).all()
        for user in users:
            self.assertEqual(user.name, 'Jérémy')

    def test_default_user_role(self):
        db.session.add(User('Jérémy', 'mail@monMail.com', 'python'))
        db.session.commit()
        users = db.session.query(User).all()
        for user in users:
            self.assertEqual(user.role, 'user')


# TEST LOGOUT PAGE

    def test_logged_in_users_can_logout(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        self.login('Jérémy', 'python')
        response = self.logout()
        self.assertIn(b'You were logged out.', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'You were logged out.', response.data)


# TEST REPR

    def test_user_repr(self):
        self.register('Jérémy', 'mail@monMail.com', 'python', 'python')
        db.session.commit()
        users = db.session.query(User).all()
        for user in users:
            self.assertEqual(repr(user), "<User Jérémy>")


# Run all tests
if __name__ == '__main__':
    unittest.main()
