#Making necessary imports
from datetime import datetime
from main import db, loginmanager
from flask_login import UserMixin





#Loading user using loginmanager
@loginmanager.user_loader
def load_user(UID):
    return users.query.get(int(UID))





#Making the models
class users(db.Model, UserMixin):
    __tablename__ = 'users'
    UID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    Email = db.Column(db.String, nullable=False, unique=True)
    Name = db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)
    Role = db.Column(db.String, nullable=False, default='user')
    Profile_Photo = db.Column(db.String)
    isactive = db.Column(db.Integer, nullable=False, default=False)
    last_login = db.Column(db.DateTime, default = datetime.now()) 

    user_bookings = db.relationship('Bookings', backref='users', lazy=True)
    user_movies = db.relationship('Movies', backref='users', lazy=True)
    user_theatres = db.relationship('Theatres', backref='users', lazy=True)
    user_shows = db.relationship('Shows', backref='users', lazy=True)


    def get_id(self):
        return str(self.UID)


class Movies(db.Model):
    __tablename__ = 'Movies'
    Mov_Id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    Mov_Name = db.Column(db.String, nullable = False)
    Mov_Rating = db.Column(db.Float)
    Mov_Status = db.Column(db.Boolean, nullable=False, default=True)
    Created_By = db.Column(db.Integer, db.ForeignKey('users.UID'), nullable=False)

    movie_shows = db.relationship('Shows', backref='movie', lazy=True)


class Theatres(db.Model):
    __tablename__ = 'Theatres'
    The_Id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    Created_By = db.Column(db.Integer, db.ForeignKey('users.UID'), nullable=False)
    The_Name = db.Column(db.String, nullable=False)
    The_Location = db.Column(db.String)
    The_Status = db.Column(db.Boolean, nullable=False, default = True)

    theatre_shows = db.relationship('Shows', backref='theatre', lazy=True)
    #theatre_movies = db.relationship('Movies', backref='movie_theatre', lazy=True)


class Shows(db.Model):
    __tablename__ = 'Shows'
    Show_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    The_Id = db.Column(db.Integer, db.ForeignKey('Theatres.The_Id'), primary_key=True, nullable=False)
    Mov_Id =  db.Column(db.Integer, db.ForeignKey('Movies.Mov_Id'), primary_key=True, nullable=False)
    Total_Seats = db.Column(db.Integer, nullable=False)
    Booked_Seats = db.Column(db.Integer, nullable=False, default=0)
    Show_Status = db.Column(db.Boolean, nullable=False, default=True)
    Show_Time = db.Column(db.String)
    Created_By = db.Column(db.Integer, db.ForeignKey('users.UID'), primary_key=True, nullable=False)

    booked_shows = db.relationship('Bookings', backref='shows', lazy=True)
 
    
class Bookings(db.Model):
    __tablename__ = 'Bookings'
    Book_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UId = db.Column(db.Integer, db.ForeignKey('users.UID'), nullable=False)
    Show_Id =  db.Column(db.Integer, db.ForeignKey('Shows.Show_Id'), nullable=False)
    Num_Of_Seats = db.Column(db.Integer, nullable=False)
    Booked_Status = db.Column(db.Integer, nullable=False, default=False)
    Cancellation_Status = db.Column(db.Integer, nullable=False, default=False)
    Reason = db.Column(db.String)
    Collection = db.Column(db.Integer)