from twilio.rest import Client
import requests
from main import app, db, cache

import numpy as np
from main.models import users, Movies, Theatres, Shows, Bookings
from flask_login import  current_user
import smtplib, os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask import jsonify, request
from datetime import datetime

from weasyprint import HTML
from fpdf import FPDF
from jinja2 import Template
#from main.redis_client import redis_client
from email.message import EmailMessage

import csv
from io import StringIO
import jwt
from functools import wraps




load_dotenv()

#cached functions
###############################################################################################################
@cache.cached(timeout=3000) #change timeout value to your liking.
def get_movie_list(city):
    movie_list=[]
    theatres = Theatres.query.filter_by(The_Location = city).all()
    if len(theatres)>0:
        for theatre in theatres:
            movies = get_movie_id(theatre.The_Id) #This function is returning unique movie ids which have active shows
            
            for mov in movies:
                movie = Movies.query.filter_by(Mov_Id = int(mov)).first()
                x= {}
                if movie.Mov_Status:
                    #print('goes here')
                    x['id'] = movie.Mov_Id
                    x['mov_name'] = movie.Mov_Name
                    x['mov_rating'] = movie.Mov_Rating
                    if x['id']:
                        movie_list.append(x)
                        #print(movie_list)

                else:
                    pass
                
            
              
        unique_list =  get_unique_dicts(movie_list)
        print(unique_list)
        return jsonify(unique_list)
    
    else:
        return jsonify({'message': 'Error', 'details': 'No movies in this city!'})

@cache.cached(timeout=3000)
def get_all_theatre_city():
    theatres = Theatres.query.all()
    theatre_list = []
    for theatre in theatres:
        if len(theatre_list)==0:
            theatre_list.append(theatre.The_Location)
        else:
            if theatre.The_Location in theatre_list:
                pass
            else:
                theatre_list.append(theatre.The_Location)
    return jsonify(theatre_list)

################################################################################################################
    
def get_unique_dicts(dictionary_list):
    seen_ids = set()
    unique_dicts = []

    for dictionary in dictionary_list:
        if 'id' in dictionary:
            if dictionary['id'] not in seen_ids:
                seen_ids.add(dictionary['id'])
                unique_dicts.append(dictionary)

    return unique_dicts

def Unique(list1):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list


def movie_theatre():
    with app.app_context():
        movie_list = []
        theatre_list = []
        if current_user:
            movies = Movies.query.filter_by(Created_By = current_user.UID).all()
            theatres = Theatres.query.filter_by(Created_By = current_user.UID).all()
            for movie in movies:
                if movie.Mov_Status:
                    movie_list.append(movie.Mov_Name)
            for theatre in theatres:
                if theatre.The_Status:
                    theatre_list.append(theatre.The_Name)

    return movie_list, theatre_list

def get_not_logged_in_today():
    today_date = datetime.now().date()
    userlist = users.query.all()
    send_list = []
    for user in userlist:
        lastlogindate = user.last_login.date()
        if lastlogindate == today_date and user.Role == 'User':
            send_list.append(user.Email)
    return send_list

def get_active_movies_shows(Theatre_Id):
    with app.app_context():
        movies = []
        showlist = []
        shows = Shows.query.filter_by(The_Id = Theatre_Id).all()
        for show in shows:
            if show.Show_Status:
                movies.append(show.Mov_Id)
                showlist.append(show.Show_Id)
        print(movies)
        print(showlist)

    return movies, showlist


def get_movie_id(theatre_id):
    movie_ids = []
    movies = Shows.query.filter_by(The_Id = theatre_id).all()
    for movie in movies:
        if movie.Show_Status:
            movie_ids.append(movie.Mov_Id)

    return np.unique(movie_ids)
    
def get_show_id(movie_id):
    with app.app_context():
        show_ids = []
        if current_user:
            shows = Shows.query.filter_by(Mov_Id = movie_id).all()
            for show in shows:
                if show.Show_Status:
                    show_ids.append(show.Show_Id)
    return show_ids

#Returns List of active bookings    
def get_booking_id(show_id):
    with app.app_context():
        booking_ids = []
        if current_user:
            bookings = Bookings.query.filter_by(Show_Id = show_id).all()
            for booking in bookings:
                if booking.Booked_Status and not booking.Cancellation_Status:
                    booking_ids.append(booking.Book_Id)
    return booking_ids


def cancel_show(Booking_Id, reason):
    with app.app_context():
        cancel_status = False
        user_email = []
        if current_user:
            bookings = Bookings.query.filter_by(Book_Id=Booking_Id).first()
            if bookings and bookings.Booked_Status:
                #id = bookings.UID
                email = bookings.users.Email
                user_email.append(email)
                bookings.Cancellation_Status = True
                bookings.Reason = reason
                db.session.commit()
                cancel_status = True
            elif not bookings.Booked_Status:
                bookings.Cancellation_Status = True
                db.session.commit()
                cancel_status = True

        return cancel_status, user_email




              
#Setting up webhooks
def send_google_chat_message(webhook_url, message):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
    }
    payload = {
        'text': message,
    }
    response = requests.post(webhook_url, json=payload, headers=headers)
    return response.status_code == 200


