# Daniel's Hotel

Daniel's Hotel is a Django-based web application for managing hotel room bookings and displaying hotel information.

## Features

- Home page with hotel information and image carousel
- Room listing page
- Individual room booking page
- User authentication system
- Admin interface for managing rooms, bookings, and amenities

## Tech Stack

- Django
- Python
- HTML/CSS
- JavaScript
- Bootstrap 5
- Font Awesome

## Project Structure

The project includes the following main components:

- `CustomUser` model for user management
- `Profile` model for additional user information
- `Room` model for managing hotel rooms
- `Booking` model for handling reservations
- `Amenity` model for room amenities
- `RoomImage` model for room photos

## Setup and Installation

1. Clone the repository
2. Create a virtual environment and activate it
3. Install the required packages: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Run the development server: `python manage.py runserver`

## Usage

- Access the admin interface at `/admin/` to manage rooms, bookings, and other data
- Visit the home page to see general hotel information
- Browse available rooms and make bookings

## Contributing

[Include information about how others can contribute to the project]

## License

[Specify the license under which your project is released]
