from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.model import reg_login,bands
from flask_app import bcrypt

@app.route('/')
def index():
    return redirect('/bands')

@app.route('/bands')
def home():
    return render_template('homepage.html')

@app.route('/bands/register',methods=['post'])
def register():
    if reg_login.User.validate_reg(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        user_id = reg_login.User.save(data)
        session['user_id'] = user_id
        return redirect('/')
    return redirect('/')

@app.route('/bands/login',methods=['post'])
def login():
    this_user = reg_login.User.get_by_email(request.form)
    print(this_user)
    if this_user:
        if bcrypt.check_password_hash(this_user.password,request.form['password']):
            session['user_id'] = this_user.id
            return redirect('/bands/dashboard')
    flash('Invalid email/password.','logError')
    return redirect('/')

@app.route('/bands/logout')
def logout():
    session.clear()
    return redirect('/')