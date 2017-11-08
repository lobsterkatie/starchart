from flask_sqlalchemy import SQLAlchemy
from json import dumps

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """A user of the app."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)

    charts = db.relationship("User", secondary="usercharts")

    def __repr__(self):
        """Provide helpful representation when printed"""

        repr_str = "<User {fname} {lname} id: {id}>"
        return repr_str.format(fname=self.firstname,
                               lname=self.lastname,
                               id=self.user_id)

    def get_full_name(self):
        """Return the user's full name"""

        return " ".join([self.firstname, self.lastname])


class Chart(db.Model):
    """A chart belonging to one user"""

    __tablename__ = "charts"

    chart_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)

    users = db.relationship("User", secondary="usercharts")

    def __repr__(self):
        """Provide helpful representation when printed"""

        repr_str = "<Chart id: {id} users: {users}>"
        users = [user.get_full_name() for user in self.users]
        return repr_str.format(id=self.chart_id, users=users)


class UserChart(db.Model):
    """An association table connecting charts to users"""

    __tablename__ = "usercharts"

    chart_user_id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.Integer,
                         db.ForeignKey("charts.chart_id"),
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)


class Star(db.Model):
    """A star on a given chart"""

    __tablename__ = "stars"

    star_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    giver_id = db.Column(db.Integer,
                         db.ForeignKey("users.user_id"),
                         nullable=False)
    receiver_id = db.Column(db.Integer,
                            db.ForeignKey("users.user_id"),
                            nullable=False)
    color = db.Column(db.String(32), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text, nullable=True)

    chart = db.relationship("Chart")
    giver = db.relationship("User",
                            primaryjoin="User.user_id==Star.giver_id")
    receiver = db.relationship("User",
                               primaryjoin="User.user_id==Star.receiver_id")

    def __repr__(self):
        """Provide helpful representation when printed"""

        repr_str = "<Star id: {id} from: {giver} to: {receiver} on {ts}>"
        return repr_str.format(id=self.star_id,
                               giver=self.giver.get_full_name(),
                               receiver=self.receiver.get_full_name(),
                               ts=self.timestamp.date())



# FIXME do I need this???
class Frienships(db.Model):
    """A friend relationship between two users"""

    __tablename__ = "friendships"

    friendship_id = db.Column(db.Integer, primary_key=True)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to the Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///starchart'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    #create a fake flask app, so that we can talk to the database by running
    #this file directly
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
