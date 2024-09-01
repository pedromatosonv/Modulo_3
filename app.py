from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
tasks = [
    Task(id=1, title='Task 1', description='Description 1'),
    Task(id=2, title='Task 2', description='Description 3'),
    Task(id=3, title='Task 3', description='Description 3'),
]
task_id_control = 1

@app.route("/")
def hello_world():
    return "Hello, world!"

@app.route("/tasks", methods=['POST'])
def create_task():
    global task_id_control

    data = request.get_json()
    new_task = Task(
        id=task_id_control,
        title=data['title'],
        description=data.get('description', ''),
    )
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({ "message": "Nova tarefa criada com sucesso" })

@app.route('/tasks', methods=['GET'])
def list_tasks():
    task_list = [task.to_dict() for task in tasks]

    response = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }

    return jsonify(response)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if (t.id == id):
            return jsonify(t.to_dict())

    return jsonify({ "message": 'No task with given id was found' }), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t

    if not task:
        return jsonify({ "message": 'No task with given id was found' }), 400

    data = request.get_json()

    task.title = data.get('title')
    task.description = data.get('description')
    task.completed = data.get('completed')

    return ''

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for idx, t in enumerate(tasks):
        if (t.id == id):
            tasks.pop(idx)
            return ''

    return jsonify({ "message": "No task with given id was found" }), 400

if __name__ == "__main__":
    app.run(debug=True)