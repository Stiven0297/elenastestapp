import pytest

from task_app.models import Task


@pytest.mark.django_db(transaction=True)
class TestTaskViewCase:

    def test_save_task_view(self, get_api_client_authenticated):
        client, user = get_api_client_authenticated

        response = client.post(
            '/api/tasks/', {
                'title': 'Tarea de prueba 3 admin2',
                'description': 'Esta es una descripcion de tarea de 3 admin2',
                'completed': False
            }
        )

        assert response.status_code == 201
        assert response.data['title'] == "Tarea de prueba 3 admin2"

    def test_get_all_tasks_view(
        self,
        get_api_client_authenticated,
        make_tasks
    ):
        client, user = get_api_client_authenticated

        task = make_tasks()

        response = client.get('/api/tasks/')

        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_get_fake_task_view(
        self,
        get_api_client_authenticated,
        make_tasks
    ):
        client, user = get_api_client_authenticated

        task = make_tasks()

        response = client.get(f'/api/tasks/99/')

        assert response.status_code == 404
        assert response.data['detail'] == "Not found."

    def test_update_tasks_view(
        self,
        get_api_client_authenticated,
        make_tasks
    ):
        client, user = get_api_client_authenticated

        task = make_tasks()

        client.patch(
            f'/api/tasks/{task.id}/', {
                'completed': True
            }
        )

        response = client.get(f'/api/tasks/{task.id}/')

        assert response.status_code == 200
        assert response.data['completed'] is True

    def test_delete_task_view(
        self,
        get_api_client_authenticated,
        make_tasks
    ):
        client, user = get_api_client_authenticated

        task = make_tasks()

        client.delete(f'/api/tasks/{task.id}/')

        deleted_task = Task.objects.filter(id=task.id)

        response = client.get(f'/api/tasks/{task.id}/')

        assert response.status_code == 404
        assert response.data['detail'] == "Not found."
        assert len(deleted_task) == 0

    def test_invalid_page_task_view(
        self,
        get_api_client_authenticated,
        make_tasks
    ):
        client, user = get_api_client_authenticated

        task = make_tasks()

        response = client.get('/api/tasks/?page=2')

        assert response.status_code == 404
        assert response.data['detail'] == "Invalid page."


    def test_page_task_view(
        self,
        get_api_client_authenticated,
        make_tasks
    ):
        client, user = get_api_client_authenticated

        make_tasks()
        make_tasks()
        make_tasks()
        make_tasks()
        make_tasks()
        make_tasks()
        make_tasks()
        make_tasks()
        make_tasks()
        make_tasks()

        response = client.get('/api/tasks/?page=1')

        assert response.status_code == 200
        assert len(response.data['results']) == 5




