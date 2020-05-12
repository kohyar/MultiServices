from app import db
import logging as lg 





class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(200), nullable = False)
    year = db.Column(db.Integer, nullable = False)

    def __init__(self, name, year):
        self.name = name 
        self.year = year

    def serialize(self):
        return {
            'id':self.id,
            'name': self.name,
            'year': self.year
        }
    def __repr__(self):
        return '<Book {}, year {}>'.format(self.name, self.year)

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Book("David Copperfield", 1849))
    db.session.add(Book("The Sun Also Rises", 1926))
    db.session.commit()
    lg.warning('Database initialized!')
