from app.models import db, Appointment, Service, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime


def seed_appointments():
    appointment1 = Appointment(
        userId=1,
        employeeId=2,
        appointmentDate=datetime(2023, 11, 29),
        appointmentTimeStr="9:00 AM",
    )

    service_ids_for_appointment1 = [1, 2, 3]
    services_for_appointment1 = Service.query.filter(
        Service.id.in_(service_ids_for_appointment1)).all()

    appointment1.services = services_for_appointment1

    appointment2 = Appointment(
        userId=2,
        employeeId=2,
        appointmentDate=datetime(2023, 11, 16),
        appointmentTimeStr="11:00 AM",
    )
    service_ids_for_appointment2 = [3, 4, 5]
    services_for_appointment2 = Service.query.filter(
        Service.id.in_(service_ids_for_appointment2)).all()
    appointment2.services = services_for_appointment2

    db.session.add(appointment1)
    db.session.add(appointment2)
    db.session.commit()


def undo_appointments():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.appointments RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM appointments"))

    db.session.commit()
