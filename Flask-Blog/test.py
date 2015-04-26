# -*- coding:Utf8 -*-

"""
    Flask blog controller unit test.
"""

from blog import app
import unittest


########################
#    Main Program :    #
########################


class FlaskTestCase(unittest.TestCase):
    """
        Run some test to ensure this web site works well
    """
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_load(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertIn(b"Please login to access your blog.", response.data)

    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(username="admin", password="admin"),
                               follow_redirects=True)
        self.assertIn(b"You were successfully logged in.", response.data)

    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(username="inconnu", password="inconnu"),
                               follow_redirects=True)
        self.assertIn(b"Invalid Credentials. Please try again.", response.data)

    def test_logout(self):
        tester = app.test_client(self)
        tester.post('/', data=dict(username="inconnu", password="inconnu"),
                    follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True, content_type='html/text')
        self.assertIn(b"You were logged out.", response.data)

    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/main', follow_redirects=True, content_type='html/text')
        self.assertIn(b"You need to login first.", response.data)

    def test_post_show_up(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(username="admin", password="admin"),
                               follow_redirects=True)
        self.assertIn(b"I&#39;m well.", response.data)


if __name__ == '__main__':
    unittest.main()
