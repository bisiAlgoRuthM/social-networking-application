from django.test import TestCase

# Create your tests here.
from .models import User  # Replace with your model

class UserTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user('testuser', 'test@example.com', 'password123')
        self.assertEqual(user.username, 'testuser')
        # Add more assertions to test user creation logic