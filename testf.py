#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort
from flask import make_response, request
from flask import url_for
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

@app.route('/')
def index():
	return 'hello, world!'

@auth.get_password
def get_password(username):
	if username == 'hhh':
		return 'hhh'
	return None

@app.route('/api/task1', methods=['GET'])
def get_tasks():
	return jsonify({'task_name': index()})

tasks = [
		{'id': '1', 'title': u'buy groceries', 'des': u'milk, pizza'},
		{'id': '2', 'title': u'learn restful', 'des': u'api design'},
		]

@app.route('/api/task/<int:task_id>', methods=['GET'])
def get_taskid(task_id):
	task = filter(lambda x: x['id'] == str(task_id), tasks)
	if len(task) == 0:
		abort(404)
	return jsonify({'get task': task[0]})

@app.route('/api/task/', methods=['POST'])
#@auth.login_required
def create_task():
	print request.json
	if not request.json or not 'title' in request.json:
		abort(400)
	task = {}
	if len(tasks):
		task['id'] = str(int(tasks[-1]['id'])+1)
	else:
		task['id'] = '1'
	task['title'] = request.json['title']
	task['des'] = request.json.get('des', '')
	tasks.append(task)
	return jsonify({'tasklist': tasks}), 201

@app.route('/api/task/<int:task_id>', methods=['PUT'])
#@auth.login_required
def update_task(task_id):
	task = filter(lambda x: x['id'] == str(task_id), tasks)
	if len(task) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'title' in request.json and type(request.json['title']) != unicode:
		abort(400)
	if 'des' in request.json and type(request.json['des']) != unicode:
		abort(400)
	try:
		task[0]['title'] = request.json.get('title', task[0]['title'])
		task[0]['des'] = request.json.get('des', task[0]['des'])
	except:
		abort(304)
	return jsonify({'tasklist': tasks}), 201

@app.route('/api/task/<int:task_id>', methods=['DELETE'])
#@auth.login_required
def delete_task(task_id):
	task = filter(lambda x: x['id'] == str(task_id), tasks)
	if len(task) == 0:
		abort(404)
	tasks.remove(task[0])
	return jsonify({'result': True, 'tasklist': tasks})



def make_access_path(task):
	new_task = {}
	for t in task:
		if t == 'id':
			new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
		else:
			new_task[t] = task[t]
	return new_task

@app.route('/api/tasks', methods=['GET'])
@auth.login_required
def get_task():
	return jsonify({'tasks': map(make_access_path, tasks)})



@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}),403)

@app.errorhandler(304)
def not_changed(error):
	return manke_response(jsonify({'error': 'Not changed as exespecet'}), 304)

@app.errorhandler(400)
def not_useable(error):
	return make_response(jsonify({'error': 'Not accept body format'}),400)

@app.errorhandler(403)
def refuse_access(error):
	return make_response(jsonify({'error': 'Forbidden'}),403)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def not_allowed_method(error):
	return make_response(jsonify({'error': 'Not allowed method'}), 405)

@app.errorhandler(422)
def not_useable(error):
	return make_response(jsonify({'error': 'Unprocessable entity'}),422)

@app.errorhandler(429)
def not_useable(error):
	return make_response(jsonify({'error': 'Too many requests'}),429)

@app.errorhandler(500)
def server_errro(error):
	return make_response(jsonify({'error': 'Internal server error'}),500)

if __name__ == '__main__':
	app.run(debug=True)


