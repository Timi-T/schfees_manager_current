#!/usr/bin/python3
"""
Module to handle all classroom requests
"""

from api.v1.views import app_views
from flask import request, jsonify
from flask_login import current_user


@app_views.route('/schools/<sch_id>/students', methods=['GET'], strict_slashes=False)
def get_students(sch_id):
    """Function to get all students in a school"""
    from models import storage

    schools = current_user.schools
    for sch in schools:
        if sch.id == sch_id:
            classes = sch.classes
    new_dict = {}
    for cls in classes:
        students = cls.students
        for stu in students:
            student_class = storage.get('Classroom', stu.cls_id)
            for k, stu_cls in student_class.items():
                fees_expected = stu_cls.fees_expected
            fees_percent = stu.fees_paid / fees_expected
            stu_dict = stu.to_dict()
            stu_dict['fees_percent'] = int(fees_percent * 100)
            new_dict[stu.id] = stu_dict
    return new_dict

@app_views.route('/schools/<sch_id>/students/<stu_id>', methods=['GET'], strict_slashes=False)
def get_student(sch_id, stu_id):
    """Function to get a student from a school"""
    from models import storage

    schools = current_user.schools
    for sch in schools:
        if sch.id == sch_id:
            classes = sch.classes
    new_dict = {}
    student = storage.get('Student', stu_id)
    if student:
        for k, stu in student.items():
            if stu.sch_id == sch_id:
                student_class = storage.get('Classroom', stu.cls_id)
                for k, stu_cls in student_class.items():
                    fees_expected = stu_cls.fees_expected
                fees_percent = stu.fees_paid / fees_expected
                stu_dict = stu.to_dict()
                stu_dict['fees_percent'] = int(fees_percent * 100)
                new_dict[stu.id] = stu_dict
                return new_dict
    return jsonify({"code": "Student doesnt exist in this school"})

@app_views.route('/schools/<sch_id>/students', methods=['POST'], strict_slashes=False)
def create_student(sch_id):
    """Function to create a new student in a school"""
    from models import storage
    from models.students import Student
    from api.v1.views.auth import bcrypt

    info = request.get_json()
    stu_info = {}
    a = stu_info['name'] = info.get('name')
    b = stu_info['age'] = info.get('age')
    c = stu_info['sex'] = info.get('sex')
    d = stu_info['parent_phone'] = info.get('parent_phone')
    e = stu_info['cls'] = info.get('cls')
    f = stu_info['cls_id'] = info.get('cls_id')
    stu_info['sch_id'] = sch_id
    pwd = info.get('password')
    if not (a and b and c and d and e and f and pwd and sch_id):
        return jsonify({"code": "Invalid data"})
    check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": 'Wrong password'})
    school = storage.get('School', sch_id)
    if not school:
        return jsonify({"code": "Invalid school id"})
    cls = storage.get('Classroom', stu_info['cls_id'])
    if not cls:
        return jsonify({"code": "Invalid class id"})
    for k, sch in school.items():
        students = sch.students
    for stu in students:
        if stu.name == stu_info['name']:
            return jsonify({"code": "Student exists"})
    new_student = Student(**stu_info)
    save_stu = storage.save()
    if save_stu is True:
        for k, v in school.items():
            stu_count = v.no_of_students
            v.update(**{"no_of_students": stu_count + 1})
            storage.save()
        for k2, v2 in cls.items():
            stu_count = v2.no_of_students
            v2.update(**{"no_of_students": stu_count + 1})
            storage.save()
        return jsonify({"code": "Created"})
    else:
        return jsonify({"code": "Post failed"})

@app_views.route('/schools/<sch_id>/students/<stu_id>', methods=['PUT'], strict_slashes=False)
def update_student(sch_id, stu_id):
    """Function to update a student"""
    from models import storage
    from api.v1.views.auth import bcrypt

    info = request.get_json()
    pwd = info.get('password')
    check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": "Wrong password"})
    a = name = info.get('name').replace('_', ' ')
    b = age = info.get('age')
    c = sex = info.get('sex')
    d = parent_phone = info.get('parent_phone')
    if not a and b and c and d:
        return jsonify({"code": "Invalid credentials"})
    update_dict = {}
    update_dict['name'] = name
    update_dict['age'] = age
    update_dict['sex'] = sex
    update_dict['parent_phone'] = parent_phone
    school = storage.get('School', sch_id)
    if not school:
        return jsonify({"code": "Invalid school id"})
    student = storage.get('Student', stu_id)
    if not student:
        return jsonify({"code": "Invalid student id"})
    for k, stu in student.items():
        if stu.id == stu_id and stu.sch_id == sch_id:
            stu.update(**update_dict)
            save_stu = storage.save()
            if save_stu is True:
                return jsonify({"code": "Updated"})
    return jsonify({"code": "Error updating student"})
    

@app_views.route('/schools/<sch_id>/students/<stu_id>', methods=['DELETE', 'POST'], strict_slashes=False)
def delete_student(sch_id, stu_id):
    """Function to delete a student from a school"""
    from models import storage
    from api.v1.views.auth import bcrypt

    info = request.get_json()
    pwd = info.get('password')
    check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": "Wrong password"})
    school = storage.get('School', sch_id)
    if not school:
        return "Invalid school id"
    student = storage.get('Student', stu_id)
    if not student:
        return "Invalid student id"
    for k, stu in student.items():
        if stu.id == stu_id and stu.sch_id == sch_id:
            storage.delete(stu)
            save_stu = storage.save()
            if save_stu is True:
                for k, sch in school.items():
                    no_of_sch_students = sch.no_of_students
                    new_number = no_of_sch_students - 1
                    sch.update(**{'no_of_students': new_number})
                    storage.save()
                cls = storage.get('Classroom', stu.cls_id)
                for k, v in cls.items():
                    current = v.no_of_students
                    new = current - 1
                    v.update(**{'no_of_students': new})
                    storage.save()
                return jsonify({"code": "Deleted"})
    return jsonify({"code": "Error deleting student"})