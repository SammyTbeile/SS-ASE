import unittest
from app import app
from app.login.models import User


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['MONGODB_SETTINGS'] = {
            'db': 'testing'
        }
        self.app = app.test_client()

    def tearDown(self):
        User.objects(username='tester').delete()


    def login(self, username, password):
        return self.app.post('/login/signin/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/login/logout', follow_redirects=True)

    def register(self, username, name, email, phone, dorm_building,
                 password, confirm):
        return self.app.post('/login/register/', data=dict(
            username=username,
            name=name,
            email=email,
            phone=phone,
            dorm_building=dorm_building,
            password=password,
            confirm=confirm
        ), follow_redirects=True)

    def test_login_failure(self):
        print("testing that failed login returns the login page")
        rv = self.login('wrong', 'test')
        assert 'Login' in str(rv.data)

    def test_register(self):
        print("testing registration")
        rv = self.register(
            'tester',
            'test name',
            'a@gmail.com',
            '1234567890',
            'test building',
            'a',
            'a')
        assert 'Login' in str(rv.data)

    def test_double_register(self):
        print("testing double registration")
        self.register(
            'tester',
            'test name',
            'a@gmail.com',
            '1234567890',
            'test building',
            'a',
            'a')
        rv = self.register(
          'tester',
          'test name',
          'a@gmail.com',
          '1234567890',
          'test building',
          'a',
          'a')
        assert 'Username is not unique' in str(rv.data)

    def test_invalid_registration(self):
        print("testing invalid registration")
        rv = self.register(
          'tester',
          'test name',
          'not an email',
          '123don\'tcall',
          'test building',
          'a',
          'b')
        assert 'Invalid registration' in str(rv.data)


    def test_login(self):
        print("testing login")
        User(username='tester', password='a', email='a@gmail.com',
             phone='1234567890', name='a', dorm_building='a',
             confirm='a').save()
        rv = self.login('tester', 'a')
        assert 'Feed' in str(rv.data)

    def test_logout(self):
        print("test logout")
        rv = self.logout()
        assert 'Login' in str(rv.data)

    def test_is_authenticated(self):
        print("test is_authenticated")
        user = User(username='tester', password='a', email='a@gmail.com',
             phone='1234567890', name='a', dorm_building='a',
             confirm='a').save()
        result = user.is_authenticated()
        assert (result == True)

    def test_is_active(self):
      print("test is_active")
      user = User(username='tester', password='a', email='a@gmail.com',
           phone='1234567890', name='a', dorm_building='a',
           confirm='a').save()
      assert (user.is_active() == True)

    def test_is_anonymous(self):
      print("test is_anonymous")
      user = User(username='tester', password='a', email='a@gmail.com',
           phone='1234567890', name='a', dorm_building='a',
           confirm='a').save()
      assert (user.is_anonymous() == False)



if __name__ == '__main__':
    unittest.main()
