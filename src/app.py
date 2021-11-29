from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import jsonpickle
from sqlalchemy import text
import sqlalchemy
import requests
from sqlalchemy.orm import session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Floreria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

connection = db.session.connection()

def obtenerJson(tabla):
    column_names = (list)(tabla.keys())
    results = []
    for row in tabla:
        iterador = 0
        data = {}
        for elemento in column_names:
            data[column_names[iterador]] = row[iterador]
            iterador = iterador + 1
        results = results + [
            data
        ]
    #result_dict = {'results': results}
    return jsonify(results)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Bienvenido a mi API'})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    all_tasks = connection.execute('SELECT * FROM Usuarios')

    return obtenerJson(all_tasks)

@app.route('/api/login', methods=['POST'])
def login():
    correo = request.json['correo']
    contrasena = request.json['contrasena']
    user = connection.execute("CALL LOGIN('" + correo +"', '" + contrasena + "')")

    return obtenerJson(user)

@app.route('/api/seachProducts', methods=['POST'])
def products():
    product = connection.execute("SELECT * FROM Productos")

    return obtenerJson(product)

@app.route('/api/insertUser', methods=['POST'])
def insertUser():
    nombre = request.json['name']
    contrasena = request.json['password']
    email = request.json['email']
    db.session.execute(
        "CALL INSERTAR_USUARIO('" + nombre + "', '" + contrasena + "', '" + email + "')"
    )
    db.session.commit()

    return jsonify({'message': 'Hecho'})

if __name__ == "__main__":
    app.run(debug=True)

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(70), unique=True)
#     description = db.Column(db.String(100))

#     def __init__(self, title, description):
#         self.title = title
#         self.description = description

# db.create_all()

# class TaskSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'title', 'description')

# task_schema = TaskSchema()
# tasks_schema = TaskSchema(many=True)


# @app.route('/tasks', methods=['POST'])
# def create_task():

#     title = request.json['title']
#     description = request.json['description']

#     new_task = Task(title, description)
#     db.session.add(new_task)
#     db.session.commit()

#     return task_schema.jsonify(new_task)

#     # print(request.json)
#     # return 'recibido'

# @app.route('/tasks', methods=['GET'])
# def get_tasks():
#     all_tasks = Task.query.all()
#     result = tasks_schema.dump(all_tasks)
#     return jsonify(result)

# @app.route('/tasks/<id>', methods=['GET'])
# def get_task(id):
#     task = Task.query.get(id)
#     return task_schema.jsonify(task)

# @app.route('/tasks/<id>', methods=['PUT'])
# def update_task(id):
#     task = Task.query.get(id)

#     title = request.json['title']
#     description = request.json['description']

#     task.title = title
#     task.description = description

#     db.session.commit()

#     return task_schema.jsonify(task)

# @app.route('/tasks/<id>', methods=['DELETE'])
# def delete_task(id):
#     task = Task.query.get(id)

#     db.session.delete(task)
#     db.session.commit()
    
#     return task_schema.jsonify(task)