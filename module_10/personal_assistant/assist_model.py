import re
from datetime import timedelta, datetime

import pymongo

from personal_assistant.db import contacts_collection


class RecordEditor:
    def change_field_value(self, name, field, updated_data, command):
        """
        Function change field value.
        :param name: contact name that data which should be changed
        :param field: field to delete
        :param updated_data: new value
        :return: (dict) updated entry
        """
        if command == 'note_add':
            existing_note = contacts_collection.find(
                {'name': {'$eq': name}},
                {'note': 1, '_id': 0}
            )
            existing_note = list(existing_note)[0]['note']
            updated_data = existing_note + updated_data

        contacts_collection.update_one(
            {'name': name},
            {'$set': {field: updated_data}}
        )


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
        count_name = contacts_collection.find(
            {"name": {'$eq': name}}
        )
        return len(list(count_name)) > 0

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
        contacts_collection.insert_one(
            {
                'name': name,
                'birthday': datetime.strptime(f"{str(birthday)}T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"),

                'note': note,
                'phones': [
                    {'phone': phone},
                ],
                'emails': [
                    {'email': email}
                ]
            }
        )


class RecordForDeletion:
    def to_delete(self, name):
        """
        Function deletes records by specified name.
        :return: None
        """
        contacts_collection.delete_one({'name': name})


class BirthdayPeople:
    def to_congratulate(self, n, datetime_now):
        """
        The function returns a list of contacts filtered by date of birth after "n" days.
        """
        user_date = datetime_now + timedelta(days=int(n))  # Getting needed date

        contacts = contacts_collection.aggregate(
            [
                {
                    "$addFields": {
                        "month_day": {
                            "$dateToString": {
                                "format": '%m-%d',
                                "date": '$birthday'
                            }
                        }
                    }
                },
                {
                    "$match": {
                        "month_day": {
                            '$eq': user_date.strftime('%m-%d')
                        }
                    }
                },
                {
                    '$sort': {
                        'name': pymongo.ASCENDING
                    }
                }
            ]
        )

        return list(contacts)


class RecordSearcher:
    def to_search(self, key_word):
        """
        Search for contacts and notes from the contact book. NOT LOOKING FOR BY DATE OF BIRTH !!!
        """
        match = contacts_collection.find(
            {
                '$or': [
                    {"name": {"$regex": key_word, "$options": "i"}},
                    {"note": {"$regex": key_word, "$options": "i"}},
                    {"phones.phone": {"$regex": key_word, "$options": "i"}},
                    {"emails.email": {"$regex": key_word, "$options": "i"}}
                ]
            }
        )

        return list(match)


class DatabaseContent:
    def to_get_all(self):
        contacts = contacts_collection.find()

        return contacts


