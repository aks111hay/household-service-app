# Household Service App

## Overview
The Household Service App is a Flask-based platform designed to connect working professionals who provide household services (such as cleaning, plumbing, electrical repairs, etc.) with households seeking these services. This app simplifies the process of finding and hiring trusted professionals for various household tasks, bringing convenience and reliability to both service providers and households.

---

## Features

### For Service Providers:
- **Profile Creation:** Service providers can create profiles, listing their expertise, location, availability, and pricing.
- **Manage Bookings:** View and manage incoming service requests.
- **Ratings and Reviews:** Build credibility through customer feedback.

### For Households:
- **Search Services:** Easily search for professionals based on location, service category, or availability.
- **Request Services:** Book service providers and track request status.
- **Leave Reviews:** Rate and review service providers to help others make informed choices.

### General Features:
- **User Authentication:** Secure login and registration for both service providers and households.
- **Admin Dashboard:** Monitor and manage platform data such as users, bookings, and reviews.
- **Responsive Design:** Fully functional on desktops, tablets, and mobile devices.

---

## Installation

### Prerequisites:
1. Python 3.9 or above.
2. Virtual environment (optional but recommended).
3. Flask and required dependencies (see `requirements.txt`).

### Steps:
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/aks111hay/household-service-app.git
   cd household-service-app
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database:**
   - Initialize the SQLite database:
     ```bash
     flask db init
     flask db migrate -m "Initial migration."
     flask db upgrade
     ```
   - Alternatively, configure another database in the `config.py` file.

5. **Run the Application:**
   ```bash
   flask run
   ```
   The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## File Structure
```
.
├── app/
│   ├── __init__.py
│   ├── models.py        # Database models for the app
│   ├── routes.py        # Application routes and logic
│   ├── templates/       # HTML templates
│   └── static/          # CSS, JS, and image files
├── migrations/          # Database migrations
├── tests/               # Unit tests for the app
├── config.py            # Configuration settings
├── requirements.txt     # Required Python dependencies
├── README.md            # Documentation
└── run.py               # Entry point for the application
```

---

## Key Technologies
- **Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite (default), with support for PostgreSQL/MySQL
- **Authentication:** Flask-Login, Flask-WTF

---

## Usage
### Service Providers:
1. Register as a service provider.
2. Complete your profile with skills, pricing, and availability.
3. Respond to service requests and manage bookings.

### Households:
1. Register as a household user.
2. Search for required services using filters like location and category.
3. Book a service provider and track the booking status.

---

## Future Enhancements
1. **Real-Time Notifications:** Notify users of booking updates.
2. **In-App Payments:** Integrate a secure payment gateway for booking services.
3. **Geo-Location:** Improve service matching based on proximity.
4. **Subscription Plans:** Introduce premium features for professionals.
5. **Chat Functionality:** Enable direct communication between households and service providers.

---

## Contributing
We welcome contributions to enhance the platform. Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## Contact
For inquiries or support, please contact:
- Email: askh123600@gmail.com
- GitHub: [https://github.com/aks111hay/household-service-app](https://github.com/aks111hay/household-service-app)

---

Start connecting professionals and households today with the Household Service App!

