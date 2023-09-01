#Making Necessary Imports
from flask import request, render_template, jsonify, make_response, redirect, url_for, flash, request
from sqlalchemy.exc import IntegrityError
from main.tasks import *
from main.func import *
from main import app, db, bcrypt
from main.models import users, Movies, Theatres, Shows, Bookings
from flask_cors import cross_origin


#Functinality based Imports
from datetime import datetime, timedelta
import os
from time import perf_counter_ns
import jwt
from functools import wraps


#Cached API
#Checked with postman     
@app.route('/get_movies/<string:city>')
@cross_origin()
def get_movies(city):
    data = get_movie_list(city)
    return data


@app.route('/all_cities')
@cross_origin()
def all_cities():
    data = get_all_theatre_city()
    return data

#cached apis end above this line


#Checked Using Postman
@app.route('/login_user', methods=['POST'])
@cross_origin()
def login_user():
    data = request.get_json()
    
    if request.method == 'POST':
        if not data or not data['email'] or not data['password']:
            #return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})
            return jsonify({'message': 'Error', 'details': 'Please enter all the required data'})
        
        user = users.query.filter_by(Email = data['email']).first()

        if user and user.Role != 'User':
           return jsonify({'message': 'Error', 'details': 'You are not logging in as a user!'})
        
        if not user:
            #return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})
            return jsonify({'message': 'Error', 'details': 'user not found'})
        
        pwd_check = bcrypt.check_password_hash(user.Password, data['password'])
        if pwd_check:
            jwtoken = jwt.encode({'id': user.UID, 'exp' : datetime.utcnow() + timedelta(days=120)}, app.config['SECRET_KEY'], algorithm="HS256")
            user.isactive = True
            db.session.commit()
            return jsonify({'token': jwtoken, 'details': "User successfully logged in!"})
            #return jsonify({'token': jwtoken.decode(), 'message': "User successfully logged in!"})
        
        if not pwd_check:
            #return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})
            return jsonify({'message': 'Error', 'details': 'Password not verified'})
        
    

#Checked using Postman
@app.route('/logout_user')
@cross_origin()
@auth_token_required
def logout(current_user):
    current_user.isactive = False
    db.session.commit()
    return jsonify({"message": "You have been logged out!"})


#Checked using Postman
@app.route('/get_current_user')
@cross_origin()
@auth_token_required
def get_current_user(current_user):
    current_user.last_login = datetime.now()
    db.session.commit()
    return jsonify({'user_id': current_user.UID, 'user_name': current_user.Name, 'email': current_user.Email})


#checked using Postman
@app.route('/create_user', methods=['POST'])
@cross_origin()
def create_user():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    name = data['name']
    email = data['email']
    try:
        user = users(Name = name, Email = email, Password = hashed_password, Role='User')
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message":'Error','details': "Email Id Already in use. Pick a different Email Id.."})
    jwtoken = jwt.encode({'id': user.UID, 'exp' : datetime.utcnow() + timedelta(days=120)}, app.config['SECRET_KEY'], algorithm="HS256")
    user.isactive = True
    db.session.commit()
    return jsonify({'token': jwtoken, 'message': "User successfully Created and logged in!"})
    


#Checked with postman
@app.route('/update_user', methods=['PUT'])
@cross_origin()
@auth_token_required
def update_user(current_user):
    data = request.get_json()
    updated_name = data['name']
    updated_email = data['email']
    if current_user:
        try:
            current_user.Name = updated_name
            current_user.Email = updated_email
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'error', 'details': 'Email Id Already in use. Pick a different Email Id..'})
    else:
        return jsonify({'message':'error', 'details':'Your Login has expired. Please login and try again!'})    
    return jsonify({'message':'success', 'details':'Profile Successfully Updated!'})


#checked with postman
@app.route('/change_password', methods=['PUT'])
@cross_origin()
@auth_token_required
def change_password(current_user):
    token = None
    if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if current_user:
               
                link = f'127.0.0.1:5000/secure_link/{current_user.UID}'
               
                subject = 'Password Change Email'
                body = f'Please use the below link to change your password! {link}'
                result = send.delay('m.nitish1995@gmail.com', subject, body)
                if result:
                    return jsonify({'message':'Success', 'details':'A password change email has been sent to you!'})
                else:
                    return jsonify({'message':'Error', 'details':'Password change email could not be sent(Celery Issue). Please try again after sometime!'})
            
            else:
                return jsonify({'message':'Error', 'details':'User not verified. Please try again after logging in!'})

