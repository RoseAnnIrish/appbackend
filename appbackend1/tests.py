from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import connections


class TodoTests(APITestCase):

    @classmethod
    def tearDownClass(cls):
        """Close database connections after all tests."""
        connections.close_all()  # Close all database connections
        super().tearDownClass()  # Call parent class method

    def create_user(self, username='testuser', password='password123', email='testuser@example.com'):
        """
        Helper method to create and return a user for testing.
        """
        user = User.objects.create_user(username=username, password=password, email=email)
        return user

    def authenticate(self, user):
        """
        Helper method to authenticate the user and return the token.
        """
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return token

    def test_register_user(self):
        """
        Test case for user registration.
        """
        url = reverse('register')  # URL for the registration endpoint
        data = {
            'username': 'user',
            'password': 'mypassword',
            'email': 'user@gmail.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Assert user creation successful

    def test_login_user(self):
        """
        Test case for user login.
        """
        # Register user first
        user = self.create_user(username='UserIrish', password='@IrishPassword', email='userirish@gmail.com')

        # Login with the registered user credentials
        url = reverse('login')  # URL for the login endpoint
        data = {
            'username': 'UserIrish',
            'password': '@IrishPassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Assert login successful

    def test_add_todo(self):
        """
        Test case for adding a new todo.
        """
        # Create and authenticate user
        user = self.create_user(username='testuser', password='password123', email='testuser@example.com')
        self.authenticate(user)

        # Add a new todo
        url = reverse('todo-list')  # URL for adding todo (using the router registered TodoViewSet)
        data = {
            'user': user.id,
            'title': 'New Todo',
            'description': 'This is a description of the new todo.',
            'due_date': '2025-04-01',
            'status': 'pending',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Assert todo is added successfully

    def test_edit_todo(self):
        """
        Test case for editing an existing todo.
        """
        # Create and authenticate user
        user = self.create_user(username='testuser', password='password123', email='testuser@example.com')
        self.authenticate(user)

        # Create a todo first
        url = reverse('todo-list')  # URL for adding todo (using the router registered TodoViewSet)
        todo_data = {
            'user': user.id,
            'title': 'Old Todo',
            'description': 'This is the old todo description.',
            'due_date': '2025-04-01',
            'status': 'pending',
        }
        response = self.client.post(url, todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the ID of the created todo
        todo_id = response.data['id']  # Get the actual todo ID

        # Edit the created todo
        #url = reverse('todo-list') + f"todo/{todo_id}/"  # URL to edit todo, with the correct pattern
        #url = reverse('todo-detail', args=[todo_id])
        data = {
            'user': user.id,
            'title': 'Updated Todo',
            'description': 'Updated description for the todo.',
            'due_date': '2025-05-01',
            'status': 'completed',
        }
        response = self.client.put(f'/api/todo/todo/{todo_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Assert todo is updated successfully

    def test_delete_todo(self):
        """
        Test case for deleting a todo.
        """
        # Create and authenticate user
        user = self.create_user(username='testuser', password='password123', email='testuser@example.com')
        self.authenticate(user)

        # Create a todo first
        url = reverse('todo-list')  # URL for adding todo (using the router registered TodoViewSet)
        todo_data = {
            'user': user.id,
            'title': 'Todo to be deleted',
            'description': 'This todo will be deleted.',
            'due_date': '2025-04-01',
            'status': 'pending',
        }
        response = self.client.post(url, todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the ID of the created todo
        todo_id = response.data['id']  # Get the actual todo ID

        # Now delete the created todo
        #url = reverse('todo-list') + f"todo/{todo_id}/"  # URL to delete todo, with the correct pattern
        response = self.client.delete(f'/api/todo/todo/{todo_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

