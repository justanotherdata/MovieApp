#Making necessary imports
from flask import request, Response, jsonify
from main import app, db, bcrypt
from main.external_config.redis_client import redis_client
#from main.forms import LoginForm, Create_Theatre, Create_Movies, Create_Show
from main.models import users, Movies, Theatres, Shows
from main.func import *
from main.tasks import *
from flask_cors import cross_origin
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError





#Basic routes
@app.route('/login_admin', methods=['POST'])
@cross_origin()
def login_admin():
    data = request.get_json()
    
    if request.method == 'POST':
        if not data or not data['email'] or not data['password']:
            
            return jsonify({'message': 'Error', 'details': 'Please enter all the required data'})
        
        user = users.query.filter_by(Email = data['email']).first()

        if user and user.Role != 'Admin':
           return jsonify({'message': 'Error', 'details': 'You are not logging in as a admin!'})
        
        if not user:
            
            return jsonify({'message': 'Error', 'details': 'Admin not identified'})
        
        pwd_check = bcrypt.check_password_hash(user.Password, data['password'])
        if pwd_check:
            jwtoken = jwt.encode({'id': user.UID, 'exp' : datetime.utcnow() + timedelta(days=120)}, app.config['SECRET_KEY'], algorithm="HS256")
            user.isactive = True
            db.session.commit()
            return jsonify({'token': jwtoken, 'details': "User successfully logged in!"})
            
        
        if not pwd_check:
            
            return jsonify({'message': 'Error', 'details': 'Password not verified'})


@app.route('/logout_admin')
@cross_origin()
@auth_token_required
def logout_admin(current_user):
    current_user.isactive = False
    db.session.commit()
    return jsonify({"message": "You have been logged out!"})


@app.route('/home_admin')
@cross_origin()
@auth_token_required
def home_admin(current_user):
    if(current_user):
        admin = users.query.filter_by(UID = current_user.UID).first()
        show_count = 0
        movie_count = 0
        theatre_count = 0
        booked_tkts = 0
        result_list=[]

        shows = admin.user_shows

        for show in shows:
            if show.Show_Status:
                show_count = show_count+1
                
                bookings = show.booked_shows
                for booking in bookings:
                    if booking.Booked_Status and not booking.Cancellation_Status:
                        booked_tkts = booked_tkts + booking.Num_Of_Seats
        result_list.append({'name': 'Shows', 'Count': show_count})
        result_list.append({'name': 'Bookings', 'Count': booked_tkts})

        movies= admin.user_movies
        for movie in movies:
            if movie.Mov_Status:
                movie_count = movie_count+1

        theatres = admin.user_theatres
        for theatre in theatres:
            if theatre.The_Status:
                theatre_count = theatre_count+1

        result_list.append({'name': 'Movies', 'Count': movie_count})
        result_list.append({'name': 'Theatres', 'Count': theatre_count})
        return jsonify(result_list)
    
    else:
        return jsonify({'message': 'Error', 'details': 'You are not loged in or your login has expired!'})
    

@app.route('/admin_bookings')
@cross_origin()
@auth_token_required
def admin_bookings(current_user):
    result_list = []
    message = ""

    if current_user:
        shows = Shows.query.filter_by(Created_By = current_user.UID).all()
        for show in shows:
            bookings = show.booked_shows
            for booking in bookings:
                
                x={}
                x['Booking_Id'] = booking.Book_Id
                x['Booked_By'] = booking.UId
                x['Theatre_Name'] = show.theatre.The_Name
                x['Movie_Name'] = show.movie.Mov_Name
                x['Location'] = show.theatre.The_Location
                x['Timing'] = show.Show_Time
                x['Num_of_seats'] = booking.Num_Of_Seats
                x['Cancellation_Status'] = booking.Cancellation_Status
                x['Cancellation_Reason'] = booking.Reason
                result_list.append(x)


    else:
        message = 'Your login has expired! Please login again!'

    if len(result_list)>0:
        return jsonify(result_list)
    
    else:
        if message:
            return jsonify({'message': 'Error', 'details': message})
        else:
            return jsonify({'message': 'Error', 'details': 'No bookings yet!'})


@app.route('/admin_theatres')
@cross_origin()
@auth_token_required
def admin_active_theatres(current_user):
    result_list = []
    if current_user:
        theatres = Theatres.query.filter_by(Created_By = current_user.UID).all()
        if len(theatres) > 0:
            for theatre in theatres:
                x= {}
                x['Theatre_Id'] = theatre.The_Id 
                x['Theatre_Name'] = theatre.The_Name  
                x['Theatre_Location'] = theatre.The_Location    
                x['Theatre_Status'] = theatre.The_Status

                result_list.append(x)

            return jsonify(result_list)
        
        else:
            return jsonify({'message': 'Error', 'details': 'No theatres have been created!'})

    else:
        return jsonify({'message': 'Error', 'details': 'You are not logged in!'})
    


