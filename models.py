from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.String(10), unique=True, nullable=False)
    train_name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    departure = db.Column(db.String(20), nullable=False)
    arrival = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "train_id": self.train_id,
            "train_name": self.train_name,
            "source": self.source,
            "destination": self.destination,
            "departure": self.departure,
            "arrival": self.arrival
        }
