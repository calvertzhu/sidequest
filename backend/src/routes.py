from flask import Blueprint, request, jsonify
from db import tasks_collection
from bson import ObjectId

api = Blueprint('api', __name__)

@api.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(tasks_collection.find())
    for task in tasks:
        task['_id'] = str(task['_id'])
    return jsonify(tasks)

@api.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    result = tasks_collection.insert_one({'task': data['task']})
    return jsonify({'_id': str(result.inserted_id)})

@api.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    tasks_collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Deleted'})
