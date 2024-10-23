from django.db import models
from passenger.models import Passenger
from django.contrib.auth.hashers import make_password


# Create your models here.




class CompletedBookings(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    pass_id = models.IntegerField(null=True, blank=True)
    driver_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    completion_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Completed Booking {self.booking_id} with status {self.status}"


class Driver(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)  # Updated for consistency
    address = models.TextField()
    vehicle = models.CharField(max_length=50)  # Updated for consistency
    licence = models.CharField(max_length=50)  # Updated for consistency
    password = models.CharField(max_length=255)  # Hashed password will be stored
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    auto_img = models.ImageField(upload_to='uploads/temporarydrivers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_live = models.BooleanField(default=False)  # Indicates if the driver is live/active
    current_location = models.CharField(max_length=255, null=True, blank=True)  # Current location of the driver

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Hash password before saving if it hasn't been hashed already
        if not self.password.startswith('pbkdf2_'):  # Check if already hashed
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Bookings(models.Model):
    book_id = models.AutoField(primary_key=True)
    pass_id = models.IntegerField(null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="bookings")
    from_location = models.CharField(max_length=255, null=True, blank=True)
    to_location = models.CharField(max_length=255, null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    OTP = models.IntegerField(null=True, blank=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Booking {self.book_id} from {self.from_location} to {self.to_location}"



class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    pass_id = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True, blank=True)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    review_text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Review {self.review_id} for Driver {self.driver_id}"


class TemporaryDriver(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)  # Updated for consistency
    address = models.TextField()
    vehicle = models.CharField(max_length=50)  # Updated for consistency
    licence = models.CharField(max_length=50)  # Updated for consistency
    password = models.CharField(max_length=255)  # Hashed password will be stored
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    auto_img = models.ImageField(upload_to='uploads/temporarydrivers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Hash password before saving if it hasn't been hashed already
        if not self.password.startswith('pbkdf2_'):  # Check if already hashed
            self.password = make_password(self.password)
        super().save(*args, **kwargs)