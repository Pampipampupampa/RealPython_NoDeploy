# -*- coding:Utf8 -*-


import os
import unittest

from project import app, db, bcrypt
from project._config import basedir
from project.models import User, Task


# Database used for testing
TEST_DB = 'test.db'


class TasksTests(unittest.TestCase):
    """
        Tasks unit test.
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

    def create_admin_user(self, name='Superman', email='admin@monMail.com',
                          password='allpowerful'):
        new_user = User(name=name, email=email,
                        password=bcrypt.generate_password_hash(password),
                        role='admin')
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/',
                             data=dict(name='Go to the bank',
                                       due_date='02/05/2014', priority='1',
                                       posted_date='02/04/2014', status='1'),
                             follow_redirects=True)

# TEST TASK PAGE AS NORMAL USER

    def test_logged_in_users_can_access_tasks_page(self):
        self.register()
        self.login()
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    def test_users_can_add_tasks(self):
        self.register()
        self.login()
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b"New entry was successfully posted, Thanks.", response.data)

    def test_users_cannot_add_tasks_when_error(self):
        self.register()
        self.login()
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(name='Go to the bank',
                                                   due_date='',
                                                   priority='1',
                                                   posted_date='02/04/2014',
                                                   status='1'),
                                 follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.register()
        self.login()
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        # First user have user_id == 1
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b"The task was marked as complete. Well done !", response.data)

    def test_users_can_delete_tasks(self):
        self.register()
        self.login()
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        # First user have user_id == 1
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b"The task was deleted. Why not add a new one?", response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.login()
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(b'The task was marked as complete. Well done !', response.data)
        self.assertIn(b'You can only update tasks that belong to you.', response.data)

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.login()
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(b'You can only delete tasks that belong to you.', response.data)


# TEST TASK PAGE AS ADMIN
    def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.login()
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(b'You can only update tasks that belong to you.', response.data)

    def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
        self.create_user()
        self.login()
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertNotIn(b'You can only delete tasks that belong to you.', response.data)

    def test_string_representation_of_the_task_object(self):
        from datetime import date
        # Foreign key constraint active by default on my sqlite3 build
        # Need to add first a user before addind a task
        db.session.add(User("Tester", "mail@mail.fr", "python"))
        db.session.add(Task("Test", date(2015, 1, 22), 10, date(2015, 1, 23),
                            1, 1))
        db.session.commit()
        tasks = db.session.query(Task).all()
        for task in tasks:
            self.assertEqual(task.name, 'Test')


# TEST REPR

    def test_task_repr(self):
        from datetime import date
        db.session.add(User("Tester", "mail@mail.fr", "python"))
        db.session.add(Task("Test", date(2015, 1, 22), 10, date(2015, 1, 23),
                            1, 1))
        db.session.commit()
        tasks = db.session.query(Task).all()
        for task in tasks:
            self.assertEqual(repr(task), "<Task Test>")


# TEST USER FEATURES

    def test_task_template_displays_logged_in_user_name(self):
        self.register()
        self.login()
        response = self.app.get('tasks/', follow_redirects=True)
        # Jérémy as binary string (unicode currently not supported)
        self.assertIn(b'J\xc3\xa9r\xc3\xa9my', response.data)


# TEST ACTIONS DISPLAYED

    def test_users_cannot_see_task_modify_links_for_tasks_not_created_by_them(self):
        self.register()
        self.login()
        self.app.get("tasks/", follow_redirects=True)
        self.create_task()
        self.logout()
        self.register(name='Escroc', email='mail2@monMail.com',
                      password='python')
        self.login(name='Escroc', password='python')
        response = self.app.get("tasks/", follow_redirects=True)
        self.assertNotIn(b'Mark as complete', response.data)
        self.assertNotIn(b'Delete', response.data)

    def test_users_can_see_task_modify_links_for_tasks_created_by_them(self):
        self.register()
        self.login()
        self.app.get("tasks/", follow_redirects=True)
        self.create_task()
        self.logout()
        self.register(name='Escroc', email='mail2@monMail.com',
                      password='python')
        self.login(name='Escroc', password='python')
        self.app.get("tasks/", follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)

    def test_admin_users_can_see_task_modify_links_for_all_tasks(self):
        self.register()
        self.login()
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'complete/1/', response.data)
        self.assertIn(b'delete/1/', response.data)
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)

# Run all tests
if __name__ == '__main__':
    unittest.main()
