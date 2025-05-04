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
```bash
git clone [your-repository-url]
cd daniels-hotel
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
Environment Variables (.env)
ini
Kopiera
Redigera
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
Migrations and Admin
bash
Kopiera
Redigera
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
📸 Screenshots
<details> <summary>Home View - Fullscreen</summary> <img src="https://github.com/user-attachments/assets/8446b1a3-a277-4f13-a671-5c9aea45d699" alt="Home View Fullscreen"> </details> <details> <summary>Home View - Mobile</summary> <img src="https://github.com/user-attachments/assets/e466e7f3-13e1-4ebc-93f6-4e4d0419d2fa" alt="Home View Mobile"> </details> <details> <summary>Room Selection - Fullscreen</summary> <img src="https://github.com/user-attachments/assets/f0c0e4de-8772-4fac-a8da-fab78e5e5fb1" alt="Room Selection Fullscreen"> </details> <details> <summary>Room Selection - Mobile</summary> <img src="https://github.com/user-attachments/assets/70d222d0-9b6e-4a5a-9a57-7c0cead23b92" alt="Room Selection Mobile"> </details> <details> <summary>Booking Form - Fullscreen</summary> <img src="https://github.com/user-attachments/assets/7ba3017f-ff2b-45d1-a646-67b8965d92b0" alt="Booking Form Fullscreen"> </details> <details> <summary>Booking Form - Mobile</summary> <img src="https://github.com/user-attachments/assets/e7940d0d-68a1-435b-8563-e73e87dd9f51" alt="Booking Form Mobile"> </details>
🖼️ Wireframes
<details> <summary>Home Page</summary> <img src="https://github.com/user-attachments/assets/f3d5e3fb-f0ad-43ee-85d8-16582254c363" alt="Home Page Wireframe"> </details> <details> <summary>Room Selection</summary> <img src="https://github.com/user-attachments/assets/5da9c3cb-3bd4-487d-98ab-757626a23ab9" alt="Room Selection Wireframe"> </details> <details> <summary>Room Information</summary> <img src="https://github.com/user-attachments/assets/3217cc9a-e811-451b-8d19-37402f8b2e9a" alt="Room Information Wireframe"> </details>
📋 User Guide
Guest User Workflow
Browse Rooms: Explore available rooms with filters

Select Room: View detailed room information

Book Room: Choose dates and complete booking

Manage Bookings: View and modify reservations

Admin User Workflow
Login: Access admin dashboard

Manage Rooms: Add, edit, delete rooms

Manage Bookings: Track and update reservations

User Management: Handle user accounts

Generate Reports: Analyze bookings and revenue

✅ Django Tests
<details> <summary>Test Results</summary> <img src="https://github.com/user-attachments/assets/f331fbae-6e53-4518-967e-8edc86d74bbd" alt="Test Results"> </details> ```
