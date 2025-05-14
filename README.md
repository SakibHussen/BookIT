# BookIT

## Overview
The BookIT project is a Flask-based web application designed for event booking and management. It provides user registration and login functionality with role-based access control, distinguishing between regular users and administrators. Administrators can create, edit, and delete events, specifying details such as event type, capacity, cost, location, and timing. Regular users can browse available events, book tickets with quantity and payment information, and view their bookings. The application uses a SQLite database to store user, event, and booking data, and employs secure password hashing and session management. The user interface is rendered through HTML templates tailored for different user roles and actions, ensuring a user-friendly experience for managing and participating in events.

## Features
- User authentication and role management (login, register, logout, admin vs user)
- Event management (create, edit, delete events by admin)
- Event booking by users
- Rendering various web pages (login, register, user home, admin home, event booking, event creation/editing)


## Tech Stack
This project is built using:
- **HTML** (65.5%): For designing and structuring the user interface.
- **Python** (34.5%): For backend logic and server-side functionalities.

## Installation
To run this project locally, follow these steps:
1. Clone this repository:
   ```bash
   git clone https://github.com/SakibHussen/BookIT.git