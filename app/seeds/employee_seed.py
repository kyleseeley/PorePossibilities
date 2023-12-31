from app.models import db, Employee, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime


# Adds a demo user, you can add other users here if you want
def seed_employees():
    astrid = Employee(
        firstname='Astrid',
        lastname='Valles',
        email='astrid@pore.com',
        password='password',
        authorized=True,
        is_owner=True,
        about='Astrid Valles is a skilled Registered Nurse and Licensed Aesthetician with 16 years of experience in aesthetics. With a background in the operating room and medical spa, she has received training from top professionals in the field. Astrid\'s passion lies in truly understanding her patients, addressing their concerns and goals beyond aesthetics. She treats each patient holistically, caring for their skin, emotional well-being, and overall health. Astrid\'s journey began at her mom\'s salon, where she learned the reward of helping people feel great. Now based in Denver, she enjoys outdoor adventures and spending time with her pets.',
        job_title='Registered Nurse and Licensed Aesthetician',
        monday_start=None,
        monday_end=None,
        tuesday_start=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        tuesday_end=datetime.strptime("4:00 PM", '%I:%M %p').time(),
        wednesday_start=datetime.strptime("10:00 AM", '%I:%M %p').time(),
        wednesday_end=datetime.strptime("6:00 PM", '%I:%M %p').time(),
        thursday_start=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        thursday_end=datetime.strptime("4:00 PM", '%I:%M %p').time(),
        friday_start=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        friday_end=datetime.strptime("3:00 PM", '%I:%M %p').time(),
        saturday_start=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        saturday_end=datetime.strptime("2:00 PM", '%I:%M %p').time(),
        sunday_start=None,
        sunday_end=None)
    sanam = Employee(
        firstname='Sanam',
        lastname='Nejad',
        email='sanam@pore.com',
        password='password',
        authorized=True,
        monday_start=None,
        monday_end=None,
        tuesday_start=datetime.strptime("10:00 AM", '%I:%M %p').time(),
        tuesday_end=datetime.strptime("3:00 PM", '%I:%M %p').time(),
        wednesday_start=datetime.strptime("10:00 AM", '%I:%M %p').time(),
        wednesday_end=datetime.strptime("4:00 PM", '%I:%M %p').time(),
        thursday_start=datetime.strptime("11:00 AM", '%I:%M %p').time(),
        thursday_end=datetime.strptime("4:00 PM", '%I:%M %p').time(),
        friday_start=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        friday_end=datetime.strptime("3:00 PM", '%I:%M %p').time(),
        saturday_start=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        saturday_end=datetime.strptime("2:00 PM", '%I:%M %p').time(),
        sunday_start=None,
        sunday_end=None)
    lindsay = Employee(
        firstname='Lindsay',
        lastname='Fischer',
        email='lindsay@pore.com',
        password='password',
        authorized=False,
        monday_start=None,
        monday_end=None,
        tuesday_start=None,
        tuesday_end=None,
        wednesday_start=datetime.strptime("12:00 AM", '%I:%M %p').time(),
        wednesday_end=datetime.strptime("6:00 PM", '%I:%M %p').time(),
        thursday_start=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        thursday_end=datetime.strptime("2:00 PM", '%I:%M %p').time(),
        friday_start=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        friday_end=datetime.strptime("1:00 PM", '%I:%M %p').time(),
        saturday_start=datetime.strptime("9:30 AM", '%I:%M %p').time(),
        saturday_end=datetime.strptime("2:00 PM", '%I:%M %p').time(),
        sunday_start=None,
        sunday_end=None)

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
