from flask import Blueprint
from apifairy import authenticate, body, response
from api import db

from api.models import Day
from api.auth import token_auth
from api.schemas import DaySchema
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

day = Blueprint('day', __name__)
day_schema = DaySchema()

@day.route('/day', methods=['POST'])
@authenticate(token_auth)
@body(day_schema)
@response(day_schema, 201)
def new(args):
    day = Day(**args)
    db.session.add(day)
    db.session.commit()
    return day

@day.route('/day-range', methods=['POST'])
@authenticate(token_auth)
@body(day_schema)
@response(day_schema, 201)
def new_range(args):
    print("args:", args)
    today = datetime.now()
    temp_calendar = calendar.Calendar()
    temp = {}
    month_count = 0
    while month_count < int(args['count_month']):
        day = today + relativedelta(months=+month_count)
        week_of_month = temp_calendar.monthdays2calendar(day.year, day.month)
        for week in week_of_month:
            for w in week:
                if w[0] != 0:
                    print(w)
            print('*'*30)
        # print(week_of_month)
        temp[day.strftime('%B')] = []
        month_count += 1
    print(temp)
    # day = Day(**args)
    # db.session.add(day)
    # db.session.commit()
    return args


# Сколько месяцев
# Сколько дней в неделю
# Начало месяца
