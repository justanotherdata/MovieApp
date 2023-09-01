#from main import app, cache
from main.external_config.redis_client import redis_client
from main import celery
#from flask import Response
import time, os
from main.func import *
from main.external_config.webhook import *
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

#All celery tasks here
###############################################################################################################
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, dummy_send_daily_reminder.s(), name='Send reminder every 10 seconds')
    sender.add_periodic_task(crontab(hour=17, minute=30),send_daily_reminder.s())
    sender.add_periodic_task(crontab(day_of_month=1, hour=17, minute=30), send_daily_reminder.s())


#Sends email reminders to users everyday if they arenot logged in!
@celery.task(name='send_daily_reminder')
def send_daily_reminder():
    count = 0
    send_list = get_not_logged_in_today()
    for user in send_list():
        count=count+1
        Email = user('Email')
        Subject = 'Login Reminder'
        reminder_message = f"Don't forget to complete the task today! user - {count} - {user}"
        send_email(email = Email, subject = Subject, body = reminder_message)  
    return 'All msgs_sent'

#Dummy reminder for gchat every 10 sec
@celery.task(name='dummy_send_daily_reminder')
def dummy_send_daily_reminder():
    webhook_url = os.environ.get("webhook_url")
    reminder_message = f"Don't forget to complete the task today!"
    send_google_chat_message(webhook_url, reminder_message) 
    return 'msg_sent on googlechat'


#Sending emails for cancellation, bookings etc.
@celery.task(name='send')
def send(email, subject, body):
    email_status = send_email(email, subject, body)
    return email_status

#Sending reports monthly to the users
@celery.task(name='send_monthly_report')
def send_monthly_report():
    data = get_user_data() #This function gets user data of all users.

    for user in data:
        
        email = user['Email']
        subject = 'Your Monthly Report'
        body = f"<h1>Hello {user['Name']}! </h1> <p>Last Month you booked {user['num_of_Tickets_booked']} tickets in {user['num_of_shows_booked']} show. You also cancelled {user['num_of_Cancellations_made']} tickets.</P>"
        send_email(email, subject, body, is_html=True)
        print('email sent')
    return 'all emails sent'

@celery.task(name='download_report')
def download_user_report(id):
    #time.sleep(2)
    data = get_theatre_data_for_csv(id)
    
    csv_content = generate_csv(data)

    redis_client.setex(f'csv_{id}', 3600, csv_content) #Saving the file in redis-server for 1hour.
    
    
##############################################################################################################
#Celery Task Just to check functionality
@celery.task(name='my_first_celery.task')
def reverse(string):
    time.sleep(3)
    return string[::-1]





