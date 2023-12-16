from app.models import db, Company, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime


# Adds a demo user, you can add other users here if you want
def seed_company():
    company1 = Company(
        ownerId=1,
        name='Pore Possibilities',
        email='hello@porepossibilities.com',
        phone='555-222-7673',
        address='865 Albion St. Suite 250',
        city='Denver',
        state='CO',
        zipCode='80220',
        starRating=3.5,
        numReviews=2,
        monday_open=None,
        monday_close=None,
        tuesday_open=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        tuesday_close=datetime.strptime("4:00 PM", '%I:%M %p').time(),
        wednesday_open=datetime.strptime("10:00 AM", '%I:%M %p').time(),
        wednesday_close=datetime.strptime("6:00 AM", '%I:%M %p').time(),
        thursday_open=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        thursday_close=datetime.strptime("4:00 PM", '%I:%M %p').time(),
        friday_open=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        friday_close=datetime.strptime("3:00 PM", '%I:%M %p').time(),
        saturday_open=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        saturday_close=datetime.strptime("2:00 PM", '%I:%M %p').time(),
        sunday_open=None,
        sunday_close=None
    )

    db.session.add(company1)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_company():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.companies RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM companies"))

    db.session.commit()