#checked with postman and html-form
@app.route('/secure_link/<int:id>', methods=['GET', 'POST'])
def secure_link(id):
    if request.method == 'GET':
        return render_template('password_change.html')
    else:
        curr_password = request.form.get('curr_password')
        new_password = request.form.get('new_password')
        user = users.query.filter_by(UID = id).first()
        pwd_check = bcrypt.check_password_hash(user.Password, curr_password)
        if pwd_check:
            new_hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            try:
                user.Password = new_hashed_password
                db.session.commit()
                result = send.delay('m.nitish1995@gmail.com', 'Password Changed', 'Your current password has been changed!')
                if result:
                    return jsonify({'message':'Success', 'details':'Your password has been changed!'})
                else:
                    return jsonify({'message':'Error', 'details':'Your password has been updated but we were unable to send you an Email.'})

            except:
                db.session.rollback()
                return jsonify({'message':'Error', 'details':'Your password was not changed due to some db error!'})
            
        else:
            return jsonify({'message':'Error', 'details':'Your current password was wrong. Please refresh the page and try again with the correct password!'})
  


#Checked with postman
@app.route('/all_bookings')
@cross_origin()
@auth_token_required
def all_bookings(current_user):
    if current_user:
        user_list = []
        id = current_user.UID
        tickets = Bookings.query.filter_by(UId = id).all()
        for ticket in tickets:
            
            x = {}
            if ticket.Booked_Status:
                
                x['id'] = ticket.Book_Id
                show_id = ticket.Show_Id
                show = Shows.query.filter_by(Show_Id = show_id).first()
                x['mov_name'] = show.movie.Mov_Name
                x['mov_rating'] = show.movie.Mov_Rating
                x['the_name'] = show.theatre.The_Name
                x['the_id'] = show.theatre.The_Id
                x['timing'] = show.Show_Time
                x['num_of_tkts'] = ticket.Num_Of_Seats
                if not ticket.Cancellation_Status:
                    x['active_status'] = True
                else:
                    x['active_status'] = False
                user_list.append(x)
                
        if(len(user_list) > 0):    
            return jsonify(user_list)
        else:
            return jsonify({'message': 'Success', 'details': 'No bookings for this user from else!'})
    
    else:
        return jsonify({'message': 'Error', 'details': 'The user is not authenticated. Please try again after logging in!'})


#Checked with postman  
@app.route('/cancel_booking', methods=['POST'])
@cross_origin()
@auth_token_required
def cancel_booking(current_user):
    if current_user:
        data = request.get_json()
        booking_id = data['booking_id']

        user_id = current_user.UID

        booking = Bookings.query.filter_by(Book_Id = booking_id).first()
        show = Shows.query.filter_by(Show_Id = booking.Show_Id).first()
        cancelled_num_of_seats = booking.Num_Of_Seats

        if booking.Booked_Status and booking.UId == user_id and not booking.Cancellation_Status:
            booking.Cancellation_Status = True
            show.Booked_Seats = show.Booked_Seats - cancelled_num_of_seats
            db.session.commit()
            body = f'Your booking for {cancelled_num_of_seats} seats for show {show.movie.Mov_Name} has been successfully cancelled!'
            result = send.delay('m.nitish1995@gmail.com', 'Booking Cancellation Email', body = body)
            if result:
                return jsonify({'message': 'Success', 'details': 'Your tkts have been cancelled! An Email was sent'})
            else:
                return jsonify({'message': 'Success', 'details': 'Your tkts have been cancelled! We were not able to send email(Celery issue)'})
        
        else:
            return jsonify({'message': 'Error', 'details': 'Some form of authentication error! Tkts were not cancelled'})

    else:
        return jsonify({'message': 'Error', 'details': 'User was not verified!'})


