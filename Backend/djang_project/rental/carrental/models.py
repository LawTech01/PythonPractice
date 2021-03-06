import uuid

from django.db import models

# Create your models here.


class Kind(models.Model):
    """ describes a kind, eg, bikes, cars, trucks, buses """
    name = models.CharField(max_length=200, help_text='Please enter the kind of this car')

    """util methods for this table"""
    def __str__(self):
        return self.name


class Vehicle(models.Model):
    """describes a vehicle, eg, toyota camry, mercedes jeep, yatsuchi bike"""
    name = models.CharField(max_length=200)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Please describe the vehicle for the borrower')
    kinds = models.ManyToManyField(Kind, help_text='select a kind for this car')

    """util methods for this table"""
    def __str__(self):
        """ returns a string that is exactly rendered as the display name of instances for that model """
        return self.name


class Manufacturer(models.Model):
    company_name = models.CharField(max_length=200)
    founded = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return f"{self.company_name}-{self.founded}"


class VehicleInstance(models.Model):
    """ represent a specific vehicle that can be rented """
    plate_no = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique ID for this particular vehicle')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.RESTRICT, null=True)
    due_back = models.DateField(null=True, blank=True)
    RENT_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )
    """ We make use of block(capital letter) so it can be accessible under its class alone."""
    """ tuples : used to store multiple items in a single variable"""
    status = models.CharField(max_length=1, choices=RENT_STATUS, blank=True, default='a', help_text='Car availability')

    class Meta:
        """ It defines how its parents class behave """
        ordering= ['due_back', 'vehicle']

    def __str__(self):
        return f"{self.vehicle}-{self.plate_no}"
    """ f strings in python, we use to combine."""
