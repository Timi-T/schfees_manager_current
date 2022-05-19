#!/usr/bin/python3
"""
create blueprint for the flask app
and import all the views when this folder is initiated
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.user_view import *
from api.v1.views.school_view import *
from api.v1.views.classroom_view import *
from api.v1.views.student_view import *
from api.v1.views.fees_view import *