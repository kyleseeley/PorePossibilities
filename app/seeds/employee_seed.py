from app.models import db, Employee, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_employees():
    astrid = Employee(
        firstname='Astrid',
        lastname='Valles',
        email='astrid@pore.com',
        password='password',
        authorized=True,
        is_owner=True,
        availability={
            "Monday": ["9:00 AM - 6:00 PM"],
            "Tuesday": ["9:00 AM - 6:00 PM"],
            "Wednesday": ["9:00 AM - 6:00 PM"],
            "Thursday": ["9:00 AM - 6:00 PM"],
            "Friday": ["9:00 AM - 6:00 PM"],
            "Saturday": [],
            "Sunday": []
        })
    sanam = Employee(
        firstname='Sanam',
        lastname='Nejad',
        email='sanam@pore.com',
        password='password',
        authorized=True,
        availability={
            "Monday": ["9:00 AM - 1:00 PM"],
            "Tuesday": ["11:00 AM - 6:00 PM"],
            "Wednesday": [],
            "Thursday": ["9:00 AM - 3:00 PM"],
            "Friday": ["12:00 PM - 6:00 PM"],
            "Saturday": ["9:00 AM - 1:00 PM"],
            "Sunday": []
        })
    lindsay = Employee(
        firstname='Lindsay',
        lastname='Fischer',
        email='lindsay@pore.com',
        password='password',
        authorized=False,
        availability={
            "Monday": [],
            "Tuesday": ["11:00 AM - 6:00 PM"],
            "Wednesday": ["9:00 AM - 2:00 PM"],
            "Thursday": [],
            "Friday": ["9:00 AM - 3:00 PM"],
            "Saturday": ["9:00 AM - 1:00 PM"],
            "Sunday": ["9:00 AM - 1:00 PM"]
        })

    db.session.add(astrid)
    db.session.add(sanam)
    db.session.add(lindsay)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_employees():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.employees RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM employees"))

    db.session.commit()
