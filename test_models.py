#!/usr/bin/python3
"""
Testing the models as i build
"""

from models.base_model import Base_model
from models.fees import Fees
from models.users import User
from models.schools import School
from models.classrooms import Classroom
from models.students import Student
from models import storage


def create_all():
    del_all()
    user_info = {'name': 'Abimbola Ogunbode', 'email':'omorinola5@gmail.com', 'password':'omorinola', 'phone_no': '08011164280'}
    user = User(**user_info)
    school = School('Potters Home', '21 Akinsola Dopemu Lagos', **{'user_id': user.id})
    cls_info = {'name':'Primary 1', 'class_teacher':'Mr Ogunbode', 'class_fees':50000, 'sch_id': school.id, 'user_id':user.id}
    new_class = Classroom(**cls_info)
    stu_info = {'name': 'Adebayo Tosin', 'cls_name': 'Primary 6', 'cls_id': new_class.id, 'sch_id': school.id, }
    new_student = Student(**stu_info)
    new_fee = Fees(**{'payer_name':'Taiwo Oyekan', 'student_id': new_student.id, 'stu_id': new_student.stu_id, 'amount': 35000, 'purpose': 'tuition'})
    storage.new(user)
    storage.new(school)
    storage.new(new_class)
    storage.new(new_student)
    storage.new(new_fee)
    try:
        storage.save()
    except Exception as e:
        print(e)

def del_all():
    db = storage.all()
    for k, v in db.items():
        if v.__class__.__name__ == 'User':
            try:
                storage.delete(v)
            except Exception as e:
                print(e)
    storage.save()

def print_all():
    db = storage.all()
    for k, v in db.items():
        name = v.__class__.__name__
        print('{}: '.format(name) + v.id)

def change_name(clss, name):
    db = storage.all(clss)
    for k, v in db.items():
        v.name = name
    storage.save()
    return (storage.all(clss))


#create_all()
"""u = storage.all('User')
for k, v in u.items():
    nu = v.update(**{'name': 'Sabinus Okonjo'})
print(nu)
print(v.name)
print(v.date_created)
print(v.date_updated)
#del_all()
#print_all()"""

u = storage.all('User')
for k, v in u.items():
    v.update(**{'name': 'Sabinus Okonjo'})
    storage.save()

print_all()
"""
nu = storage.all('User')
for k, v in nu.items():
    print(v.name)
    print(v.date_created)
    print(v.date_updated)"""

#del_all()
