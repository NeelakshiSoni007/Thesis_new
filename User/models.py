from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    pwd = db.Column(db.String(120), index=True, unique=False)

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):

        return False

    def get_id(self):
        return str(self.id)



    def __repr__(self):
        return '<User %r>' % (self.username)
