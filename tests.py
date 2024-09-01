import requests

BASE_URL = 'http://127.0.0.1:5000'

tasks = []

def test_create_task():
    new_task_data = {
        "title": "New Task",
        "description": "Task description"
    }

    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)

    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json['id'])

def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")

    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json

def test_get_task():
    task_id = tasks[0]

    response = requests.get(f"{BASE_URL}/tasks/{task_id}")

    assert response.status_code == 200
    response_json = response.json()
    assert task_id == response_json['id']

def test_update_task():
    task_id = tasks[0]
    payload = {
        "title": "New title",
        "description": "New description",
        "completed": True,
    }

    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    response_json = response.json()
    assert response_json['title'] == 'New title'
    assert response_json['description'] == 'New description'
    assert response_json['completed'] is True

def test_delete_task():
    task_id = tasks[0]

    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/tasks")
    response_json = response.json()

    task_deleted = True

    for t in response_json['tasks']:
        if (t.id == task_id):
            task_deleted = False
            break

    assert task_deleted is True