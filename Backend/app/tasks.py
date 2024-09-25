
from app import  celery
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from .mail import send_email



from datetime import datetime, timedelta


import os
import csv
import time 




@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=10, minute=24),
        test.s("Happy Mondays!"),
    )
    #monthly report
    sender.add_periodic_task(
        crontab(day_of_month='1', hour=23, minute=59),
        send_monthly_report.s()
    ),
    #daily remainder
    sender.add_periodic_task(
        crontab(hour=18, minute=00),
        send_daily_remainder.s()
    )


from .model import Booking, AdminAuth , Venue, Show

@celery.task
def send_monthly_report():
    data = get_booking_report_current_month()
    with open('monthly_bookings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    auth = AdminAuth.query.all()
    for a in auth:
        send_email("mad2project.ticketshow@gmail.com",a.email,"Monthly Report", "Please find the attached monthly report", "monthly_bookings.csv")
    





def get_booking_report_current_month():
    today = datetime.today()
    first_day_of_month = today.replace(day=1,month=today.month-1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = first_day_of_month.replace(month=today.month) - timedelta(days=1)

    bookings = Booking.query.filter(Booking.booking_time >= first_day_of_month,
                                Booking.booking_time <= last_day_of_month).all()
    all_bookings = [
        ["Booking ID", "Show Name", "Booking Time", "Seats", "Rating", "Venue Name", "Venue Location", "Venue Place"]
    ]
    for b in bookings:
        show = Show.query.filter_by(id=b.show_id).first()
        venue = Venue.query.filter_by(id=show.venue_id).first()
        all_bookings.append([
            b.id,
            show.name,
            b.booking_time,
            b.seats,
            b.rating,
            venue.name,
            venue.location,
            venue.place
        ])
    return all_bookings



@celery.task
def send_daily_remainder():
    auth = AdminAuth.query.all()
    for a in auth:
        if a.last_login == None:
            continue
        if a.last_login.date() == datetime.today().date():
                continue
        
        send_email("mad2project.ticketshow@gmail.com",a.email,"Daily Reminder", "Please visit the admin dashboard, You are not visited today")













@celery.task
def add(x, y):
    print("add")
    return x + y

@celery.task
def test(arg):
    print("test")
    print(arg)
    return arg

@celery.task
def a_20_sec_task():
    print("20 sec task")
    time.sleep(20)
    print("20 sec task done")