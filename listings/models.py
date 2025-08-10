from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Listing(models.Model):
    """Model for travel accommodation listings"""
    
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('cabin', 'Cabin'),
        ('condo', 'Condo'),
        ('loft', 'Loft'),
        ('studio', 'Studio'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    max_guests = models.PositiveIntegerField()
    
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    cleaning_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    amenities = models.JSONField(default=list, blank=True)
    house_rules = models.JSONField(default=list, blank=True)
    
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    
    is_active = models.BooleanField(default=True)
    is_instant_bookable = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.city}, {self.country}"
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0
    
    @property
    def total_reviews(self):
        """Get total number of reviews"""
        return self.reviews.count()


class Booking(models.Model):
    """Model for booking reservations"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    
    number_of_guests = models.PositiveIntegerField()
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    special_requests = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking {self.id} - {self.listing.title} ({self.check_in_date} to {self.check_out_date})"
    
    def save(self, *args, **kwargs):
        """Calculate total price before saving"""
        if not self.total_price:
            nights = (self.check_out_date - self.check_in_date).days
            self.total_price = (
                self.listing.price_per_night * nights +
                self.listing.cleaning_fee +
                self.listing.service_fee
            )
        super().save(*args, **kwargs)


class Review(models.Model):
    """Model for guest reviews"""
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    
    cleanliness_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    communication_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    check_in_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    accuracy_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    location_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    value_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['listing', 'guest', 'booking']
    
    def __str__(self):
        return f"Review by {self.guest.username} for {self.listing.title} - {self.rating}/5"
