import os
from app import app
import unittest
import tempfile

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        '''
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

        app.config['MONGODB_SETTINGS'] = {
            'db': 'testing'
        }
        '''
        #app.config['TESTING'] = True
        self.app = app.test_client()

    #def tearDown(self):
        #db.users.remove()

    def login(self, username, password):
        return self.app.post('/login/signin/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/login/logout/', follow_redirects=True)

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
    '''
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
        print(str(rv.data))
        assert 'Login' in str(rv.data)
        rv2 = self.login('a', 'a')
        assert 'Feed' in str(rv.data)


    def test_login(self):
        print("testing login")
        rv = self.login('a', 'a')
        print(rv)
        assert 'Feed' in str(rv.data)
    '''

if __name__ == '__main__':
    unittest.main()
