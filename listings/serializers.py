from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    
    guest = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'guest', 'rating', 'comment', 'cleanliness_rating',
            'communication_rating', 'check_in_rating', 'accuracy_rating',
            'location_rating', 'value_rating', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'address', 'city', 'state',
            'country', 'postal_code', 'latitude', 'longitude',
            'property_type', 'bedrooms', 'bathrooms', 'max_guests',
            'price_per_night', 'cleaning_fee', 'service_fee',
            'amenities', 'house_rules', 'host', 'is_active',
            'is_instant_bookable', 'created_at', 'updated_at',
            'reviews', 'average_rating', 'total_reviews'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'host']


class ListingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Listing model"""
    
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'address', 'city', 'state',
            'country', 'postal_code', 'latitude', 'longitude',
            'property_type', 'bedrooms', 'bathrooms', 'max_guests',
            'price_per_night', 'cleaning_fee', 'service_fee',
            'amenities', 'house_rules', 'is_instant_bookable'
        ]
    
    def create(self, validated_data):
        """Set the host to the current user"""
        validated_data['host'] = self.context['request'].user
        return super().create(validated_data)


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    
    listing = ListingSerializer(read_only=True)
    guest = UserSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'guest', 'check_in_date', 'check_out_date',
            'number_of_guests', 'total_price', 'status', 'special_requests',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_price', 'created_at', 'updated_at', 'guest']


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Booking model"""
    
    class Meta:
        model = Booking
        fields = [
            'listing', 'check_in_date', 'check_out_date',
            'number_of_guests', 'special_requests'
        ]
    
    def create(self, validated_data):
        """Set the guest to the current user"""
        validated_data['guest'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, data):
        """Validate booking data"""
        listing = data['listing']
        check_in = data['check_in_date']
        check_out = data['check_out_date']
        guests = data['number_of_guests']
        
        # Check if check-out is after check-in
        if check_out <= check_in:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )
        
        # Check if number of guests is within limit
        if guests > listing.max_guests:
            raise serializers.ValidationError(
                f"Number of guests ({guests}) exceeds maximum allowed ({listing.max_guests})."
            )
        
        # Check if listing is active
        if not listing.is_active:
            raise serializers.ValidationError(
                "This listing is not available for booking."
            )
        
        return data 