@app.route('/user/get_show/<int:movie_id>/<city>')
@cross_origin()
def user_get_show(movie_id, city):
    result = {}
    movie = Movies.query.filter_by(Mov_Id = movie_id).first()
    if movie and movie.Mov_Status:
        shows = Shows.query.filter_by(Mov_Id = movie_id).all()
        if len(shows) > 0:
            result['Mov_Name'] = movie.Mov_Name
            result['Mov_Rating'] = movie.Mov_Rating
            show_details = []
            theatre_list = []
            for show in shows:
                if show.Show_Status and show.theatre.The_Location == city:
                    theatre = show.theatre.The_Id
                    if theatre in theatre_list:
                        pass
                    else:
                        theatre_list.append(theatre)

                else:
                    print('First debugging message from show in shows block')


            for theatre in theatre_list:
                x = {}
                thea = Theatres.query.filter_by(The_Id=theatre).first()
                if thea.The_Status and thea.The_Location == city:
                    x['Theatre_Id'] = theatre
                    x['Theatre_Name'] = thea.The_Name

                    running_shows = Shows.query.filter_by(The_Id = theatre).all()
                    all_show = []
                    if len(running_shows)>0:
                        for show in running_shows:
                            if show.Mov_Id == movie_id and show.Show_Status:
                                available_seats = show.Total_Seats - show.Booked_Seats
                                if available_seats > 0:
                                    y = {}
                                    y['available'] = available_seats
                                    y['show_id'] = show.Show_Id
                                    y['time'] = show.Show_Time

                                    all_show.append(y)

                                else:
                                    print('Debugging test running_shows block 3')

                            else:
                                print('Debugging test running_shows block 2')

                    else:
                        print('Debugging test running_shows block 1')

                    if len(all_show)>0:
                        x['all_show'] = all_show
                        show_details.append(x)
                    else:
                        print('Debugging test len(all_shows) block 1')

            if len(show_details)>0:
                result['show_details'] = show_details

                return result

            else:
                return jsonify({'message': 'Error', 'details': 'No show for this movie_id'})


            
            
            

        else:
            return jsonify({'message':'Error', 'details':'No active Show for this movie id in your city!'})


    else:
        return jsonify({'message':'Error', 'details':'The movie is not active!'})
 


@app.route('/user/get_movie/<int:the_id>/<city>')
@cross_origin()
def user_get_movie(the_id, city):
    shows = Shows.query.filter_by(The_Id = the_id).all()
    if len(shows)> 0:
        result_list = []
        for show in shows:
            if show.Show_Status and show.theatre.The_Location == city and show.movie.Mov_Status:
                x = {}
                x['id'] = show.movie.Mov_Id
                x['mov_name'] = show.movie.Mov_Name
                x['mov_rating'] = show.movie.Mov_Rating
                x['city'] = show.theatre.The_Location

                result_list.append(x)

            else:
                print('Debugging pass 1')
        if len(result_list)>0:
            final_result_list = get_unique_dicts(result_list)
            return jsonify(final_result_list)
        else:
            return jsonify({'message': 'Error', 'details': 'No Movie in this theatre in your city!'})

    else:
        return jsonify({'message': 'Error', 'details': 'No movies in this theatre'})

#tested With Postman
@app.route('/booking_cnf', methods=['POST'])
@cross_origin()
@auth_token_required
def booking_cnf(current_user):
    data = request.get_json()
    show_id = data['show_id']
    num_of_tkts = data['num_of_tkts']
    price = data['price']

    user_id = current_user.UID
    show = Shows.query.filter_by(Show_Id = show_id).first()

    total_seats = show.Total_Seats
    booked_seats = show.Booked_Seats
    available_seats = total_seats - booked_seats
    

    if int(num_of_tkts) <= available_seats and current_user.Role == 'User':
        collection = int(price) * int(num_of_tkts)
        booking = Bookings(UId = user_id, Show_Id = show_id, Num_Of_Seats = num_of_tkts, Booked_Status=1, Collection=collection)
        db.session.add(booking)
        show.Booked_Seats = booked_seats + int(num_of_tkts)
        
        db.session.commit()
        body = f'{num_of_tkts} tkts for {show.movie.Mov_Name} has been booked.'
        result = send.delay('m.nitish1995@gmail.com', 'Booking Confirmation', body)
        if result:
            return jsonify({'message': 'Success', 'details': 'Tkt Booked! A confirmation email will be sent!'})
        else:
            return jsonify({'message': 'Success', 'details': 'Your tkt was booked but we were unable to send you the confirmation Email!'})
        
    else:
        return jsonify({'message': 'Error', 'details': 'Number of seats you tried to book exceeds the available number of seats!'})

