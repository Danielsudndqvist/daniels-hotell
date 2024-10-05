# Daniel's Hotel - Django Web Application

# Daniel's Hotel - Django Web Application

## Project Description

Daniel's Hotel is a comprehensive web application built with Django, designed to streamline the hotel room booking process. This system offers a user-friendly interface for both guests and hotel management, providing a seamless experience from room browsing to booking confirmation.

Key aspects of the project include:

1. **User Management**: 
   - Custom user model extending Django's AbstractUser
   - User registration with email as the primary identifier
   - Secure authentication system
   - User profiles with additional information (phone, address, date of birth)

2. **Room Management**:
   - Detailed room listings with descriptions, types, and pricing
   - Room categorization (Standard, Deluxe, Suite)
   - Support for room amenities and occupancy limits
   - Image gallery for each room

3. **Booking System**:
   - Interactive booking process
   - Date-based availability checking
   - Price calculation based on stay duration
   - Booking confirmation with email notifications

4. **User Dashboard**:
   - View personal bookings
   - Edit or cancel existing reservations
   - Booking history

5. **Admin Interface**:
   - Comprehensive management of rooms, bookings, and user accounts
   - Room availability updates
   - Booking status management

6. **Search and Filter**:
   - Advanced room search based on dates, room type, and price range
   - Real-time availability updates

7. **Responsive Design**:
   - Mobile-friendly interface using Bootstrap
   - Consistent styling across devices

8. **Security Features**:
   - CSRF protection
   - Secure handling of user data and payments

9. **Cloud Integration**:
   - Google Cloud Storage for managing media files in production

10. **Scalability**:
    - Designed to handle multiple rooms and concurrent bookings
    - Easily extendable for additional features

This application aims to provide a robust solution for small to medium-sized hotels, offering an efficient way to manage bookings, improve customer experience, and streamline hotel operations. Whether you're a guest looking for the perfect room or a hotel manager keeping track of reservations, Daniel's Hotel provides the tools you need in an intuitive, web-based platform.

## Features
- User registration and authentication
- Room listing and detailed view
- Room booking system
- Booking management (view, edit, cancel bookings)
- Admin interface for hotel management

## User Stories for Daniel's Hotel
https://github.com/users/Danielsudndqvist/projects/3/views/1

## Technology Stack
- Python 3.x
- Django 4.2.15
- PostgreSQL (Production) / SQLite (Development)
- HTML, CSS, JavaScript
- Bootstrap 5.3.2
- Font Awesome 6.5.1
- Google Cloud Storage (for media files in production)

## Installation

1. Clone the repository:
git clone [your-repository-url]
cd daniels-hotel

3. Install the required packages:
pip install -r requirements.txt

4. Set up your environment variables in a `.env` file:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json

5. Run migrations:
python manage.py migrate


6. Create a superuser:
python manage.py createsuperuser

7. Run the development server:
python manage.py runserver

## Deployment to Heroku
Log in (or sign up) to Heroku. ( https://www.heroku.com/ )
From the dashboard, create a "new app" and follow the instructions.
When created go to the settings tab and add a Config Var for:
DATABASE_URL
SECRET_KEY
GOOGLE_CREDENTIALS
GS_BUCKET_NAME
GS_PROJECT_ID
Go to the deployment tab.
Select GitHub as deployment method.
Connect app to the correct repository.
Choose to deploy either manully or enable automatic deploys.

