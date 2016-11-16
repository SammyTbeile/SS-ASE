
import os
from app import app, db
from app.login.models import User
import unittest
import tempfile

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING']=True
        app.config['WTF_CSRF_ENABLED']=False
        app.config['MONGODB_SETTINGS']={
            'db': 'testing'
        }
        self.app = app.test_client()
    def tearDown(self):
        User.objects().delete()

    def login(self, username, password):
        return self.app.post('/login/signin/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/login/logout', follow_redirects=True)

    def register(self, username, name, email, dorm_building,
        phone, password, confirm):
        return self.app.post('/login/register/', data=dict(
            username=username,
            name=name,
            email=email,
            dorm_building=dorm_building,
            password=password,
            confirm=confirm
        ), follow_redirects=True)

    def test_login_failure(self):
        print("testing that failed login returns the login page")
        rv = self.login('test', 'test')
        assert 'Login' in str(rv.data)

    def test_register(self):
        print("testing registration")
        rv = self.register(
            'a',
            'a',
            'a@gmail.com',
            'a',
            'a',
            'a',
            'a')
        assert 'Login' in str(rv.data)


    def test_login(self):
        print("testing login")
        User(username='a', password='a', email='a@gmail.com', phone='a', name='a',dorm_building='a', confirm='a').save()
        rv = self.login('a', 'a')
        assert 'Feed' in str(rv.data)

    def test_logout(self):
        print("test logout")
        rv = self.logout()
        assert 'Login' in str(rv.data)



if __name__ == '__main__':
    unittest.main()