@app.route('/admin_movies')
@cross_origin()
@auth_token_required
def admin_movies(current_user):
    result_list = []
    if current_user:
        movies = Movies.query.filter_by(Created_By = current_user.UID).all()
        if len(movies)>0:
            for movie in movies:
                x={}
                x['Mov_Id'] = movie.Mov_Id
                x['Mov_Name'] = movie.Mov_Name
                x['Mov_Status'] = movie.Mov_Status
                x['Mov_Rating'] = movie.Mov_Rating

                result_list.append(x)

            return jsonify(result_list)
        
        else:
            return jsonify({'message': 'Error', 'details': 'No movies have been created!'})
        
    else:
        return jsonify({'message': 'Error', 'details': 'You are not logged in!'})


@app.route('/admin_shows')
@cross_origin()
@auth_token_required
def admin_shows(current_user):
    result_list = []
    if current_user:
        shows = Shows.query.filter_by(Created_By = current_user.UID).all()
        if len(shows) > 0:
            for show in shows:
                x={}
                x['Show_Id'] = show.Show_Id
                x['Mov_Name'] = show.movie.Mov_Name
                x['Mov_Rating'] = show.movie.Mov_Rating
                x['The_Name'] = show.theatre.The_Name
                x['Location'] = show.theatre.The_Location
                x['Show_Status'] = show.Show_Status
                x['Show_Time'] = show.Show_Time

                result_list.append(x)
            
            return jsonify(result_list)


        else:
            return jsonify({'message': 'Error', 'details': 'No show have been created for this movie!'})

    else:
        return jsonify({'message': 'Error', 'details': 'You are not logged in!'})
    


@app.route('/generate_and_send_csv_')
@cross_origin()
@auth_token_required
def generate_and_send_csv_(current_user):
    id = current_user.UID
    data = download_user_report.delay(id)

    if data:
        return jsonify({'url': f'127.0.0.1:5000/download_report/{id}'})
    else:
        return jsonify({'message': 'Error', 'details': 'Something went wrong. Check celery part of your code'})
    


@app.route('/download_report/<int:id>')
@cross_origin()

def download_report(id):
    csv_content = redis_client.get(f'csv_{id}')

    if csv_content is not None:
        response = Response(csv_content, content_type='text/csv')
        response.headers['Content-Disposition'] = f'attachment; filename=theatre_data_{id}.csv'
        return response
    else:
        return jsonify({'message': 'Error', 'details': "CSV file not found or has expired."})
    

@app.route('/add_theatre', methods=['POST'])
@cross_origin()
@auth_token_required
def add_theatre(current_user):
    if current_user.Role == 'Admin':
        data = request.get_json()
        created_by = current_user.UID
        name = data['The_Name']
        location = data['The_Location']
        data = Theatres.query.filter(Theatres.The_Location.icontains(location) & Theatres.The_Name.icontains(name)).first()
        if data:
            return jsonify({'message': 'Error', 'details': 'You can not have 2 Identical Theatres in the same city'})
        else:
            try:
                theatre = Theatres(Created_By=created_by, The_Name=name, The_Location=location)
                db.session.add(theatre)
                db.session.commit()

                cache.clear()

                return jsonify({'message': 'Success', 'details': 'Theatre Added!'})
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': 'Error', 'details': 'Some Database error occured!'})
    else:
        return jsonify({'message': 'Error', 'details': 'You are not logged in as admin'})
    

@app.route('/add_movie', methods=['POST'])
@cross_origin()
@auth_token_required
def add_movie(current_user):
    if current_user.Role == 'Admin':
        data=request.get_json()
        created_by = current_user.UID
        name = data['Mov_Name']
        rating = data['Mov_Rating']

        movie_check = Movies.query.filter(Movies.Mov_Name.icontains(name) & Movies.Created_By.icontains(created_by)).first()

        if movie_check:
            return jsonify({'message': 'Error', 'details': 'You can not have 2 movies with the same title'})
        
        else:
            movie = Movies(Mov_Name=name, Mov_Rating=rating, Created_By=created_by)
            db.session.add(movie)
            db.session.commit()


            cache.clear()
           
            return jsonify({'message': 'Success', 'details': 'Movie Added!'})
    

    else:
        return jsonify({'message':'Error', 'details': 'You are not logged in as admin'})
    

