# ALX Travel App - Database Modeling and Data Seeding

A Django-based travel accommodation application with comprehensive database models, API serializers, and data seeding capabilities.

## Project Structure

```
alx_travel_app_0x00/
├── alx_travel_app/          # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── listings/                # Main app for listings and bookings
│   ├── __init__.py
│   ├── models.py            # Database models (Listing, Booking, Review)
│   ├── serializers.py       # DRF serializers for API
│   ├── views.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   └── management/
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── seed.py      # Database seeding command
├── manage.py
├── requirements.txt         # Python dependencies
└── README.md
```

## Features

### Database Models

1. **Listing Model**
   - Property details (title, description, address, location)
   - Property specifications (type, bedrooms, bathrooms, max guests)
   - Pricing (per night, cleaning fee, service fee)
   - Amenities and house rules (JSON fields)
   - Host relationship and availability status

2. **Booking Model**
   - Reservation details (check-in/out dates, guests)
   - Pricing calculation (automatic total price calculation)
   - Status tracking (pending, confirmed, cancelled, completed)
   - Guest and listing relationships

3. **Review Model**
   - Overall rating and detailed category ratings
   - Guest feedback and comments
   - One-to-one relationship with bookings
   - Validation for rating ranges

### API Serializers

- **UserSerializer**: User profile data
- **ListingSerializer**: Complete listing information with reviews
- **ListingCreateSerializer**: For creating new listings
- **BookingSerializer**: Booking details with listing information
- **BookingCreateSerializer**: For creating new bookings with validation
- **ReviewSerializer**: Review data with guest information

### Data Seeding

Comprehensive seeding command that creates:
- Sample users with realistic profiles
- Diverse listings across multiple cities
- Realistic pricing based on location and property type
- Bookings with various statuses
- Reviews for completed bookings

## Setup Instructions

### Prerequisites

- Python 3.8+
- Django 5.2+
- Django REST Framework

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx_travel_app_0x00
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Seed the database**
   ```bash
   python manage.py seed
   ```

### Seeding Options

The seed command supports various options to customize the amount of data:

```bash
# Default seeding (10 users, 20 listings, 30 bookings, 50 reviews)
python manage.py seed

# Custom amounts
python manage.py seed --users 5 --listings 10 --bookings 15 --reviews 25

# Minimal data for testing
python manage.py seed --users 3 --listings 5 --bookings 8 --reviews 10
```

## Database Schema

### Listing Model Fields
- `title`: Property title (CharField, max 200 chars)
- `description`: Detailed description (TextField)
- `address`, `city`, `state`, `country`, `postal_code`: Location details
- `latitude`, `longitude`: GPS coordinates (DecimalField)
- `property_type`: Type of accommodation (choices: apartment, house, villa, etc.)
- `bedrooms`, `bathrooms`, `max_guests`: Property specifications
- `price_per_night`, `cleaning_fee`, `service_fee`: Pricing information
- `amenities`, `house_rules`: JSON fields for flexible data
- `host`: ForeignKey to User model
- `is_active`, `is_instant_bookable`: Status flags
- `created_at`, `updated_at`: Timestamps

### Booking Model Fields
- `listing`: ForeignKey to Listing
- `guest`: ForeignKey to User
- `check_in_date`, `check_out_date`: Reservation dates
- `number_of_guests`: Number of guests
- `total_price`: Calculated total (auto-calculated)
- `status`: Booking status (choices: pending, confirmed, cancelled, completed)
- `special_requests`: Additional requests (TextField)
- `created_at`, `updated_at`: Timestamps

### Review Model Fields
- `listing`: ForeignKey to Listing
- `guest`: ForeignKey to User
- `booking`: OneToOneField to Booking
- `rating`: Overall rating (1-5)
- `comment`: Review text
- `cleanliness_rating`, `communication_rating`, etc.: Detailed ratings
- `created_at`, `updated_at`: Timestamps

## API Usage

The application provides RESTful API endpoints for:

- **Listings**: CRUD operations for property listings
- **Bookings**: Create and manage reservations
- **Reviews**: Submit and retrieve guest reviews
- **Users**: User profile management

### Example API Calls

```bash
# Get all listings
GET /api/listings/

# Create a new listing
POST /api/listings/
{
    "title": "Beautiful Apartment in Downtown",
    "description": "Modern apartment with city views",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "property_type": "apartment",
    "bedrooms": 2,
    "bathrooms": 1,
    "max_guests": 4,
    "price_per_night": "150.00"
}

# Create a booking
POST /api/bookings/
{
    "listing": 1,
    "check_in_date": "2024-01-15",
    "check_out_date": "2024-01-20",
    "number_of_guests": 2
}
```

## Validation Features

- **Booking Validation**: Ensures check-out date is after check-in date
- **Guest Limits**: Validates number of guests against listing capacity
- **Rating Validation**: Ensures ratings are within 1-5 range
- **Active Listings**: Only allows bookings for active listings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the ALX Software Engineering program.

## Author

ALX Student - Database Modeling and API Development Project 