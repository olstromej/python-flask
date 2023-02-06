from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('animals', user='olstromej', password='123', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Animals(BaseModel):
  name = CharField()
  type = CharField()

db.connect()
db.drop_tables([Animals])
db.create_tables([Animals])

Animals(name='Fritz', type='dog').save()
Animals(name='Klaus', age='cat').save()
zoey = Animals(name='Zoey', type = 'dog')
zoey.save()
melvin = Animals(name = 'Melvin', type = 'cat')
melvin.save()

app = Flask(__name__)

@app.route('/animals/', methods=['GET', 'POST'])
@app.route('/animals/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Animals.get(Animals.id == id)))
    else:
        animal_list = []
        for animal in Animals.select():
            animal_list.append(model_to_dict(animal))
        return jsonify(animal_list)

  if request.method =='PUT':
    body = request.get_json()
    Animals.update(body).where(Animals.id == id).execute()
    return "Animals " + str(id) + " has been updated."

  if request.method == 'POST':
    new_animal = dict_to_model(Animals, request.get_json())
    new_animal.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Animals.delete().where(Animals.id == id).execute()
    return "Person " + str(id) + " deleted."

app.run(debug=True, port=3030)