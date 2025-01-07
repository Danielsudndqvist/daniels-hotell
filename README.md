# 🏨 Daniel's Hotel - Django Web Application

[![Heroku Deployment](https://heroku-badge.herokuapp.com/?app=pp4-daniels-hotel-d50d43bb18a9)](https://pp4-daniels-hotel-d50d43bb18a9.herokuapp.com/)
![Python Version](https://img.shields.io/badge/python-3.x-blue)
![Django Version](https://img.shields.io/badge/django-4.2.15-green)

**Live Demo**: [Daniel's Hotel Website](https://pp4-daniels-hotel-d50d43bb18a9.herokuapp.com/)

## 🌟 Project Overview

Daniel's Hotel is a comprehensive Django web application designed to streamline the hotel room booking process. It provides an intuitive, user-friendly interface for both guests and hotel management, ensuring a seamless experience from room browsing to booking confirmation.

## ✨ Key Features

### 1. 👤 User Management
- Custom user model extending Django's AbstractUser
- Email-based registration
- Secure authentication system
- Detailed user profiles

### 2. 🛏️ Room Management
- Detailed room listings with descriptions and pricing
- Room categorization (Standard, Deluxe, Suite)
- Support for room amenities and occupancy limits
- Image gallery for each room

### 3. 📅 Booking System
- Interactive and intuitive booking process
- Real-time availability checking
- Dynamic price calculation
- Email notification confirmations

### 4. 📊 User Dashboard
- Personal booking management
- Reservation editing and cancellation
- Comprehensive booking history

### 5. 🔐 Additional Features
- Responsive Bootstrap design
- Advanced search and filter functionality
- Admin interface for comprehensive management
- Google Cloud Storage integration
- Robust security features

## 🚀 Technology Stack

- **Backend**: Python 3.x, Django 4.2.15
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Frontend**: HTML, CSS, JavaScript
- **Frameworks**: Bootstrap 5.3.2
- **Additional Tools**: 
  - Font Awesome 6.5.1
  - Google Cloud Storage

## 🔧 Installation Guide

### Prerequisites
- Python 3.x
- pip
- Virtual environment (recommended)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone [your-repository-url]
   cd daniels-hotel
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (`.env` file):
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=your_database_url
   GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
   ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## 📋 User Guide

### Guest User Workflow
1. **Browse Rooms**: Explore available rooms with filters
2. **Select Room**: View detailed room information
3. **Book Room**: Choose dates and complete booking
4. **Manage Bookings**: View and modify reservations

### Admin User Workflow
1. **Login**: Access admin dashboard
2. **Manage Rooms**: Add, edit, delete rooms
3. **Manage Bookings**: Track and update reservations
4. **User Management**: Handle user accounts
5. **Generate Reports**: Analyze bookings and revenue

## 🐞 Troubleshooting

- **Login Issues**: Use "Forgot Password" feature
- **Booking Problems**: Check room availability
- **Image Loading**: Clear browser cache

## 📬 Feedback
We welcome your suggestions! Contact us through the website's "Contact Us" form.

## 🔗 User Stories
[View Project User Stories](https://github.com/users/Danielsudndqvist/projects/3/views/1)

## 🚀 Deployment to Heroku

1. Log in to Heroku
2. Create a new app
3. Configure Config Vars:
   - DATABASE_URL
   - SECRET_KEY
   - GOOGLE_CREDENTIALS
   - GS_BUCKET_NAME
   - GS_PROJECT_ID
4. Connect to GitHub repository
5. Deploy (manual or automatic)

## 📊 Project Statistics

[![Testing Coverage](https://img.shields.io/badge/test%20coverage-100%25-brightgreen)]()
[![Bugs](https://img.shields.io/badge/open%20bugs-1-yellow)]()
[![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)]()

## 📄 License

*Add your license information here*

---

**Made with ❤️ by Daniel's Hotel Development Team**