@app.route('/admin_city_movies', methods=['GET'])
@cross_origin()
@auth_token_required
def admin_theatres(current_user):
    result_list = []
    if current_user.Role == 'Admin':
        cities = Theatres.query.filter_by(Created_By = current_user.UID).all()
        movies = Movies.query.filter_by(Created_By = current_user.UID).all()

        
        if len(cities)> 0:
            a = []
            for city in cities:
                a.append(city.The_Location)

            b = {}
            b['city'] = Unique(a)   
            result_list.append(b)
        else:
           b={}
           b['city'] = []
           result_list.append(b)

        x ={}
        a = []
        for movie in movies:
            if movie.Created_By == current_user.UID:
                y={}
                y['mov_id'] = movie.Mov_Id
                y['mov_name'] = movie.Mov_Name
                a.append(y)

        x['movie'] = a
        
        result_list.append(x)

       
        return jsonify(result_list)

    else:
        return jsonify({'message':'Error', 'details': 'You are not logged in as admin'})
    


@app.route('/admin_city_theatre/<city>')
@cross_origin()
@auth_token_required
def admin_city_theatre(current_user, city):
    result_list = []
    theatres = Theatres.query.filter(Theatres.The_Location.icontains(city) & Theatres.Created_By.icontains(current_user.UID)).all()
  
    if theatres:
        for theatre in theatres:
            x={}
            x['the_id'] = theatre.The_Id
            x['the_name'] = theatre.The_Name

            result_list.append(x)

        return jsonify(result_list)

    else:
        return jsonify({'message': 'Error', 'details': 'No theatre created by this user!'})
    

@app.route('/add_show', methods=['POST'])
@cross_origin()
@auth_token_required
def add_show(current_user):
    if current_user.Role == 'Admin':
        data=request.get_json()
        Created_By = current_user.UID
        The_Id = data['The_Id']
        Mov_Id = data['Mov_Id']
        Total_Seats = data['Total_Seats']
        Show_Time = data['Show_Time']

        show = Shows(Created_By = Created_By, The_Id=The_Id, Mov_Id=Mov_Id, Total_Seats=Total_Seats, Show_Time=Show_Time)
        data_check = Shows.query.filter(Shows.The_Id.icontains(The_Id) & Shows.Mov_Id.icontains(Mov_Id) & Shows.Show_Time.icontains(Show_Time) & Shows.Created_By.icontains(current_user.UID)).first()
        if data_check:
            return jsonify({'message':'Error', 'details': 'You can not create identical shows'})
        else:
            db.session.add(show)
            db.session.commit()

            cache.clear()
            
            return jsonify({'message': 'Success', 'details': 'Show Added!'})

    else:
        return jsonify({'message':'Error', 'details': 'You are not logged in as admin'})
    

@app.route('/admin/enable_show/<int:show_id>')
@cross_origin()
@auth_token_required
def admin_enable_show(current_user, show_id):
    show = Shows.query.filter_by(Show_Id = show_id).first()
    if show.Created_By == current_user.UID:
        show.Show_Status = True
        db.session.commit()
        return jsonify({'message': 'Success', 'details': 'Show Enabled'})

    else:
        return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'})
    

@app.route('/admin/delete_show/<int:show_id>')
@cross_origin()
@auth_token_required
def admin_delete_show(current_user, show_id):
    show = Shows.query.filter_by(Show_Id = show_id).first()
    if show.Created_By == current_user.UID:
        if not show.Show_Status:
            bookings = show.booked_shows
            if len(bookings)>0:
                for booking in bookings:
                    db.session.delete(booking)
                    db.session.commit()

            db.session.delete(show)
            db.session.commit()
            return jsonify({'message': 'Success', 'details': 'Show Deleted'})
        else:
            return jsonify({'message':'Error', 'details': 'Disable a show and then delete it'})

    else:
        return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'})
    

@app.route('/admin/get_bookings/<int:show_id>')
@cross_origin()
@auth_token_required
def admin_get_bookings(current_user, show_id):
    result_list = []
    show = Shows.query.filter_by(Show_Id = show_id).first()
    if show.Created_By == current_user.UID:
        bookings = show.booked_shows
        if len(bookings)> 0:
            for booking in bookings:
                x = {}
                x['Booking_Id'] = booking.Book_Id
                x['Movie_Name'] = show.movie.Mov_Name
                x['Theatre_Name'] = show.theatre.The_Name
                x['Location'] = show.theatre.The_Location
                x['Num_of_seats'] = booking.Num_Of_Seats
                x['Timing'] = show.Show_Time
                x['Cancellation_Reason'] = booking.Reason
                x['Cancellation_Status'] = booking.Cancellation_Status

                result_list.append(x)

            return jsonify(result_list)

        else:
           return jsonify({'message':'Error', 'details': 'No booked show for this Show_Id'}) 

    else:
       return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'}) 
    

