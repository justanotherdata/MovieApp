#Making Necessary Imports
from flask import request, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from main import app, db, bcrypt
from main.forms import Superadmin_signup, LoginForm, Create_admin
from main.models import users, Movies, Theatres, Shows, Bookings
from flask_login import login_user, current_user, logout_user, login_required





#Making the routes
@app.route('/superadmin/register', methods=['GET', 'POST'])
@app.route("/register_superadmin", methods=['GET', 'POST'])
def register_superadmin():
    if current_user.is_authenticated:
        return redirect(url_for('admin_management'))
    form = Superadmin_signup()
    if request.method == 'GET':
        return render_template('superadmin_register.html', title='Register', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
            name = form.Name.data
            email = form.Email.data
            role = 'SuperAdmin' 
            profile = 'New_App\main\static\no-mans-sky-van-gogh-style-glenn-brown-style-highly-detailed-comprehensive-cinematic-digital-p-132810287.png'
            user = users(Email=email, Password=hashed_password, Role=role, Profile_Photo=profile, Name = name)
            try:
                
                db.session.add(user)
                db.session.commit()
                flash(f'Super-Admin {name} created and logged in!', 'success')
                return redirect(url_for('admin_management'))
            except IntegrityError:
                flash(f'Email Id already in use', 'danger')
                return render_template('superadmin_register.html', title="Register", form=form)
        return render_template('superadmin_register.html', title='Register', form=form)
            

@app.route('/superadmin/login', methods=['GET', 'POST'])
@app.route("/login_superadmin", methods = ['GET', 'POST'])
def login_superadmin():
    if current_user.is_authenticated:
        return redirect(url_for('admin_management'))
    form = LoginForm()
    if request.method == 'GET':
        return render_template('admin_login.html', title = 'Login', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = users.query.filter_by(Email = form.Email.data).first()
            if user and bcrypt.check_password_hash(user.Password, form.Password.data):
                #Here we will put an if else condotion to check if the user logging in is a SuperAdmin
                if user.Role == 'SuperAdmin':
                    login_user(user, remember=form.Remember.data)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('admin_management'))
                flash('Please input Valid credentials for a Superadmin login!', 'danger')
                return render_template('admin_login.html', title = 'Login', form = form)
            else:
                flash(f'Invalid Credentials. Please try again!', 'danger')
        return render_template('admin_login.html', title= 'Login', form=form)

  
@app.route('/superadmin/logout')
@app.route("/logout_superadmin")
@login_required 
def logout_superadmin():
    logout_user()
    return redirect(url_for('login_superadmin'))


@app.route('/create_admin', methods=['GET', 'POST'])
@login_required
def create_admin():
    form = Create_admin()
    #Check if the logged in user is superadmin.
    
    if current_user.is_authenticated and current_user.Role == 'SuperAdmin':
        if request.method == 'GET':
            return render_template('superadmin_create_admin.html', title='Create New Admin', form=form)
        elif request.method == 'POST':
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
                name = form.Name.data
                email = form.Email.data
                role = 'Admin' 
                profile = 'New_App\main\static\no-mans-sky-van-gogh-style-glenn-brown-style-highly-detailed-comprehensive-cinematic-digital-p-132810287.png'
                user = users(Email=email, Password=hashed_password, Role=role, Profile_Photo=profile, Name = name)
                try:
                    db.session.add(user)
                    db.session.commit()
                    flash(f'Admin {name}, created!', 'success')
                    flash(f'Username: {email}, Password: {form.Password.data}! Please Save this somewhere safely!', 'info')
                    login_cred = {'Email': email, 'Password': form.Password.data}
                    #return render_template('superadmin_admin_management.html', title='Info')
                    return redirect(url_for('admin_management'))
                except IntegrityError:
                    flash(f'Email Id already in use', 'danger')
                    return render_template('superadmin_create_admin.html', title="Create New Admin", form=form)
    else:
        flash('You are not logged in as a SuperAdmin', 'danger')
        message = 'Login as a Superadmin to create a new Admin'
        return render_template('superadmin_about.html', title='Info', message=message)


@app.route("/superadmin")
@app.route("/home_superadmin")
def home_superadmin():
    return redirect(url_for('login_superadmin'))


@app.route('/admin_management', methods=['GET', 'POST'])
@login_required
def admin_management():
    if current_user.is_authenticated and current_user.Role == 'SuperAdmin':
        admins = users.query.filter_by(Role='Admin').all()
        return render_template('superadmin_admin_management.html', title='Admin Management', admins = admins)
    else:
        message = 'Only Superadmins are authorised to view this page'
        return render_template('superadmin_about.html', title='Info', message=message)





# API Section
@app.route('/delete_admin/<int:admin_id>', methods=['GET','POST'])
@login_required
def delete_admin(admin_id):
    if current_user.is_authenticated and current_user.Role == 'SuperAdmin':
        uid = users.query.filter_by(UID = admin_id).first()
        if uid:
            flash(f'You will delete the admin-id: {uid} and all of their info! Are you sure?', 'danger')
            # We will apply deletion login here. And then flash the success message on the admin-management page.
            #However, we need to delete all the movies, shows, theatres created by that particlar user.
            message = 'Dummy Message for admin deletion'
            return render_template('superadmin_about.html', title='Info', message=message)
        else:
            flash('There is no admin with this Id. Please check and try again', 'info')
            return redirect(url_for('admin_management'))
    else:
        flash('You need to be logged in as a Superadmin to perform this action')
        return render_template('superadmin_about.html', title='info', message='Please logout and signin again as a superadmin to complete that action!')
        

@app.route('/get_admin/<int:admin_id>', methods = ['GET'])
@login_required
def get_admin(admin_id):
    if current_user.is_authenticated and current_user.Role == 'SuperAdmin':
        uid = users.query.filter_by(UID = admin_id).first()
        if uid:
            return render_template('superadmin_admin.html', admin=uid, title=uid.UID)
        else:
            flash('There is no admin with this Id. Please check and try again', 'info')
            return redirect(url_for('admin_management'))
        
    else:
        flash('You need to be logged in as a Superadmin to perform this action')
        return render_template('superadmin_about.html', title='info', message='Please logout and signin again as a superadmin to complete that action!')


@app.route('/edit_admin/<int:admin_id>', methods = ['GET', 'POST'])
@login_required
def edit_admin(admin_id):
    form = Create_admin()
    if current_user.is_authenticated and current_user.Role == 'SuperAdmin':
        uid = users.query.filter_by(UID = admin_id).first()
        form.Email.data = uid.Email
        form.Name.data = uid.Name
        if uid:
            if request.method == 'GET':
                flash(f'Here we will edit the info for admin_id : {admin_id}', 'info')
                return render_template('superadmin_create_admin.html', form=form, title='Edit Admin', user = uid)
            elif request.method == 'POST':
                if form.validate_on_submit():
                    uid.Name = form.Name.data
                    uid.Email = form.Email.data
                    uid.Password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
                    try:
                        db.session.commit()
                        flash(f'Updated login info for admin {uid.Name}', 'success')
                        return redirect(url_for('admin_management'))
                    except IntegrityError:
                        flash('Email Id Already in use', 'danger')
                        return redirect(url_for('admin_management'))    
        else:
            flash('There is no admin with this Id. Please check and try again', 'info')
            return redirect(url_for('admin_management'))
        
    else:
        flash('You need to be logged in as a Superadmin to perform this action')
        return render_template('superadmin_about.html', title='info', message='Please logout and signin again as a superadmin to complete that action!')