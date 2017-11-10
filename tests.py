from unittest import TestCase
from model import db, connect_to_db, User, Chart, Star
from flask import Flask
from datetime import datetime

def make_example_data():
    """Add test data to the database"""

    #create users
    charlie = User(firstname="Charlie", lastname="Dog",
                   email="charlie@dogsaregreat.com", password="marshmallow")
    maisey = User(firstname="Maisey", lastname="Puppy",
                  email="maisey@squirrelchasers.com", password="monkey")

    #create a chart that they share
    chart = Chart(title="StarChart")
    chart.users = [charlie, maisey]

    #add some stars to the chart
    star1 = Star(giver=charlie, receiver=maisey, reason="For licking my nose",
                 timestamp=datetime(2016, 12, 31), chart=chart)
    star2 = Star(giver=maisey, receiver=charlie,
                 reason="For being a great big sister",
                 timestamp=datetime(2016, 11, 21), chart=chart)

    #put the whole collection in the database; everything hangs off of the
    #stars so we can just add them
    db.session.add_all([star1, star2])
    db.session.commit()

    # import pdb; pdb.set_trace()



class ModelTests(TestCase):
    """Tests for the model"""

    def setUp(self):

        #connect to test database
        app = Flask(__name__)
        connect_to_db(app, "postgresql:///testdb")

        #add data to the database
        db.create_all()
        make_example_data()

    def tearDown(self):

        #clear out the database
        db.session.close()
        db.drop_all()

    def test_reprs(self):
        """Make sure the reprs are doing their job"""

        #test User repr
        charlie = User.query.get(1)
        self.assertEqual(
            charlie.__repr__(),
            "<User Charlie Dog id: 1>")

        #test Chart repr
        chart = Chart.query.get(1)
        self.assertEqual(
            chart.__repr__(),
            "<Chart id: 1 users: [u'Charlie Dog', u'Maisey Puppy']>")

        #test Star repr
        star = Star.query.get(1)
        self.assertEqual(
            star.__repr__(),
            "<Star id: 1 from: Charlie Dog to: Maisey Puppy on 2016-12-31>")


    def test_chart_get_stars(self):
        """Test the get_stars() method in the Chart class"""

        #get relevant objects out of DB
        chart = Chart.query.get(1)
        maisey_star = Star.query.get(1)
        charlie_star = Star.query.get(2)

        #run the method and make sure it gave back the right stuff
        stars = chart.get_stars()
        self.assertEqual(stars, {1: [charlie_star],
                                 2: [maisey_star]})







if __name__ == "__main__":
    print
    print
    import unittest
    unittest.main(verbosity=2)
