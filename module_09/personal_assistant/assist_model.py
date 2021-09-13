import os
import re
from datetime import timedelta, datetime

from sqlalchemy import or_, and_
# from sqlalchemy import select, func, desc, nullslast
from sqlalchemy.orm import joinedload, load_only, selectinload
from sqlalchemy import exc, extract

# from sqlalchemy.sql.expression import func

from personal_assistant.db import session
from personal_assistant.models import Contact, Email, Phone


class RecordEditor:
    def change_field_value(self, name, field, updated_data, command):
        """
        Function change field value.
        :param name: contact name that data which should be changed
        :param field: field to delete
        :param updated_data: new value
        :return: (dict) updated entry
        """
        db = {'name': Contact, 'birthday': Contact, 'note': Contact, 'phone': Phone, 'email': Email}
        table = db[field]
        contact = session.query(
            Contact
        ).filter_by(
            name=name
        ).one()
        con_id = contact.contact_id

        if command == 'note_add':
            existing_note = contact.note
            updated_data = existing_note + updated_data

        session.query(
            table
        ).filter_by(
            contact_id=con_id
        ).update(
            {field: updated_data}
        )
        session.commit()


class ValidationCheck:
    @staticmethod
    def check_birthday(user_birthday):
        try:
            if datetime.strptime(user_birthday, '%Y-%m-%d'):
                return user_birthday
        except ValueError:
            raise ValueError

    @staticmethod
    def check_email(user_email):
        try:
            if user_email == (re.search(r'[a-zA-Z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}', user_email)).group():
                return user_email
            raise AttributeError
        except AttributeError:
            raise AttributeError

    @staticmethod
    def check_is_name_exist(name):
        count_name = session.query(
            Contact
        ).filter_by(
            name=name
        ).count()
        return count_name > 0

    @staticmethod
    def check_phone_number(user_phone_number):
        try:
            if user_phone_number == (re.search(r'\+?\d?\d?\d?\d{2}\d{7}', user_phone_number)).group():
                return user_phone_number
            raise AttributeError
        except AttributeError:
            raise AttributeError


class RecordCreator:
    def to_create_record(self, name, phone, email, birthday, note):
        contact = Contact(
            name=name,
            birthday=birthday,
            note=note,
        )
        session.add(contact)
        session.commit()

        phone = Phone(
            phone=phone,
            contact_id=contact.contact_id,
        )
        session.add(phone)

        email = Email(
            email=email,
            contact_id=contact.contact_id,
        )
        session.add(email)
        session.commit()


class RecordForDeletion:
    def to_delete(self, name):
        """
        Function deletes records by specified name.
        :return: None
        """
        contact = session.query(
            Contact
        ).filter(
            Contact.name == name
        ).one()
        session.delete(contact)
        session.commit()


class BirthdayPeople:
    def to_congratulate(self, n):
        """
        Function return list of users from user list, whose birthday is in n days from current date
        """
        user_date = (datetime.now() + timedelta(days=int(n))).date()  # Getting needed date

        contacts = session.query(
            Contact
        ).join(
            Contact.phones,
            Contact.emails
        ).options(
            joinedload(Contact.phones),
            joinedload(Contact.emails)
        ).filter(
            extract('month', Contact.birthday) == user_date.month,
            extract('day', Contact.birthday) == user_date.day
        ).all()
        return contacts


class RecordSearcher:
    def to_search(self, key_word):
        """
        Search for contacts and notes from the contact book. NOT LOOKING FOR BY DATE OF BIRTH !!!
        """
        match = session.query(
            Contact
        ).join(
            Contact.phones,
            Contact.emails
        ).options(
            joinedload(Contact.phones),
            joinedload(Contact.emails)
        ).filter(
            or_(
                Contact.name.ilike(f'%{key_word}%'),
                Contact.note.ilike(f'%{key_word}%'),
                Phone.phone.ilike(f'%{key_word}%'),
                Email.email.ilike(f'%{key_word}%')
            )
        ).all()
        return match


class DatabaseContent:
    def to_get_all(self):
        contacts = session.query(
            Contact
        ).join(
            Contact.phones,
            Contact.emails
        ).options(
            joinedload(Contact.phones),
            joinedload(Contact.emails)
        ).all()
        return contacts


