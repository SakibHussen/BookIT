from app import app, db, Event, Booking, User

with app.app_context():
    
     
    user=User.query.all()
    print(f'Total Users: {len(user)}\n')
    for user in user:
        print(f'User ID: {user.id}\n')
        print(f'User Name: {user.name}\n')
        print(f'User Email: {user.email}\n')
        


