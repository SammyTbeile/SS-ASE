import os
from app import app, db
from app.login.models import User
from app.feed_module.models import Listing
import unittest
import tempfile

class ListingTestCase(unittest.TestCase):

    def login(self, username, password):
        return self.app.post('/login/signin/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def setUp(self):
        app.config['TESTING']=True
        app.config['WTF_CSRF_ENABLED']=False
        app.config['MONGODB_SETTINGS']={
            'db': 'testing'
        }
        app.config['LOGIN_DISABLED']=True
        self.app = app.test_client()
        User(username='z', password='a', email='z@gmail.com', phone='z',
            name='z',dorm_building='a', confirm='a').save()

        self.login('a', 'a')


    def tearDown(self):
        User.objects.delete()

    def add_listing(self, title, size, price, info, filename, file):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'myuserid'
                sess['_fresh'] = True # https://flask-login.readthedocs.org/en/latest/#fresh-logins
                sess['logged_in']= True
            return self.app.post('/list', data=dict(
                title=title,
                size=size,
                price=price,
                info=info,
                # files=file
            ), follow_redirects=True)

    def get_feed(self):
        return self.app.get('/feed', follow_redirects=True)

    def test_add_listing_invalid(self):
        print("Testing adding a listing with invalid attributes")
        rv = self.add_listing(
            title='ShirtTest',
            size='M',
            price='10',
            info='wash',
            filename='bad',
            file="nothing"
            )
        assert '401' in str(rv.status)

    def test_add_listing_valid(self):
        print("Testing adding a listing with valid attributes")
        ra = self.login('z','a')
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(APP_ROOT, "app/static")
        filename = 'pic.jpg'
        destination ="/".join([target, filename])
        rv = self.add_listing(
            title='ShirtTest',
            size='M',
            price='10',
            info='wash',
            filename=destination,
            file={'file':open(destination, 'rb')}
            )
        print(rv.data)
        assert '400' in str(rv.status)

    def test_feed_unauthenticated(self):
        print("testing getting the feed while unauthorized")
        rv = self.get_feed()
        assert '401' in str(rv.status)

    def test_feed_authenticated(self):
        print("testing getting the feed while authenticated")
        ra = self.login("z", "a")
        rv = self.get_feed()
        assert '200' in str(rv.status)



if __name__ == '__main__':
    unittest.main()
