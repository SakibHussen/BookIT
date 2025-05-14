from flask import Flask,render_template,request,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Event, Booking
from datetime import datetime

app=Flask(__name__, template_folder='templates')

app.config['SECRET_KEY']='Tomkehlier417'
import os
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance/site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            if user.admin:
                return redirect(url_for('admin_home'))
            return redirect(url_for('user_home'))
        flash('Invalid email or password', category='error')
    return render_template('login.html',user= current_user)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', category='error')
            return render_template('register.html')
        name=request.form.get('name')
        password= generate_password_hash(request.form.get('password'))
        street= request.form.get('street')
        city=request.form.get('city')
        state=request.form.get('state')
        zip_code=request.form.get('zip')
        admin=request.form.get('admin','no') == 'yes'
        user = User(email=email, name=name, password=password, street=street,
                    city=city, state=state, zip=zip_code, admin=admin)
        db.session.add(user)
        db.session.commit()
        flash('Account created Sucessfully! Please log in',category='success')
        return redirect(url_for('login'))
    return render_template('register.html')
            
@app.route('/user_home')
@login_required
def user_home():
    if current_user.admin:
        return redirect(url_for('admin_home'))
    events = Event.query.all()
    bookings = current_user.bookings
    return render_template('user_home.html', events=events, bookings=bookings)
        
@app.route('/admin_home')
@login_required
def admin_home():
    if not current_user.admin:
        return redirect(url_for('user_home'))
    events = Event.query.all()
    return render_template('admin_home.html', events=events)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', category='success')
    return redirect(url_for('login'))
# creating event
@app.route('/create_event', methods=['GET','POST'])
@login_required
def create_event():
    if not current_user.admin:
        return redirect(url_for('user_home'))
    if request.method=='POST':
        type=request.form.get('type')
        capacity= int(request.form.get('capacity'))
        cost= float(request.form.get('cost'))
        street= request.form.get('street')
        city=request.form.get('city')
        state=request.form.get('state')
        zip_code=request.form.get('zip')
        start_time=datetime.strptime(request.form.get('start_time'),'%Y-%m-%dT%H:%M')
        end_time=datetime.strptime(request.form.get('end_time'),'%Y-%m-%dT%H:%M')

        if start_time < datetime.now() or end_time <= start_time or capacity <= 0 or cost<0:
            flash('Invalid input',category='danger')
            return render_template('create_event.html')
        # Event is the class od db and after getting all the information, it will create an event
        event=Event(type=type, capacity=capacity, cost=cost, street=street,
            remaining_tickets=capacity,  # Initialize remaining tickets to capacity
                      city=city, state=state, zip=zip_code, start_time=start_time, end_time=end_time)
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully',category='success')
        return redirect(url_for('admin_home'))
    return render_template('create_event.html')

@app.route('/book_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        if quantity <= 0 or quantity > event.remaining_tickets:  # Check against remaining tickets
            flash(f'Cannot book {quantity} tickets. Only {event.remaining_tickets} available.')
            return redirect(url_for('book_event', event_id=event_id))

        payment_info = request.form.get('payment_info') if event.cost > 0 else None
        booking = Booking(payment_info=payment_info, status='confirmed', quantity=quantity,
                          user_id=current_user.id, event_id=event_id)
        db.session.add(booking)
        event.remaining_tickets -= quantity
        db.session.commit()  
        return redirect(url_for('user_home'))
    return render_template('book_event.html', event=event)

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    if not current_user.admin:
        return redirect(url_for('user_home'))
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.type = request.form.get('type')
        event.capacity = int(request.form.get('capacity'))
        event.cost = float(request.form.get('cost'))
        event.street = request.form.get('street')
        event.city = request.form.get('city')
        event.state = request.form.get('state')
        event.zip = request.form.get('zip')
        event.start_time = datetime.strptime(request.form.get('start_time'), '%Y-%m-%dT%H:%M')
        event.end_time = datetime.strptime(request.form.get('end_time'), '%Y-%m-%dT%H:%M')
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('admin_home'))
    return render_template('edit_event.html', event=event)

@app.route('/delete_event/<int:event_id>')
@login_required
def delete_event(event_id):
    if not current_user.admin:
        return redirect(url_for('user_home'))
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('admin_home'))

if __name__ == '__main__':
        app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_debugger=True,
        use_reloader=True,
        passthrough_errors=True
    
)