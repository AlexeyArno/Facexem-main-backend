import os
from facexem_app import app
import unittest
import tempfile
import json
from facexem_app import extensions
from tests import create_user, delete_user, get_page_info, set_page_info, set_subject, get_lections


class FacexemTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        extensions.db.init_app(app)
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        self.app_context.pop()

    def login(self, email, password):
        data = json.dumps({'email': email, 'pass': password})
        return self.app.post('/api/user/login',
                             data=data,
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/api/user/logout', follow_redirects=False)

    def test_login_logout(self):
        rv = self.login('ledsass@gmail.com', '111111')
        data = json.loads(rv.data)
        assert 'Success' in data['result']
        self.logout()
        rv = self.login('ledsass@gmail.com', '1111')
        data = json.loads(rv.data)
        assert 'Error' in data['result']
        rv = self.logout()
        data = json.loads(rv.data)
        assert 'Error' in data['result']

    def test_create_and_delete_user(self):
        for i in range(10):
            rv = create_user.create_user(self, 'ledss@gmail.com', 'JesusChrist', '11111')
            data = json.loads(rv.data)
            assert 'Success' in data['result']
            rv = set_page_info.set_page_info(self, '12', '23', ['111', '2222', '222'], '23')
            data = json.loads(rv.data)
            assert 'Success' in data['result']
            rv = get_page_info.get_page_info(self, '12', '23', ['111', '2222', '222'], '23')
            assert "Success" == rv
            rv = set_subject.set_subject(self, ['math_pro'])
            data = json.loads(rv.data)
            assert 'Success' in data['result']
            rv = get_lections.get_lections(self, 'math_pro', )
            assert "Success" == rv
            rv = delete_user.delete_user(self)
            data = json.loads(rv.data)
            assert 'Success' in data['result']


if __name__ == '__main__':
    unittest.main()
