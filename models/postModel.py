from main import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body
        }
    
    def __repr__(self):
        return '<Post %r>' % self.title