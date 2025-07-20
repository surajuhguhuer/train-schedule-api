from flask import Flask, request, jsonify
from models import db, Train
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///trains.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return "🚆 Train Schedule API is running!"

@app.route('/trains', methods=['GET'])
def get_trains():
    trains = Train.query.all()
    return jsonify([t.to_dict() for t in trains])

@app.route('/trains/<source>/<destination>', methods=['GET'])
def get_trains_between(source, destination):
    trains = Train.query.filter_by(source=source, destination=destination).all()
    return jsonify([t.to_dict() for t in trains])

@app.route('/trains', methods=['POST'])
def add_train():
    data = request.json
    new_train = Train(
        train_id=data['train_id'],
        train_name=data['train_name'],
        source=data['source'],
        destination=data['destination'],
        departure=data['departure'],
        arrival=data['arrival']
    )
    db.session.add(new_train)
    db.session.commit()
    return jsonify({"message": "Train added successfully!"}), 201

@app.route('/trains/<train_id>', methods=['PUT'])
def update_train(train_id):
    data = request.json
    train = Train.query.filter_by(train_id=train_id).first()
    if not train:
        return jsonify({"error": "Train not found"}), 404

    train.train_name = data.get('train_name', train.train_name)
    train.source = data.get('source', train.source)
    train.destination = data.get('destination', train.destination)
    train.departure = data.get('departure', train.departure)
    train.arrival = data.get('arrival', train.arrival)
    db.session.commit()
    return jsonify({"message": "Train updated successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
