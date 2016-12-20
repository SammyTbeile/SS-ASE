import os
import unittest
from app import app
from app.login.models import User
from app.feed_module.models import Listing
from io import BytesIO
from flask import url_for

class ListingTestCase(unittest.TestCase):

    def login(self, username, password):
        return self.app.post('/login/signin/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['MONGODB_SETTINGS'] = {
            'db': 'testing'
        }
        app.config['LOGIN_DISABLED'] = True
        self.app = app.test_client()
        User(username='tester', password='a', email='test@gmail.com', phone='1234567890',
             name='tester', dorm_building='test', confirm='a').save()

        self.login('tester', 'a')


    def tearDown(self):
        User.objects(username='tester').delete()
        Listing.objects(title='ShirtTest').delete()

    def add_listing(self, title, size, price, info, test_file):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'myuserid'
                sess['_fresh'] = True # https://flask-login.readthedocs.org/en/latest/#fresh-logins
                sess['logged_in'] = True
            return self.app.post('/list', buffered=True,
              content_type='multipart/form-data', data=dict(
                {'file': (test_file, 'test.jpg')},
                title=title,
                size=size,
                price=price,
                info=info

                # filename=filename
            ), follow_redirects=True)

    def add_listing_invalid(self, title, size, price, info):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'myuserid'
                sess['_fresh'] = True # https://flask-login.readthedocs.org/en/latest/#fresh-logins
                sess['logged_in'] = True
            return self.app.post('/list', buffered=True,
              content_type='multipart/form-data', data=dict(
                title=title,
                size=size,
                price=price,
                info=info

                # filename=filename
            ), follow_redirects=True)

    def get_feed(self):
        return self.app.get('/feed', follow_redirects=True)

    # Iteration 1
    def test_add_listing_invalid(self):
        print("Testing adding a listing with invalid attributes")
        rv = self.add_listing_invalid(
            title='ShirtTest',
            size='M',
            price='10',
            info='wash'
            )
        assert '400' in str(rv.status)

    # Iteration 1
    def test_add_listing_valid(self):
        print("Testing adding a listing with valid attributes")
        self.login('tester', 'a')
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(APP_ROOT, "app/static")
        filename = 'pic.jpg'
        destination = "/".join([target, filename])
        with open( destination, "rb") as test:
          BytesFile = BytesIO(test.read())

        rv = self.add_listing(
            title='ShirtTest',
            size='M',
            price='10',
            info='wash',
            test_file=BytesFile
            # file={'file':open(destination, 'rb')}
            )
        assert '400' in str(rv.status)

    # Iteration 1
    def test_feed_unauthenticated(self):
        print("testing getting the feed while unauthorized")
        self.app.get("/login/logout", follow_redirects=True)
        rv = self.get_feed()
        assert '401' in str(rv.status)

    # Iteration 1
    def test_feed_authenticated(self):
        print("testing getting the feed while authenticated")
        self.login("z", "a")
        rv = self.get_feed()
        assert '200' in str(rv.status)

    # Post iteration 1
    def test_get_list(self):
      print("tetsting getting the listing")
      rv = self.app.get("/list", follow_redirects=True)
      assert 'Create a Listing' in str(rv.data)

    # Post iteration 1
    def test_index(self):
      print("testing getting the index")
      rv = self.app.get("/", follow_redirects=True);
      assert 'Rags2Riches' in str(rv.data)

    # Post iteration 1
    def test_get_item(self):
      print("testing getting an item")
      rv = self.app.get("/listing/cufflinks")
      assert 'Contact Seller' in str(rv.data)


if __name__ == '__main__':
    unittest.main()
