import random

from faker import Faker
from sqlalchemy import exists, and_
from db import session, engine
from sqlalchemy.sql.expression import func
from models import (Contact, Phone, Email)

fake = Faker()


def create_contacts():
    for _i in range(500):
        name = fake.name()
        note = None
        if _i % 2 == 0:
            note = fake.job()

        contact = Contact(
            name=name,
            birthday=fake.date_of_birth(),
            note=note,
        )
        session.add(contact)
        session.commit()

        phone = Phone(
            phone=fake.phone_number(),
            contact_id=contact.contact_id,
        )
        session.add(phone)

        email = Email(
            email=f'{name.lower().replace(" ", ".")}@gmail.com',
            contact_id=contact.contact_id,
        )
        session.add(email)
    session.commit()


if __name__ == '__main__':
    create_contacts()