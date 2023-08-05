from flask import render_template,redirect,request,session
from flask_app import app
from flask_app.model import bands,reg_login

@app.route('/bands/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = reg_login.User.get_by_id({'id': session['user_id']})
    return render_template('dashboard.html',user=user,band=bands.Band.get_all())

@app.route('/bands/new')
def new():
    return render_template('create.html')

@app.route('/bands/create',methods=['post'])
def create():
    if 'user_id' not in session:
        return redirect('/')
    print(request.form)
    if bands.Band.validate_band(request.form):
        bands.Band.save(request.form)
        return redirect('/bands/dashboard')
    return redirect('/bands/new')

@app.route('/bands/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('edit.html',band=bands.Band.get_one({'id': id}))

@app.route('/bands/update/<int:id>',methods=['post'])
def update(id):
    if 'user_id' not in session:
        return redirect('/')
    if not bands.Band.validate_band(request.form):
        return redirect(f'/bands/edit/{id}')
    data = {
        'id': id,
        'band_name': request.form['band_name'],
        'genre': request.form['genre'],
        'city': request.form['city']
    }
    bands.Band.update(data)
    return redirect('/bands/dashboard')

@app.route('/bands/my_bands/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    return render_template('my_bands.html',band=bands.Band.get_user(data))
# URL not found, unable to figure out how to bring over only bands from session user


@app.route('/bands/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':id
    }
    bands.Band.delete(data)
    return redirect('/bands/dashboard')