#Setting up twilio for msg service
def send_sms_reminder(to_phone_number, message):
    client = Client(os.environ.get("account_sid_twilio"), os.environ.get("auth_token_twilio"))
    client.messages.create(to=to_phone_number, from_=os.environ.get("from_phone_number_twilio"), body=message)



def format_report(template_file, data={}):
    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data)

def generate_pdf_report(user_data):
    message = format_report('pdf_report_user.html' , data=user_data)
    html = HTML(string=message)
    file_name = str(user_data['Name']) + ".pdf"
    print(file_name)
    html.write_pdf(target = file_name)



def num_tkts_shows_booked(id):
    tkt_count = 0
    show_count = 0
    cancel_count = 0
    bookings = Bookings.query.filter_by(UId = id).all()
    for booking in bookings:
        show_count = show_count+1
        tkt_count = tkt_count + booking.Num_Of_Seats
        if booking.Cancellation_Status and not booking.Reason:
            cancel_count = cancel_count + booking.Num_Of_Seats

    return tkt_count, show_count, cancel_count


def get_user_data():
    user_list = users.query.all()
    list_to_use = []
    for user in user_list:
        x={}
        if user.Role == 'User':
            x['Name'] = user.Name
            x['Email'] = user.Email
            user_id = user.UID

            tkt_count, show_count, cancel_count = num_tkts_shows_booked(user_id)
            x['num_of_shows_booked'] = show_count
            x['num_of_Tickets_booked'] = tkt_count
            x['num_of_Cancellations_made'] = cancel_count

            list_to_use.append(x)
    return list_to_use


def send_email(recipient_email, subject, body, is_html=False):

     # Set up the SMTP server for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_status = ''
    sender_email = os.environ.get("EMAIL")
    sender_password = os.environ.get("PASSWORD")

    # Create a MIMEMultipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Choose the content type based on the is_html parameter
    content_type = "html" if is_html else "plain"
    body_part = MIMEText(body, content_type)
    message.attach(body_part)

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)  # Replace with your SMTP server and port
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        email_status = 'sent'
        
    except Exception as e:
        #print("Error sending email:", str(e))
        email_status = 'not sent'

    return email_status


def generate_csv(data):
    output = StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=['Theatre_Id', 'Theatre_Name', 'Theatre_Location','Mov_Id', 'Movie_Name', 'Number Of Shows', 'Booked_Tickets', 'Total Cancellations'])
    csv_writer.writeheader()
    csv_writer.writerows(data)
    return output.getvalue()


def get_theatre_data_for_csv(user_id):
    shows = Shows.query.filter_by(Created_By = user_id).all()
    theatre_data = []
    movie_list = []

    for show in shows:
        x = {}
        x['Theatre_Id'] = show.The_Id
        x['Theatre_Name'] = show.theatre.The_Name
        x['Theatre_Location'] = show.theatre.The_Location
        x['Movie_Name'] = show.movie.Mov_Name
        x['Mov_Id'] = show.Mov_Id
        movie_list.append(show.Mov_Id)
        theatre_data.append(x)

    final_movie_list = np.unique(movie_list)
    movie_data = []

    for movie in final_movie_list:
        data = get_shows_booked_cancellation(int(movie))
        movie_data.append(data)

    for i in theatre_data:
        for j in movie_data:
            if i['Mov_Id'] == j['Mov_Id']:
                i['Number Of Shows'] = j['show_count']
                i['Booked_Tickets'] = j['booking_count']
                i['Total Cancellations'] = j['cancellation_count']

    return theatre_data



def get_shows_booked_cancellation(movie_id):
    shows = Shows.query.filter_by(Mov_Id = movie_id).all()
    show_list = []
    show_count = 0
    booking_count = 0
    cancellation_count = 0
    
    
    if len(shows) > 0:
        x={}
        x['Mov_Id'] = movie_id
        for show in shows:
            show_count = show_count+1
            show_list.append(show.Show_Id)
            
        x['show_count'] = show_count

        for show in show_list:
            bookings = Bookings.query.filter_by(Show_Id = show).all()
            for booking in bookings:
                if booking.Booked_Status and booking.Cancellation_Status:
                    cancellation_count = cancellation_count + booking.Num_Of_Seats
                elif booking.Booked_Status and not booking.Cancellation_Status:
                    booking_count = booking_count + booking.Num_Of_Seats

        x['booking_count'] = booking_count
        x['cancellation_count'] = cancellation_count
        

    return x


@app.route('/moviedata')
def moviedata():
    #id = current_user.UID
    movies, theatres = movie_theatre()
    return movies

@app.route('/theatredata')
def theatredata():
    #id = current_user.UID
    movies, theatres = movie_theatre()
    return theatres


def auth_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
        if not token:
            return jsonify({"message": 'Error', 'details': "Token is missing"}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            current_user = users.query.filter_by(UID = data['id']).first()
        except:
            return jsonify({"message": 'Error', 'details': "Token is invalid or no longer active."}), 401
        if not current_user:
            return jsonify({"message": 'Error', 'details': "This token has deprecated! Please try again with a valid new token"})
        else:
            if not current_user.isactive:
                print("Does this work here!")
                return jsonify({"message":'Error', 'details': "You have been logged out! Please login and try again!"})
            return f(current_user, *args, **kwargs)
    
    return decorated