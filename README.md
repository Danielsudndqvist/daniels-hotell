# 🏨 Daniel's Hotel Booking System

## 🌟 Project Overview

Daniel's Hotel is a comprehensive Django web application designed to streamline the hotel room booking process. It provides an intuitive, user-friendly interface for both guests and hotel management, ensuring a seamless experience from room browsing to booking confirmation.

## 🛠️ Tech Stack & Badges

![Python Version](https://img.shields.io/badge/python-3.x-blue)
![Django Version](https://img.shields.io/badge/django-4.2.15-green)
![Bootstrap Version](https://img.shields.io/badge/bootstrap-5.3.2-purple)
[![Heroku Deployment](https://heroku-badge.herokuapp.com/?app=pp4-daniels-hotel-d50d43bb18a9)](https://pp4-daniels-hotel-d50d43bb18a9.herokuapp.com/)

## ✨ Key Features

### 👤 User Management
- 🔐 Custom user model extending Django's AbstractUser
- 📧 Email-based registration
- 🛡️ Secure authentication system
- 📋 Detailed user profiles

### 🛏️ Room Management
- 📝 Detailed room listings with descriptions and pricing
- 🏷️ Room categorization (Standard, Deluxe, Suite)
- 🖼️ Image gallery for each room
- 🧩 Support for room amenities and occupancy limits

### 📅 Booking System
- 🎯 Interactive and intuitive booking process
- ⏰ Real-time availability checking
- 💰 Dynamic price calculation
- 📬 Email notification confirmations

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- pip
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone [your-repository-url]
cd daniels-hotel

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create a .env file with:
# SECRET_KEY=your_secret_key
# DEBUG=True
# DATABASE_URL=your_database_url

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```


## 🧪 Testing Coverage

![Test Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)

- **Unit Tests**: 150+ test cases
- **Integration Tests**: Comprehensive system-wide testing
- **Manual Testing**: Extensive device and browser compatibility checks

## 🌐 Deployment

### Heroku Deployment
1. Create Heroku account
2. Install Heroku CLI
3. Configure environment variables
4. Push to Heroku main branch

### Continuous Integration
- Automated testing on every pull request
- Deployment triggered on successful main branch merge

## 🔮 Future Roadmap

- [ ] Payment gateway integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile app development
- [ ] AI-powered room recommendations

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

- **Project Lead**: Daniel Sudndqvist
- **Email**: [your-email@example.com](mailto:your-email@example.com)
- **Project Link**: [GitHub Repository](https://github.com/your-username/daniels-hotel)

---

**Made with ❤️ by Daniel's Hotel Development Team**

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
