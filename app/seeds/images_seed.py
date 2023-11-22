from app.models import db, Image, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_images():
    image1 = Image(
        name='Signature',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-8.jpg',
    )
    image2 = Image(
        name='Botanical Beaute',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-30.jpg',
    )
    image3 = Image(
        name='Advanced Skincare Treatments 1',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-90.jpg',
    )
    image4 = Image(
        name="Advanced Skincare Treatments 2",
        imageFile="https://skintheore.com/cdn/shop/files/SkinTheore-78.jpg"
    )
    image5 = Image(
        name='NanoGlow Renewel',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-20.jpg',
    )
    image6 = Image(
        name='Home Page 1',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-96.jpg'
    )

    image7 = Image(
        name='Home Page 2',
        imageFile='https://skintheore.com/cdn/shop/files/pexels-polina-kovaleva-6543620.jpg'
    )
    image8 = Image(
        name='Astrid making bed',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-13.jpg'
    )
    image9 = Image(
        name='Laser Treatment',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-88.jpg'
    )

    image10 = Image(
        name='Everything Laser',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-87.jpg'
    )
    image11 = Image(
        name='Microneedling',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-55.jpg',
    )
    image12 = Image(
        name='No-Peel Peel',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-96.jpg'
    )
    image13 = Image(
        name='Skincare Treatments 1',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-71.jpg'
    )
    image14 = Image(
        name='Signature Skin Therapies',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-109.jpg'
    )
    image15 = Image(
        name='Skincare Treatments 2',
        imageFile='https://skintheore.com/cdn/shop/files/GentleFoamingCleanser-Social_8_fb839295-b075-4b7d-81a5-9b3011414050.webp'
    )
    image16 = Image(
        name='Oxytheore',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-66.jpg'
    )
    image17 = Image(
        name='Nanoglow',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-54.jpg'
    )
    image18 = Image(
        name='Signature Skin Therapies 2',
        imageFile='https://skintheore.com/cdn/shop/files/top-view-young-woman-getting-beauty-treatment.jpg'
    )
    image19 = Image(
        name='Microneedle RF',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-14.jpg'
    )
    image20 = Image(
        name='Complexion Correrction',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-85.jpg'
    )
    image21 = Image(
        name='Oxytheore Sculpt',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore_-_August_2023_-67_c475ba2a-3e8f-4983-afca-173ea8829e86.jpg'
    )
    image22 = Image(
        name='Injectable Treatments 1',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-109_965d90a6-e226-4cfa-8f26-0b64aefe321f.jpg'
    )
    image23 = Image(
        name='Injectable Treatments 1',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-102_23b3fe76-9d5f-407d-bdeb-87f46f9eee0a.jpg'
    )
    image24 = Image(
        name='Wrinkle Relax',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-112.jpg'
    )
    image25 = Image(
        name='Lip Filler',
        imageFile='https://skintheore.com/cdn/shop/files/ST_Injectables.png'
    )
    image26 = Image(
        name='Midface Filler',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-108.jpg'
    )
    image27 = Image(
        name='Lower Face Filler',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-113.jpg'
    )
    image28 = Image(
        name='Face Towel',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-78.jpg'
    )
    image29 = Image(
        name='Astrid Face Shot',
        imageFile='https://skintheore.com/cdn/shop/files/SkinTheore-31.jpg'
    )
    image30 = Image(
        name='Sanam Face Shot',
        imageFile='https://media.licdn.com/dms/image/C5603AQHFIt9Vy0bSbQ/profile-displayphoto-shrink_800_800/0/1581230842626?e=1706140800&v=beta&t=uM0UsfixeylLQYxwvBnFFsTC5KvxrE2vhgSEDIf7rCc'
    )
    image31 = Image(
        name='Lindsay Face Shot',
        imageFile='https://scontent-den4-1.xx.fbcdn.net/v/t1.6435-9/155861024_10158876862659890_3677374401456024319_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=7f8c78&_nc_ohc=4hFAPzMAaNoAX92CwJi&_nc_ht=scontent-den4-1.xx&oh=00_AfBP4A5CFzTdyQ2uKyaEYk3sWcL2CfDgXJv3fFXrZI2GXA&oe=6584F286'
    )

    db.session.add(image1)
    db.session.add(image2)
    db.session.add(image3)
    db.session.add(image4)
    db.session.add(image5)
    db.session.add(image6)
    db.session.add(image7)
    db.session.add(image8)
    db.session.add(image9)
    db.session.add(image10)
    db.session.add(image11)
    db.session.add(image12)
    db.session.add(image13)
    db.session.add(image14)
    db.session.add(image15)
    db.session.add(image16)
    db.session.add(image17)
    db.session.add(image18)
    db.session.add(image19)
    db.session.add(image20)
    db.session.add(image21)
    db.session.add(image22)
    db.session.add(image23)
    db.session.add(image24)
    db.session.add(image25)
    db.session.add(image26)
    db.session.add(image27)
    db.session.add(image28)
    db.session.add(image29)
    db.session.add(image30)
    db.session.add(image31)
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
