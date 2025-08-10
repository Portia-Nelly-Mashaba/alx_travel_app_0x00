from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
import random
from decimal import Decimal
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seed the database with sample data for listings, bookings, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=30,
            help='Number of bookings to create (default: 30)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=50,
            help='Number of reviews to create (default: 50)'
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')
        
        # Create users
        users = self.create_users(options['users'])
        
        # Create listings
        listings = self.create_listings(options['listings'], users)
        
        # Create bookings
        bookings = self.create_bookings(options['bookings'], listings, users)
        
        # Create reviews
        self.create_reviews(options['reviews'], bookings, users)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database with:\n'
                f'- {len(users)} users\n'
                f'- {len(listings)} listings\n'
                f'- {len(bookings)} bookings\n'
                f'- {options["reviews"]} reviews'
            )
        )

    def create_users(self, count):
        """Create sample users"""
        users = []
        for i in range(count):
            username = f'user{i+1}'
            email = f'user{i+1}@example.com'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'First{i+1}',
                    'last_name': f'Last{i+1}',
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            
            users.append(user)
        
        return users

    def create_listings(self, count, users):
        """Create sample listings"""
        cities = [
            ('New York', 'NY', 'USA'),
            ('Los Angeles', 'CA', 'USA'),
            ('Chicago', 'IL', 'USA'),
            ('Miami', 'FL', 'USA'),
            ('San Francisco', 'CA', 'USA'),
            ('Paris', 'Île-de-France', 'France'),
            ('London', 'England', 'UK'),
            ('Tokyo', 'Tokyo', 'Japan'),
            ('Sydney', 'NSW', 'Australia'),
            ('Toronto', 'ON', 'Canada'),
        ]
        
        property_types = ['apartment', 'house', 'villa', 'cabin', 'condo', 'loft', 'studio']
        
        amenities_options = [
            ['WiFi', 'Kitchen', 'Free parking'],
            ['WiFi', 'Kitchen', 'Pool', 'Gym'],
            ['WiFi', 'Kitchen', 'Air conditioning', 'Heating'],
            ['WiFi', 'Kitchen', 'Washer', 'Dryer'],
            ['WiFi', 'Kitchen', 'Balcony', 'Garden'],
            ['WiFi', 'Kitchen', 'Hot tub', 'Fireplace'],
        ]
        
        house_rules_options = [
            ['No smoking', 'No pets'],
            ['No smoking', 'No parties'],
            ['No smoking', 'Quiet hours after 10 PM'],
            ['No smoking', 'No shoes inside'],
            ['No smoking', 'No loud music'],
        ]
        
        listings = []
        for i in range(count):
            city, state, country = random.choice(cities)
            property_type = random.choice(property_types)
            host = random.choice(users)
            
            # Generate realistic pricing based on property type and location
            base_price = random.randint(50, 300)
            if property_type in ['villa', 'house']:
                base_price *= 1.5
            if city in ['New York', 'San Francisco', 'Paris', 'London']:
                base_price *= 1.8
            
            listing = Listing.objects.create(
                title=f'Beautiful {property_type.title()} in {city}',
                description=f'Stunning {property_type} located in the heart of {city}. '
                           f'Perfect for your next vacation with all the amenities you need.',
                address=f'{random.randint(100, 9999)} {random.choice(["Main St", "Oak Ave", "Pine Rd", "Elm St"])}',
                city=city,
                state=state,
                country=country,
                postal_code=f'{random.randint(10000, 99999)}',
                latitude=Decimal(f'{random.uniform(20, 60):.6f}'),
                longitude=Decimal(f'{random.uniform(-180, 180):.6f}'),
                property_type=property_type,
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 3),
                max_guests=random.randint(2, 8),
                price_per_night=Decimal(str(base_price)),
                cleaning_fee=Decimal(str(random.randint(20, 100))),
                service_fee=Decimal(str(random.randint(10, 50))),
                amenities=random.choice(amenities_options),
                house_rules=random.choice(house_rules_options),
                host=host,
                is_active=random.choice([True, True, True, False]),  # 75% active
                is_instant_bookable=random.choice([True, False]),
            )
            
            listings.append(listing)
            self.stdout.write(f'Created listing: {listing.title}')
        
        return listings

    def create_bookings(self, count, listings, users):
        """Create sample bookings"""
        statuses = ['confirmed', 'completed', 'pending', 'cancelled']
        bookings = []
        
        for i in range(count):
            listing = random.choice(listings)
            guest = random.choice([u for u in users if u != listing.host])
            
            # Generate random dates
            start_date = date.today() + timedelta(days=random.randint(-30, 60))
            end_date = start_date + timedelta(days=random.randint(1, 14))
            
            booking = Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in_date=start_date,
                check_out_date=end_date,
                number_of_guests=random.randint(1, listing.max_guests),
                status=random.choice(statuses),
                special_requests=random.choice([
                    '', 'Early check-in if possible', 'Late check-out requested',
                    'Extra towels needed', 'Quiet room preferred'
                ])
            )
            
            bookings.append(booking)
            self.stdout.write(f'Created booking: {booking}')
        
        return bookings

    def create_reviews(self, count, bookings, users):
        """Create sample reviews"""
        comments = [
            'Great place to stay! Very clean and comfortable.',
            'Perfect location, easy access to everything.',
            'The host was very responsive and helpful.',
            'Beautiful property, exactly as described.',
            'Highly recommend this place for your stay.',
            'Excellent value for money.',
            'The amenities were top-notch.',
            'Very peaceful and quiet neighborhood.',
            'The check-in process was smooth.',
            'Would definitely stay here again!',
            'The place was spotless and well-maintained.',
            'Great communication with the host.',
            'Perfect for our family vacation.',
            'The location was ideal for exploring the city.',
            'Very comfortable beds and good amenities.',
        ]
        
        for i in range(count):
            if not bookings:
                break
                
            booking = random.choice(bookings)
            
            # Only create review if booking is completed
            if booking.status == 'completed':
                rating = random.randint(3, 5)  # Mostly positive reviews
                
                review = Review.objects.create(
                    listing=booking.listing,
                    guest=booking.guest,
                    booking=booking,
                    rating=rating,
                    comment=random.choice(comments),
                    cleanliness_rating=random.randint(3, 5),
                    communication_rating=random.randint(3, 5),
                    check_in_rating=random.randint(3, 5),
                    accuracy_rating=random.randint(3, 5),
                    location_rating=random.randint(3, 5),
                    value_rating=random.randint(3, 5),
                )
                
                self.stdout.write(f'Created review: {review}')
            
            # Remove this booking to avoid duplicates
            bookings.remove(booking) 