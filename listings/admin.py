from django.contrib import admin
from .models import Listing, Booking, Review


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'country', 'property_type', 'price_per_night', 'host', 'is_active', 'is_instant_bookable']
    list_filter = ['property_type', 'is_active', 'is_instant_bookable', 'country', 'city']
    search_fields = ['title', 'description', 'address', 'city', 'country']
    list_editable = ['is_active', 'is_instant_bookable']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'host')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code', 'latitude', 'longitude')
        }),
        ('Property Details', {
            'fields': ('property_type', 'bedrooms', 'bathrooms', 'max_guests')
        }),
        ('Pricing', {
            'fields': ('price_per_night', 'cleaning_fee', 'service_fee')
        }),
        ('Settings', {
            'fields': ('amenities', 'house_rules', 'is_active', 'is_instant_bookable')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing', 'guest', 'check_in_date', 'check_out_date', 'number_of_guests', 'total_price', 'status']
    list_filter = ['status', 'check_in_date', 'check_out_date']
    search_fields = ['listing__title', 'guest__username', 'guest__email']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('listing', 'guest', 'check_in_date', 'check_out_date', 'number_of_guests')
        }),
        ('Status & Pricing', {
            'fields': ('status', 'total_price', 'special_requests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing', 'guest', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['listing__title', 'guest__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('listing', 'guest', 'booking', 'rating', 'comment')
        }),
        ('Detailed Ratings', {
            'fields': ('cleanliness_rating', 'communication_rating', 'check_in_rating', 
                      'accuracy_rating', 'location_rating', 'value_rating'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
