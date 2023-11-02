from app.models import db, Service, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_services():
    consultation = Service(
        type='Consultation',
        name='Consultation',
        price=0,
        description='Let\'s chat! After getting better acquainted with you and your skin health goals, we will educate you on the best treatments and skin care. We will get you on a skin health plan that will work with your goals, schedule, and budget. This appointment is complimentary.')
    signature = Service(
        type='Skincare Treatments',
        name='Pore Possibilities Signature',
        price=160,
        description='This rejuvenating and highly effective facial is designed to address skin in need of softening, smoothing, and encouraging that glow that screams “healthy skin”. Invigorating exfoliation with enzymes, steam and ia dermaplane brings your healthy skin to light. Gentle extractions clarify the skin while specialized, focused lift + tone massage to detoxify and leave skin sculpted. Custom blended treatment masks leave the skin radiant, smooth, and bright.')
    botanicalBeaute = Service(
        type='Skincare Treatments',
        name='Botanical Beautē',
        price=160,
        description='Treat your skin with the purest, organic & clean ingredients, handpicked to cater to your unique skin. This results-oriented facial harnesses the power of organic botanicals to deeply cleanse, nourish, and revitalize your skin, leaving it glowing from within. Experience the impact of clean beauty as our Botnia custom-blended facial creates a perfect balance between relaxation and transformative skin care.')
    everythingLaser = Service(
        type='Advanced Skincare Treatments',
        name='Everything Laser',
        price=300,
        description='This no-downtime laser facial is accomplished with the ADVA and is nothing short of an aesthetic treatment miracle. This zero downtime treatment delivers visible results in a single treatment while addressing several skin conditions. This gentle and effective laser treatment addresses: wrinkles, acne scarring, uneven skin texture, dark spots, melasma, rosacea, broken capillaries, redness, crepey skin, large pores, acne, oil production, and sun damage. Skin is left bright and healthier.')
    microneedle = Service(
        type='Advanced Skincare Treatments',
        name='Microneedle',
        price=300,
        description='The aging process naturally slows our collagen and elastin production as we age. This leaves skin less plump, smooth, and peppered with surface lines and texture. Harness your own body’s ability to stimulate collagen and elastin production back to its old self. Microneedling naturally encourages healthier, smoother, brighter skin.')
    microneedleRF = Service(
        type='Signature Skin Therapies',
        name='Microneedle RF',
        price=550,
        description='Microneedling is an amazing, results-oriented treatment. Taking it to the next level by adding Radio Frequency will dramatically tighten lax, loose skin that’s lost its elasticity, in addition to smoothing and restoring your skin to the healthiest version of itself. Stem cells and growth factors are applied to the skin to significantly Improve long term results and make downtime obsolete. A take home after care kit is included with your service.')
    nanoGlowRenewel = Service(
        type='Signature Skin Therapies',
        name='NanoGlow Renewal',
        price=350,
        description='This is your ultimate, red-carpet ready facial treatment. Gentle exfoliation will be used along with the included Dermaplane treatment. We then combine powerhouse treatments designed to get your skin glowing with a proprietary blend of bespoke active ingredients and concentrates formulated just for you based on your current skin condition and needs. This includes benefits and treatments to the face and neck areas. Facial massage will lull you into complete relaxation while promoting lymphatic flow, sculpting facial features and removing toxins from deep within. A specialty translucent hydrogel mask will be slowly molded to the face, locking in the actives from the nano infusion, leaving skin plump, bright, and supremely hydrated like never before. LED Light Therapy will be applied while you mask and your shoulders, neck, and scalp are massaged to complete your red-carpet ready, completely restorative therapy.')
    wrinkleRelax = Service(
        type='Injectables',
        name='Wrinckle Relax',
        price=12,
        description='We offer Botox, Dysport, and Xeomin wrinkles relaxers at Skin Theorē. We will discuss your goals and options for treatment during your pre-treatment consultation.')
    lipFiller = Service(
        type='Injectables',
        name='Lip Filler',
        price=700,
        description='Treating your lips to a fuller look is a quick procedure at Pore Possibilities. Our diverse range of lip fillers adds volume to contour your lips, resulting in a natural and beautiful final look.')

    db.session.add(consultation)
    db.session.add(signature)
    db.session.add(botanicalBeaute)
    db.session.add(everythingLaser)
    db.session.add(microneedle)
    db.session.add(microneedleRF)
    db.session.add(nanoGlowRenewel)
    db.session.add(wrinkleRelax)
    db.session.add(lipFiller)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_services():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.services RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM services"))

    db.session.commit()