@app.route('/admin/disable_show/<int:show_id>')
@cross_origin()
@auth_token_required
def admin_disable_show(current_user, show_id):
    show = Shows.query.filter_by(Show_Id = show_id).first()
    if show.Created_By == current_user.UID:
        bookings = show.booked_shows
        if len(bookings) > 0:
            email_list = []
            for booking in bookings:
                x={}
                x['email'] = booking.users.Email
                x['Tkts'] = booking.Num_Of_Seats
                x['Movie'] = show.movie.Mov_Name
                email_list.append(x)
                booking.Cancellation_Status = True
                booking.Reason = 'Show Cancelled'
                db.session.commit()

            for ema in email_list:
                email = ema['email']
                subject = 'Show Cancellation Email'
                body = f'Your { ema["Tkts"] } tickets for movie {ema["Movie"]} has been cancelled by admin when disabling the show!' 
                send.delay(email = email, subject = subject, body= body)

        show.Show_Status = False
        show.Booked_Seats = 0
        db.session.commit()

        return jsonify({'message':'Success', 'details': 'Show has been disabled'})


    else:
        return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'})
    

@app.route('/admin/cancel_booking/<int:book_id>')
@cross_origin()
@auth_token_required
def admin_cancel_booking(current_user, book_id):
    if current_user.Role == 'Admin':
        bookings = Bookings.query.filter_by(Book_Id = book_id).all()
        if len(bookings)>0:
            email_list = []
            for booking in bookings:
                x = {}

                show = booking.shows
                 
                x['email'] = booking.users.Email
                x['Tkts'] = booking.Num_Of_Seats
                x['Movie'] = show.movie.Mov_Name
                email_list.append(x)

                booking.Cancellation_Status = True
                booking.Reason = 'Admin Cancelled your tkt!'
                if (show.Booked_Seats > 0):
                    show.Booked_Seats = show.Booked_Seats - booking.Num_Of_Seats
                else:
                    show.Booked_Seats = 0
                db.session.commit()

            for ema in email_list:
                email = ema['email']
                subject = 'Admin Ticket Cancellation Email'
                body = f'Your { ema["Tkts"] } tickets for movie {ema["Movie"]} has been cancelled by admin using booking id!' 
                send.delay(email = email, subject = subject, body= body)


            return jsonify({'message': 'Success', 'details': 'Ticket Cancelled!'})

            
        else:
            return jsonify({'message': 'Error', 'details': 'No bookings to cancel'})
    
    else:
       return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'}) 


@app.route('/admin/get_movies/<int:the_id>')
@cross_origin()
@auth_token_required
def admin_get_movies(current_user, the_id):
    result_list = []
    theatre = Theatres.query.filter_by(The_Id = the_id).first()
    if theatre.Created_By == current_user.UID:
        shows = theatre.theatre_shows
        movie_list = []
        if len(shows)>0:
            for show in shows:
                movie = show.Mov_Id
                name = show.movie.Mov_Name
                rating = show.movie.Mov_Rating
                status = show.movie.Mov_Status

                if movie in movie_list:
                    pass
                else:
                    x={}
                    x['Mov_Id'] = movie
                    x['Mov_Name'] = name
                    x['Mov_Rating'] = rating
                    x['Mov_Status'] = status

                    result_list.append(x)

                    movie_list.append(movie)

            if len(result_list)> 0:
                return jsonify(result_list)
            else:
                return jsonify({'message': 'Error', 'details': 'No movies for this Theatre Id by this user'})


        else:
          return jsonify({'message':'Error', 'details': 'No movies for this Theatre Id'})  

    else:
        return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'})
    

@app.route('/admin/enable_theatre/<int:the_id>')
@cross_origin()
@auth_token_required
def admin_enable_theatre(current_user, the_id):
    theatre = Theatres.query.filter(Theatres.The_Id.icontains(the_id) & Theatres.Created_By.icontains(current_user.UID)).first()
    if theatre:
        theatre.The_Status = True
        db.session.commit()

        return jsonify({'message': 'Success', 'details': 'Theatre has been enabled'})

    else:
        return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'})
    

