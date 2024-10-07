from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True, default="https://example.com/default_image.jpg")  # Allowing default value
    price = db.Column(db.Float, nullable=True, default=0.00)  # Allowing default price
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'price': self.price
        }
