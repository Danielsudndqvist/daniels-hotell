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

   <details>
   <summary>Click to view Room Management images</summary>

   ![Room Management Image 1](https://github.com/user-attachments/assets/83a3824e-7a91-4ecc-b224-008a6edcd56f)
   ![Room Management Image 2](https://github.com/user-attachments/assets/f4b27904-f4c2-4e94-bc1b-1a1e5cf3fa09)
   </details>

3. **Booking System**:
   - Interactive booking process
   - Date-based availability checking
   - Price calculation based on stay duration
   - Booking confirmation with email notifications

   <details>
   <summary>Click to view room selection image</summary>

   ![Room Selection Image](https://github.com/user-attachments/assets/2dd66105-9c4a-4639-8934-d6e0b8b0a266)
   </details>

   <details>
   <summary>Click to view Booking System image</summary>

   ![Booking System Image](https://github.com/user-attachments/assets/2c300330-0fa9-45a5-8664-db96c1a321d0)
   </details>

4. **User Dashboard**:
   - View personal bookings
   - Edit or cancel existing reservations
   - Booking history

   <details>
   <summary>Click to view User Dashboard image</summary>

   ![User Dashboard Image](https://github.com/user-attachments/assets/b3a5c826-18ba-4ba2-af6b-8111befd8e2d)
   </details>

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

   <details>
   <summary>Click to view Cloud Integration image</summary>

   ![Cloud Integration Image](https://github.com/user-attachments/assets/19c10c0e-9a96-4fd8-93ec-f7ce7333bf44)
   </details>
   
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
   ```
   git clone [your-repository-url]
   cd daniels-hotel
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=your_database_url
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Deployment to Heroku
1. Log in (or sign up) to Heroku. (https://www.heroku.com/)
2. From the dashboard, create a "new app" and follow the instructions.
3. When created go to the settings tab and add Config Vars for:
   - DATABASE_URL
   - SECRET_KEY
   - GOOGLE_CREDENTIALS
   - GS_BUCKET_NAME
   - GS_PROJECT_ID
4. Go to the deployment tab.
5. Select GitHub as deployment method.
6. Connect app to the correct repository.
7. Choose to deploy either manually or enable automatic deploys.