#tested with postman
@app.route('/search_movies/<search_with>', methods=['GET'])
def search_movies(search_with):
    data = Movies.query.filter(Movies.Mov_Name.startswith(search_with)).all()
    result = []
    if data:
        for movie in data:
            r={}
            r['id'] = movie.Mov_Id
            r['mov_name'] = movie.Mov_Name
            r['mov_rating'] = movie.Mov_Rating

            result.append(r)
    else:
        return jsonify({'message': 'No movies by this name'})
    
    return jsonify(result)


#tested with postman
@app.route('/search_theatres/<search_with>', methods=['GET'])
def search_theatres(search_with):
    data = Theatres.query.filter(Theatres.The_Name.startswith(search_with)).all()
    result = []
    if data:
        for theatre in data:
            r={}
            r['id'] = theatre.The_Id
            r['name'] = theatre.The_Name
            result.append(r)

    else:
        return jsonify({'message': 'No theatres by this name'})
    
    
    
    return jsonify(result)

#tested with postman
@app.route('/search_city/<search_with>', methods=['GET'])
def search_city(search_with):
    data = Theatres.query.filter(Theatres.The_Location.startswith(search_with)).all()
    result = []
    if data:
        for theatre in data:
            r={}
            r['id'] = theatre.The_Id
            r['name'] = theatre.The_Name
            result.append(r)

    else:
        return jsonify({'message': 'No theatres in this city'})
    
    
    
    return jsonify(result)

#tested with postman
@app.route('/search_city_theatre/<search_with>', methods=['GET'])
def search_city_theatre(search_with):
    data = Theatres.query.filter(Theatres.The_Location.icontains(search_with) | Theatres.The_Name.icontains(search_with)).all()
    result = []
    count = 0
    if data:
        for theatre in data:
            if theatre.The_Status:
                movies = get_movie_id(theatre.The_Id)
                for movie in movies:
                    mov = Movies.query.filter_by(Mov_Id = int(movie)).first()
                    r={}
                    if mov.Mov_Status:
                        r['id'] = mov.Mov_Id
                        r['name'] = mov.Mov_Name
                        r['rating'] = mov.Mov_Rating
                        if len(result) == 0:
                            result.append(r)

                        else:
                            if result[count]['id'] == r['id']:
                                pass
                            else:
                                result.append(r)
                                count = count+1

    else:
        return jsonify({'message': 'No theatres in this city'})
    
    
    return jsonify(result)

#tested with postman
@app.route('/get_show_details/<int:show_id>')
def get_show_details(show_id):
    show = Shows.query.filter_by(Show_Id = show_id).first()
    if show:
        x = {}
        available_seats = show.Total_Seats - show.Booked_Seats
        x['available_seats'] = available_seats
        x['movie_name'] = show.movie.Mov_Name
        x['theatre_name'] = show.theatre.The_Name
        x['city'] = show.theatre.The_Location
        x['timing'] = show.Show_Time
        if available_seats >= 0.75 * (show.Total_Seats):
            x['price_per_tkt'] = 100
            x['label'] = 'Bargain Prices'
        elif 0.25 * (show.Total_Seats) <= available_seats < 0.75 * (show.Total_Seats):
            x['price_per_tkt'] = 200
            x['label'] = 'Users choice'
        else:
            x['price_per_tkt'] = 300
            x['label'] = 'Filling Super Fast'
        
        return jsonify(x)
    
    else:
        return jsonify({'message': 'Error', 'details': 'No Show with this show_id'})
    
##################################################################################################################

#Testing Routes
@app.route('/', methods = ['GET'])
@app.route('/home_user', methods=['GET'])
def home_user():
    return 'This will send the jsonfied data to the frontend. The view will be handled by Vue!'




    






