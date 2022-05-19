#!/usr/bin/python3
"""
Module to serve all requests relating to a school
"""

from crypt import methods
from api.v1.views import app_views
from flask import request, jsonify
from flask_login import current_user
from api.v1.views.auth import bcrypt

@app_views.route('/users/<user_id>/schools')
def get_schools(user_id):
    """Function to get all schools for a user"""
    from models import storage

    user = storage.get('User', user_id)
    if not user:
        return "No such user"
    for k, usr in user.items():
        schools = usr.schools
    new_dict = {}
    for sch in schools:
        new_dict[sch.id] = sch.to_dict()
    return jsonify(new_dict)

@app_views.route('/users/<user_id>/schools/<sch_id>', methods=['GET'], strict_slashes=False)
def get_school(user_id, sch_id):
    """Function to get a school for a user"""
    from models import storage

    user = storage.get('User', user_id)
    if not user:
        return "No such user"
    for k, usr in user.items():
        schools = usr.schools
    sch_fees_expected = 0
    sch_fees_paid = 0
    for sch in schools:
        if sch.id == sch_id:
            sch_dict = sch.to_dict()
            sch_classes = sch.classes
            for cls in sch_classes:
                sch_fees_expected += cls.fees_expected * cls.no_of_students
                sch_fees_paid += cls.fees_paid
            if sch_fees_expected == 0:
                sch_percent = 0
            else:
                sch_percent = int((sch_fees_paid / sch_fees_expected) * 100)
            new_dict = {}
            sch_dict['sch_percent'] = sch_percent
            new_dict[sch.id] = sch_dict
            break
    return jsonify(new_dict)

@app_views.route('/users/<user_id>/schools', methods=['POST'], strict_slashes=False)
def create_school(user_id):
    """Function to create a school for a user"""
    from models import storage
    from models.schools import School


    info = request.get_json()
    sch_info = {}
    a = sch_info['name'] = info.get('name')
    b = sch_info['address'] = info.get('address')
    c = sch_info['level'] = info.get('level')
    d = sch_info['user_id'] = user_id
    pwd = info.get('password')
    user = storage.get('User', user_id)
    if not user:
        return jsonify({"code": "Invalid user id"})
    if not (a and b and c and pwd and d):
        return jsonify({"code": "Invalid data"})
    check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": 'Wrong password'})
    for k, usr in user.items():
        user_schools = usr.schools
    for sch in user_schools:
        if sch.name == sch_info['name']:
            return jsonify({"code": "School exists"})
    new_sch = School(**sch_info)
    save_cls = storage.save()
    if save_cls is True:
        return jsonify({"code": "School created"})
    else:
        return jsonify({"code": "Post failed"})

@app_views.route('/users/<user_id>/schools/<sch_id>', methods=['PUT'], strict_slashes=False)
def update_sch(user_id, sch_id):
    """Function to update a school"""
    from models import storage

    info = request.get_json()
    pwd = info.get('password')
    check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": "Wrong password"})
    a = name = info.get('name').replace('_', ' ')
    b = address = info.get('address').replace('_', ' ')
    c = level = info.get('level')
    if not (a and b and c):
        return jsonify({"code": "Invalid credentials"})
    update_dict = {}
    update_dict['name'] = name
    update_dict['address'] = address
    update_dict['level'] = level
    school = storage.get('School', sch_id)
    if not school:
        return jsonify({"code": "Invalid school id"})
    for k, sch in school.items():
        if sch.id == sch_id:
            sch.update(**update_dict)
            save_sch = storage.save()
            if save_sch is True:
                return jsonify({"code": "Updated"})
    return jsonify({"code": "Error updating student"})

@app_views.route('/users/<user_id>/schools/<sch_id>', methods=['DELETE'], strict_slashes=False)
def delete_school(user_id, sch_id):
    """Function to delete a school from record"""
    from models import storage

    info = request.get_json()
    pwd = info.get('password')
    check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": 'Wrong password'})
    schools = current_user.schools
    del_sch = False
    for sch in schools:
        if sch.id == sch_id:
            storage.delete(sch)
            del_sch = storage.save()
    if del_sch is True:
        return jsonify({"code": "Deleted"})
    else:
        return jsonify({"code": "Error deleting school"})