@app.route('/admin/disable_theatre/<int:the_id>')
@cross_origin()
@auth_token_required
def admin_disable_theatre(current_user, the_id):
    theatre = Theatres.query.filter(Theatres.The_Id.icontains(the_id) & Theatres.Created_By.icontains(current_user.UID)).first()
    if theatre:
        shows = theatre.theatre_shows
        email_list = []
        if len(shows)>0:
            for show in shows:
                if show.Show_Status:
                    bookings = show.booked_shows

                    for booking in bookings:
                        x = {}
                        if booking.Cancellation_Status:
                            pass
                        else:
                            x['email'] = booking.users.Email
                            x['Tkts'] = booking.Num_Of_Seats
                            x['Movie'] = show.movie.Mov_Name

                            email_list.append(x)

                        booking.Cancellation_Status = True
                        booking.Reason = 'Admin Disabled The Theatre'
                        db.session.commit()

                    show.Show_Status = False
                    show.Booked_Seats = 0
                    db.session.commit()

            for ema in email_list:
                email = ema['email']
                subject = 'Theatre Cancellation Email'
                body = f'Your { ema["Tkts"] } tickets for movie {ema["Movie"]} has been cancelled by admin using booking id!' 
                send.delay(email = email, subject = subject, body= body)


        theatre.The_Status = False
        db.session.commit()

        return jsonify({'message': 'Success', 'details': 'Theatre Cancelled!'})


    else:
        return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'})
    


@app.route('/admin/get_show/<int:movie_id>')
@cross_origin()
@auth_token_required
def admin_get_shows(current_user, movie_id):
    result_list = []
    if current_user.Role == 'Admin':
        shows = Shows.query.filter_by(Mov_Id = movie_id).all()
        if len(shows)> 0:
            for show in shows:
                
                if show.Created_By == current_user.UID:
                    x={}
                    x['Show_Id'] = show.Show_Id
                    x['Mov_Name'] = show.movie.Mov_Name
                    x['Mov_Rating'] = show.movie.Mov_Rating
                    x['The_Name'] = show.theatre.The_Name
                    x['Location'] = show.theatre.The_Location
                    x['Show_Time'] = show.Show_Time
                    x['Show_Status'] = show.Show_Status

                    result_list.append(x)
            if len(result_list) > 0:
                return jsonify(result_list)
            else:
                return jsonify({'message':'Error', 'details': 'No show by this user for this movie_id'})


        else:
            return jsonify({'message':'Error', 'details': 'No show for this movie_id'})

    else:
       return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'}) 
    

@app.route('/admin/enable_movie/<int:mov_id>')
@cross_origin()
@auth_token_required
def admin_enable_movie(current_user, mov_id):
    movie = Movies.query.filter(Movies.Mov_Id.icontains(mov_id) & Movies.Created_By.icontains(current_user.UID)).first()
    if movie:
        movie.Mov_Status = True
        db.session.commit()

        return jsonify({'message': 'Success', 'details': 'Movie has been enabled'})

    else:
        return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'}) 
    

@app.route('/admin/disable_movie/<int:mov_id>')
@cross_origin()
@auth_token_required
def admin_disable_movie(current_user, mov_id):
    movie = Movies.query.filter(Movies.Mov_Id.icontains(mov_id) & Movies.Created_By.icontains(current_user.UID)).first()
    if movie:
        shows = movie.movie_shows
        email_list = []
        if len(shows)>0:
            for show in shows:
                if show.Show_Status:
                    bookings = show.booked_shows

                    for booking in bookings:
                        x= {}

                        if booking.Cancellation_Status:
                            pass
                        else:
                            x['email'] = booking.users.Email
                            x['Tkts'] = booking.Num_Of_Seats
                            x['Movie'] = show.movie.Mov_Name

                            email_list.append(x)
                        
                        booking.Cancellation_Status = True
                        booking.Reason = 'Admin Disabled The Movie'
                        db.session.commit()

                    show.Show_Status = False
                    show.Booked_Seats = 0
                    db.session.commit()

            for ema in email_list:
                email = ema['email']
                subject = 'Movie Cancellation Email'
                body = f'Your { ema["Tkts"] } tickets for movie {ema["Movie"]} has been cancelled by admin using booking id!' 
                send.delay(email = email, subject = subject, body= body)

        movie.Mov_Status = False
        db.session.commit()

        return jsonify({'message': 'Success', 'details': 'Movie Cancelled!'})

    else:
        return jsonify({'message':'Error', 'details': 'You are not authorised to make this change'})