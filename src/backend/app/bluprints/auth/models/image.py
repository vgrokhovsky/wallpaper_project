from . import bd_object as db


category_image = db.Table('category_image',
    db.Column('image_id', db.Integer, db.ForeignKey('images.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    categories = db.relationship('Category', secondary=category_image, backref='images')

    