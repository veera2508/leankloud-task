from flask import Blueprint, request
from flask.templating import render_template
from flask_restplus import Api, Resource, fields
import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database="todo_db"
)


api_main = Blueprint('API', __name__)
api = Api(api_main, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'dueby': fields.Date(required=True, description='The task due date'),
    'status': fields.String(required=True, description='The status of the task')
})



class TodoDAO(object):
    def __init__(self):
        self.counter = 0
    
    def addTask(self, task, dueby, status):
        self.counter += 1
        cur = mydb.cursor()
        query = 'insert into todos values (%s, %s, %s, %s)'
        val =  (self.counter, task, dueby, status)
        cur.execute(query, val)
        mydb.commit()
    


    def get(self, id):
        cur = mydb.cursor()
        query = 'select * from todos where id = %s'
        val = (id,)
        cur.execute(query, val)
        res = cur.fetchall()
        if len(res) == 0:
            api.abort(404, "Todo {} doesn't exist".format(id))
        else:
            return {'id': res[0][0], 'task':res[0][1], 'dueby':res[0][2].strftime('%Y-%m-%d'), 'status':res[0][3]}

    def delete(self, id):
        cur = mydb.cursor()
        query = 'delete from todos where id = %s'
        val = (id,)
        cur.execute(query, val)
        mydb.commit()
        if cur.rowcount == 0:
            api.abort(404, "Todo {} doesn't exist".format(id))
    
    def getAll(self):
        cur = mydb.cursor()
        query = 'select * from todos'
        cur.execute(query)
        res = cur.fetchall()
        if len(res) == 0:
            api.abort(404, "No Todo exists".format(id))
        else:
            res = [{'id': res[i][0], 'task':res[i][1], 'dueby':res[0][2].strftime('%Y-%m-%d'), 'status': res[0][3]} for i in range(len(res))]
            return res
    
    def findDue(self, dueby):
        cur = mydb.cursor()
        query = 'select * from todos where dueby = %s and status != %s'
        val = (dueby, "Finished")
        cur.execute(query, val)
        res = cur.fetchall()
        if len(res) == 0:
            api.abort(404, "No todo due")
        else:
            res = [{'id': res[i][0], 'task':res[i][1], 'dueby':res[0][2].strftime('%Y-%m-%d'), 'status': res[0][3]} for i in range(len(res))]
            return res
    
    def overDue(self):
        curdate = datetime.datetime.now().strftime('%Y-%m-%d')
        cur = mydb.cursor()
        query = 'select * from todos where dueby > %s and status != %s'
        val = (curdate, "Finished")
        cur.execute(query, val)
        res = cur.fetchall()
        if len(res) == 0:
            api.abort(404, "No overdue")
        else:
            res = [{'id': res[i][0], 'task':res[i][1], 'dueby':res[0][2].strftime('%Y-%m-%d'), 'status': res[0][3]} for i in range(len(res))]
            return res
    
    def finishedTasks(self):
        cur = mydb.cursor()
        query = 'select * from todos where status = %s'
        val = ("Finished",)
        cur.execute(query, val)
        res = cur.fetchall()
        if len(res) == 0:
            api.abort(404, "No Todo exists")
        else:
            res = [{'id': res[i][0], 'task':res[i][1], 'dueby':res[0][2].strftime('%Y-%m-%d'), 'status': res[0][3]} for i in range(len(res))]
            return res


DAO = TodoDAO()


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        todos = DAO.getAll()
        return todos

    @ns.doc('create_todo')
    @ns.param('task', 'The task to be done')
    @ns.param('status', 'Status of the task (Not Started, In Process, Finished)')
    @ns.param('due_by', "The task's due date")
    def post(self):
        '''Add a new task'''
        task = request.values.get('task')
        status = request.values.get('status')
        due_by = request.values.get('due_by')
        return DAO.addTask(task, due_by, status)


@ns.route('/todo')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self):
        '''Fetch a given task'''
        id = int(request.values.get('id'))
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self):
        '''Delete a task given its identifier'''
        id = int(request.values.get('id'))
        DAO.delete(id)
        return '', 204

@ns.route('/due')
@ns.response(404, 'Todo not found')
@ns.param('due_by', 'The due date')
class Due(Resource):
    @ns.doc('todo_due')
    @ns.marshal_list_with(todo)
    def get(self):
        '''Find a todo with given due date'''
        dueby = request.values.get('due_date')
        return DAO.findDue(dueby)

@ns.route('/overdue')
@ns.response(404, 'Todo not found')
class OverDue(Resource):
    @ns.doc('todo_overdue')
    @ns.marshal_list_with(todo)
    def get(self):
        '''Find all todos which are overdue from current date'''
        return DAO.overDue()

@ns.route('/finished')
@ns.response(404, 'Todo not found')
class Finished(Resource):
    @ns.doc('finished_todo')
    @ns.marshal_list_with(todo)
    def get(self):
        '''Find all todos which are finished'''
        return DAO.finishedTasks()
    



