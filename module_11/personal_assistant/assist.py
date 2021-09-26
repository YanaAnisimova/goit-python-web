from datetime import timedelta, datetime

from bson.objectid import ObjectId
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template, request, url_for
)

import pymongo
from pymongo.collection import Collection

from personal_assistant.db import get_db

import re

from werkzeug.exceptions import abort


assist_bp = Blueprint('assist', __name__, url_prefix='/assist')


def _load_collection() -> Collection:
    db = get_db()
    return db.contacts


@assist_bp.route('/show', methods=['GET'])
def show():
    cont_collection = _load_collection()
    cursor = cont_collection.find().sort(
        [('name', pymongo.ASCENDING)]
    )
    contacts = transforms_cursor(cursor)
    return render_template('assist/show.html', contacts=contacts)


def transforms_cursor(cursor):
    return [
        {
            **{
                'id': str(contact['_id']),  # to be able to create redirect
                'index': index,
                'name': contact['name'],
                'phone': contact['phones'][0]['phone'],
                'email': contact['emails'][0]['email'],
                'birthday': contact['birthday'].strftime('%Y-%m-%d'),
                'note': contact['note'] if contact['note'] else '',
            }
        }
        for index, contact in enumerate(cursor, 1)
    ]


@assist_bp.route('/<contact_id>/delete', methods=('POST',))
def delete(contact_id):
    cont_collection = _load_collection()
    query = {'_id': ObjectId(contact_id)}
    contact = cont_collection.find_one(query)

    if not list(contact):
        abort(404, f'Not found todo {contact_id}')

    cont_collection.delete_one(query)
    flash(f'The contact named {contact["name"]} has been deleted.')

    return redirect(url_for('assist.show'))


@assist_bp.route('/search', methods=['GET'])
def search():
    cont_collection = _load_collection()
    keyword = request.args.get('keyword')
    cursor = cont_collection.find(
            {
                '$or': [
                    {"name": {"$regex": keyword, "$options": "i"}},
                    {"note": {"$regex": keyword, "$options": "i"}},
                    {"phones.phone": {"$regex": keyword, "$options": "i"}},
                    {"emails.email": {"$regex": keyword, "$options": "i"}}
                ]
            }
        ).sort([('name', pymongo.ASCENDING)])

    contacts = transforms_cursor(cursor)

    if contacts:
        flash(f'Found some users with matching keyword "{keyword}": ')

    return render_template('assist/show.html', contacts=contacts)


@assist_bp.route('/birthday', methods=['GET'])
def birthday():
    cont_collection = _load_collection()
    count_day = request.args.get('count_day')
    user_date = datetime.now().date() + timedelta(days=int(count_day))  # Getting needed date
    cursor = cont_collection.aggregate(
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

    contacts = transforms_cursor(cursor)
    return render_template('assist/show.html', contacts=contacts)


@assist_bp.route('/edit/<contact_id>', methods=('POST', 'GET'))
def edit(contact_id):
    cont_collection = _load_collection()
    query = {'_id': ObjectId(contact_id)}
    contact = cont_collection.find_one(query)

    name = contact['name']
    phone = contact['phones'][0]['phone']
    email = contact['emails'][0]['email']
    birthday = contact['birthday'].strftime('%Y-%m-%d')
    note = '' if contact['note'] is None else contact['note']

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        birthday = request.form['birthday']
        note = request.form['note']

        error = validate(name, phone, email, birthday)

        if not error:
            cont_collection.update_one(
                    query,
                    {'$set': {
                        'name': name,
                        'birthday': datetime.strptime(f"{str(birthday)}T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"),

                        'note': note,
                        'phones': [
                            {'phone': phone},
                        ],
                        'emails': [
                            {'email': email}
                        ]
                    }}
                )
            flash(f'Updated contact details for "{name}".')
            return redirect(url_for("assist.show"))
        flash(error)

    return render_template('assist/create.html', name=name, phone=phone, email=email, birthday=birthday, note=note)


@assist_bp.route('/create', methods=('GET', 'POST'))
def create():
    cont_collection = _load_collection()
    name = ''
    phone = ''
    email = ''
    birthday = ''
    note = ''

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        birthday = request.form['birthday']
        note = request.form['note']

        error = validate(name, phone, email, birthday)

        if not error:
            cont_collection.insert_one(
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

            return redirect(url_for("assist.show"))

        flash(error)

    return render_template('assist/create.html', name=name, phone=phone, email=email, birthday=birthday, note=note)


def validate(name, phone, email, birthday):
    error = ''
    if not name:
        error = 'Name is required.'
    elif not phone:
        error = 'Phone is required.'
    elif not email:
        error = 'Email is required.'
    elif not birthday:
        error = 'Birthday is required.'

    try:
        if phone != (re.search(r'(\+?\d?\d?\d?\d{2}\d{7})', phone)).group():
            raise AttributeError
    except AttributeError:
        error = 'Enter the phone number in the "+888888888888" format.'

    try:
        if email != (re.search(r'[a-zA-Z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}', email)).group():
            raise AttributeError
    except AttributeError:
        error = 'Enter the email in the "sss@ss.ss" format.'

    return error


