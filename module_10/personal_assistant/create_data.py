from faker import Faker
from datetime import datetime

from db import contacts_collection

fake = Faker()


def create_contacts():
    for _i in range(500):
        name = fake.name()
        note = None
        if _i % 2 == 0:
            note = fake.job()
        contacts_collection.insert_one(
            {
                'name': name,
                'birthday': datetime.strptime(f"{str(fake.date_of_birth())}T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"),

                'note': note,
                'phones': [
                    {'phone': fake.phone_number()},
                ],
                'emails': [
                    {'email': f'{name.lower().replace(" ", ".")}@gmail.com'}
                ]
            }
        )


if __name__ == '__main__':
    create_contacts()
