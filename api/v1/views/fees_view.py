#!/usr/bin/python3
"""
Module to handle all classroom requests
"""

from api.v1.views import app_views
from flask import request, jsonify
from flask_login import current_user


@app_views.route('/schools/<sch_id>/students/<stu_id>/fees', methods=['GET'], strict_slashes=False)
def get_student_payments(sch_id, stu_id):
    """Function to get all payments made by a student"""
    from models import storage

    school = storage.get('School', sch_id)
    if not school:
        return "Invalid sch id"
    new_dict = {}
    student = storage.get('Student', stu_id)
    if student:
        for k, stu in student.items():
            if stu.sch_id == sch_id:
                fees = stu.fees
                for fee in fees:
                    new_dict[fee.id] = fee
                return new_dict
    return "Student doesnt exist in this school"

@app_views.route('/schools/<sch_id>/classrooms/<cls_id>/fees', methods=['GET'], strict_slashes=False)
def get_class_payment(sch_id, cls_id):
    """Function to get all fees paid in a class"""
    from models import storage

    school = storage.get('School', sch_id)
    if not school:
        return "Invalid school id"
    new_dict = {}
    classroom = storage.get('Classroom', cls_id)
    if not classroom:
        return "Invalid classroom id"
    for k, cls in classroom.items():
        if cls.sch_id == sch_id:
                students = cls.students
                for student in students:
                    fees = student.fees
                    for fee in fees:
                        new_dict[fee.id] = fee
                return new_dict
    return "Student doesnt exist in this school"

@app_views.route('/schools/<sch_id>/fees', methods=['GET'], strict_slashes=False)
def get_sch_payment(sch_id):
    """Function to get fees paid in a school"""
    from models import storage

    school = storage.get('School', sch_id)
    if not school:
        return "Invalid school id"
    new_dict = {}
    for k, sch in school.items():
        classes = sch.classes
        for cls in classes:
            students = cls.students
            for stu in students:
                fees = stu.fees
                for fee in fees:
                    new_dict[fee.id] = fee
        return new_dict
    return "Student doesnt exist in this school"

@app_views.route('/schools/<sch_id>/students/<stu_id>/fees', methods=['POST'], strict_slashes=False)
def create_student_payment(sch_id, stu_id):
    """Function to create a payment for a student"""
    from models import storage
    from models.fees import Fees
    from api.v1.views.auth import bcrypt

    info = request.get_json()
    a = payer_name = info.get('payer_name')
    b = amount = int(info.get('amount'))
    c = purpose = info.get('purpose')
    pwd = info.get('password')
    fee_info = {}
    fee_info['payer_name'] = payer_name
    fee_info['amount'] = amount
    fee_info['purpose'] = purpose
    fee_info['student_id'] = stu_id
    if not (a and b and c and pwd):
        return jsonify({'code': "Invalid credentials"})
    check_user = check_user = bcrypt.check_password_hash(current_user.password, pwd)
    if not check_user:
        return jsonify({"code": "Wrong password"})
    school = storage.get("School", sch_id)
    if not school:
        return jsonify({"code": "Invalid school id"})
    student = storage.get('Student', stu_id)
    if not student:
        return jsonify({"code": "Invalid student"})
    new_fee = Fees(**fee_info)
    save_fee = storage.save()
    if save_fee is True:
        for k, stu in student.items():
            current_fee = stu.fees_paid
            new = current_fee + amount
            stu.update(**{"fees_paid": new})
            storage.save()
            cls_id = stu.cls_id
        student_class = storage.get('Classroom', cls_id)
        for k, cls in student_class.items():
            current_cls_fee = cls.fees_paid
            new_cls_fee = amount + current_cls_fee
            cls.update(**{"fees_paid": new_cls_fee})
            storage.save()
        for k, sch in school.items():
            current_sch_fee = sch.fees_paid
            new_sch_fee = current_sch_fee + amount
            sch.update(**{"fees_paid": new_sch_fee})
            storage.save()
        return jsonify({"code": "Success"})
    else:
        return jsonify({"code": "Error making payment"})


@app_views.route('/schools/<sch_id>/students/<stu_id>/fees/<fee_id>', methods=['PUT'], strict_slashes=False)
def update_student_payment(sch_id, stu_id, fee_id):
    """Function to update a payment"""
    from models import storage

    if request.headers.get('Content-Type') != "application/json":
        return "Invalid content type"
    try:
        fee_info = request.get_json()
    except Exception:
        return "Invalid data format"
    school = storage.get('School', sch_id)
    if not school:
        return "Invalid school id"
    student = storage.get('Student', stu_id)
    if not student:
        return "Invalid student id"
    fee = storage.get('Fees', fee_id)
    if not fee:
        return "Invalid fee id"
    for k, f in fee.items():
        f.update(**fee_info)
        storage.new(f)
        save_update = storage.save()
        if save_update is True:
            return "Payment updated!"
    return "Error updating payment"

@app_views.route('/schools/<sch_id>/students/<stu_id>/fees/<fee_id>', methods=['DELETE'], strict_slashes=False)
def delete_student_payment(sch_id, stu_id, fee_id):
    """Function to delete a student payment"""
    from models import storage

    school = storage.get('School', sch_id)
    if not school:
        return "Invalid school id"
    student = storage.get('Student', stu_id)
    if not student:
        return "Invalid student id"
    fee = storage.get('Fees', fee_id)
    if not fee:
        return "Invalid fee id"
    for k, f in fee.items():
        storage.delete(f)
        save_update = storage.save()
        if save_update is True:
            return "Payment deleted!"
    return "Error deleting payment"