import unittest
from app import app
import json


class FlaskAppTestCase(unittest.TestCase):
    """Unit tests for Flask application"""

    def setUp(self):
        """Set up test client before each test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after each test"""
        pass

    # Tests for GET /login
    def test_login_get_returns_200(self):
        """Test that GET /login returns 200 status code"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_get_renders_template(self):
        """Test that GET /login renders the HTML template"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'html', response.data.lower())

    # Tests for POST /login - Success cases
    def test_login_post_with_valid_username(self):
        """Test POST /login with valid username returns success"""
        response = self.client.post('/login', data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello testuser, POST request received', response.data)

    def test_login_post_with_username_with_spaces(self):
        """Test POST /login with username containing spaces"""
        response = self.client.post('/login', data={'username': 'test user'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello test user, POST request received', response.data)

    def test_login_post_with_long_username(self):
        """Test POST /login with long username"""
        long_username = 'a' * 100
        response = self.client.post('/login', data={'username': long_username})
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Hello {long_username}, POST request received'.encode(), response.data)

    # Tests for POST /login - Validation failures
    def test_login_post_without_form_data(self):
        """Test POST /login without any form data returns 400"""
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'No form data provided')

    def test_login_post_without_username_field(self):
        """Test POST /login without username field returns 400"""
        response = self.client.post('/login', data={'other_field': 'value'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Username field is required')

    def test_login_post_with_empty_username(self):
        """Test POST /login with empty username returns 400"""
        response = self.client.post('/login', data={'username': ''})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Username cannot be empty')

    def test_login_post_with_whitespace_only_username(self):
        """Test POST /login with whitespace-only username returns 400"""
        response = self.client.post('/login', data={'username': '   '})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Username cannot be empty')

    def test_login_post_with_tab_only_username(self):
        """Test POST /login with tab-only username returns 400"""
        response = self.client.post('/login', data={'username': '\t\t'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Username cannot be empty')

    # Tests for error handlers
    def test_404_error_handler(self):
        """Test that 404 error handler returns proper JSON response"""
        response = self.client.get('/nonexistent-route')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Resource not found')

    def test_404_error_handler_returns_json(self):
        """Test that 404 error handler returns JSON content type"""
        response = self.client.get('/nonexistent-route')
        self.assertEqual(response.content_type, 'application/json')

    # Tests for different HTTP methods
    def test_login_only_accepts_get_and_post(self):
        """Test that /login only accepts GET and POST methods"""
        # PUT should return 405 Method Not Allowed
        response = self.client.put('/login')
        self.assertEqual(response.status_code, 405)
        
        # DELETE should return 405 Method Not Allowed
        response = self.client.delete('/login')
        self.assertEqual(response.status_code, 405)

    # Edge cases
    def test_login_post_with_special_characters_in_username(self):
        """Test POST /login with special characters in username"""
        special_username = "user@123!#$"
        response = self.client.post('/login', data={'username': special_username})
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Hello {special_username}, POST request received'.encode(), response.data)

    def test_login_post_with_unicode_username(self):
        """Test POST /login with unicode characters in username"""
        unicode_username = "用户测试"
        response = self.client.post('/login', data={'username': unicode_username})
        self.assertEqual(response.status_code, 200)
        self.assertIn('POST request received'.encode(), response.data)


class FlaskAppIntegrationTestCase(unittest.TestCase):
    """Integration tests for Flask application"""

    def setUp(self):
        """Set up test client before each test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_full_login_flow(self):
        """Test complete login flow: GET then POST"""
        # First GET the login page
        get_response = self.client.get('/login')
        self.assertEqual(get_response.status_code, 200)
        
        # Then POST with credentials
        post_response = self.client.post('/login', data={'username': 'integrationuser'})
        self.assertEqual(post_response.status_code, 200)
        self.assertIn(b'Hello integrationuser, POST request received', post_response.data)


if __name__ == '__main__':
    unittest.main()
