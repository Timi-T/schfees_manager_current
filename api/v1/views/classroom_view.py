#!/usr/bin/python3
"""
Module to handle all classroom requests
"""

from api.v1.views import app_views
from flask import request, jsonify, render_template
from flask_login import current_user
from api.v1.views.auth import bcrypt


@app_views.route('/schools/<sch_id>/classrooms', methods=['GET'], strict_slashes=False)
def get_classrooms(sch_id):
    """Function to get all classrooms"""
    from models import storage

    schools = current_user.schools
    classes = None
    for sch in schools:
        if sch.id == sch_id:
            classes = sch.classes
    if not classes:
        return jsonify({"code": "No classrooms for this school"})
    new_dict = {}
    for cls in classes:
        new_dict[cls.id] = cls.to_dict()
    return jsonify(new_dict)

@app_views.route('/schools/<sch_id>/classrooms/<cls_id>', methods=['GET'], strict_slashes=False)
def get_classroom(sch_id, cls_id):
    """Function to get a classroom in a school"""
    from models import storage

    schools = current_user.schools
    classes = None
    for sch in schools:
        if sch.id == sch_id:
            classes = sch.classes
    cls_fees_paid = 0
    cls_fees_expected = 0
    new_dict = {}
    if classes:
        for cls in classes:
            if cls.id == cls_id:
                cls_fees_expected += cls.fees_expected * cls.no_of_students
                cls_fees_paid += cls.fees_paid
                if cls_fees_expected == 0:
                    cls_percent = 0
                else:
                    cls_percent = int((cls_fees_paid / cls_fees_expected) * 100)
                cls_dict = cls.to_dict()
                cls_dict['fees_percent'] = cls_percent
                new_dict[cls.id] = cls_dict
    return jsonify(new_dict)

@app_views.route('/schools/<sch_id>/classrooms', methods=['POST'], strict_slashes=False)
def create_class(sch_id):
    """Function to create a classroom in a school"""
    from models import storage
    from models.classrooms import Classroom

    info = request.get_json()
    class_info = {}
    a = class_info['name'] = info.get('name')
    b = class_info['class_teacher'] = info.get('class_teacher')
    c = class_info['fees_expected'] = info.get('fees_expected')
    class_info['sch_id'] = sch_id
    pwd = info.get('password')
    if not (a and b and c and pwd and sch_id):
        return jsonify({"code": "Invalid data"})
    check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": 'Wrong password'})
    school = storage.get('School', sch_id)
    if not school:
        return jsonify({"code": "Invalid school id"})
    for k, sch in school.items():
        classes = sch.classes
    for cls in classes:
        if cls.name == class_info['name']:
            return jsonify({"code": "Class exists"})
    new_class = Classroom(**class_info)
    save_cls = storage.save()
    if save_cls is True:
        for k, v in school.items():
            cur = v.no_of_classes
            v.update(**{"no_of_classes": cur + 1})
            storage.save()
        return jsonify({"code": "Created"})
    else:
        return jsonify({"code": "Post failed"})


@app_views.route('/schools/<sch_id>/classrooms/<cls_id>', methods=['PUT'], strict_slashes=False)
def update_classroom(sch_id, cls_id):
    """Function to update a classroom"""
    from models import storage

    info = request.get_json()
    pwd = info.get('password')
    check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": "Wrong password"})
    a = name = info.get('name').replace('_', ' ')
    b = class_teacher = info.get('class_teacher').replace('_', ' ')
    if not (a and b):
        return jsonify({"code": "Invalid credentials"})
    update_dict = {}
    update_dict['name'] = name
    update_dict['class_teacher'] = class_teacher
    school = storage.get('School', sch_id)
    if not school:
        return jsonify({"code": "Invalid school id"})
    for k, v in school.items():
        classes = v.classes
        for cls in classes:
            if cls.name.replace(' ', '') == (update_dict['name']).replace(' ', ''):
                return jsonify({"code": "Class exists"})
    classroom = storage.get('Classroom', cls_id)
    if classroom:
        for k, cls in classroom.items():
            if cls.sch_id == sch_id:
                cls.update(**update_dict)
                save_cls = storage.save()
            if save_cls is True:
                return jsonify({"code": "Updated"})
    return jsonify({"code" : "Error updating class"})

@app_views.route('/schools/<sch_id>/classrooms/<cls_id>', methods=['DELETE'], strict_slashes=False)
def delete_classroom(sch_id, cls_id):
    """Function to delete a classroom"""
    from models import storage

    info = request.get_json()
    pwd = info.get('password')
    check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": 'Wrong password'})
    cls = storage.get('Classroom', cls_id)
    if not cls:
        return jsonify({"code": "Class doesnt exist"})
    school = storage.get('School', sch_id)
    if not school:
        return jsonify({"code": "Invalid school id"})
    for k, sch in school.items():
        classes = sch.classes
    for cls in classes:
        if cls.id == cls_id:
            storage.delete(cls)
            save_cls = storage.save()
            if save_cls is True:
                school = storage.get('School', sch_id)
                for k, sch in school.items():
                    no_of_classes = sch.no_of_classes
                    sch.update(**{"no_of_classes": no_of_classes - 1})
                    storage.save()
                return jsonify({"code": "Deleted"})
    return jsonify({"code": "Error deleting class"})