from app.models import db, Review, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_reviews():
    review1 = Review(
        userId=1,
        companyId=1,
        review='This place is fantastic!! Astrid took fantastic care of me. I am definitely coming back.',
        stars=5
    )
    review2 = Review(
        userId=2,
        companyId=1,
        review='My skin was red for a week afterwards and I had some pain. A friendly staff though',
        stars=2
    )

    db.session.add(review1)
    db.session.add(review2)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_reviews():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.reviews RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reviews"))

    db.session.commit()
