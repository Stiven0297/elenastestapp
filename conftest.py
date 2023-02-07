import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from task_app.models import Task


@pytest.fixture
def create_test_user():
    user = User.objects.create_user(
        username='testuser',
        password='secret'
    )
    return user


@pytest.fixture
def get_api_client_authenticated(create_test_user):
    client = APIClient()
    user = create_test_user
    response_client = client.post(
        '/users/api/token/', {
            "username": "testuser",
            "password": "secret"
        }
    )

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {response_client.data['access']}",
    )

    return client, user


@pytest.fixture
def make_tasks(create_test_user):
    def post_tasks_for_test_user():
        task = Task.objects.create(
            user=create_test_user,
            title=mixer.faker.pystr(),
            description=mixer.faker.pystr(),
            completed=False
        )

        return task

    yield post_tasks_for_test_user
