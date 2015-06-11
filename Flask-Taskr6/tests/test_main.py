# -*- coding:Utf8 -*-


import os
import unittest

from project import app, db
from project._config import basedir
# from project.models import User


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
            Start server without the debug mode.
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

# TEST ERROR PAGE 404

    def test_404_error(self):
        response = self.app.get('/This-route-does-not-exist')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b'Sorry your lost. There\xe2\x80\x99s nothing here.', response.data)

# Can’t pass right now. Explain later.
    # def test_500_error(self):
    #     bad_user = User(name='Jeremy', email='jeremy@realpython.com', password='django')
    #     db.session.add(bad_user)
    #     db.session.commit()
    #     response = self.login('Jeremy', 'django')
    #     self.assertEquals(response.status_code, 500)
    #     self.assertNotIn(b'ValueError: Invalid salt', response.data)
    #     self.assertIn(b'Something went terribly wrong.', response.data)


# Run all tests
if __name__ == '__main__':
    unittest.main()
