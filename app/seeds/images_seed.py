from app.models import db, Image, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_images():
    image1 = Image(
        name='Signature',
        imageUrl='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-8.jpg',
    )
    image2 = Image(
        name='Botanical Beaute',
        imageUrl='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-30.jpg',
    )
    image3 = Image(
        name='Everything Laser',
        imageUrl='https://skintheore.com/cdn/shop/files/SkinTheore-90.jpg',
    )
    image4 = Image(
        name='Microneedling',
        imageUrl='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-55.jpg',
    )
    image5 = Image(
        name='NanoGlow Renewel',
        imageUrl='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-20.jpg',
    )

    db.session.add(image1)
    db.session.add(image2)
    db.session.add(image3)
    db.session.add(image4)
    db.session.add(image5)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_images():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM images"))

    db.session.commit()