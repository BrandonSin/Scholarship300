from django.db import models

# MODELS USED IN DATABASE TODO create better models and foreing keys

from django.urls import reverse  # To generate URLS by reversing URL patterns


class Type(models.Model):
    """Model representing a scholarship type (e.g. Athletic, Merit)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a scholarship type (e.g. Athletic, Merit.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class GPA(models.Model):
    """Model representing a GPA TODO limit to positive integer"""
    grade = models.CharField(max_length=200,
                            help_text="Enter the min gpa required to apply ")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.grade


class Scholarship(models.Model):
    """Model representing a scholarship (but not a specific copy of a scholarship)."""
    name = models.CharField(max_length=200)
    donor = models.ForeignKey('Donor', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the scholarship")
    value = models.CharField('Value', max_length=13,
                            help_text='Ammount distributed')
    type = models.ManyToManyField(Type, help_text="Select a type for this scholarship")
    # ManyToManyField used because a type can contain many scholarships and a Scholarship can cover many types.
    # Type class has already been defined so we can specify the object above.
    gpa = models.ForeignKey('GPA', on_delete=models.SET_NULL, null=True)

    def display_type(self):
        """Creates a string for the Type. This is required to display type in Admin."""
        return ', '.join([type.name for type in self.type.all()[:3]])

    display_type.short_description = 'Type'

    def get_absolute_url(self):
        """Returns the url to access a particular scholarship instance."""
        return reverse('scholarship-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name


import uuid  # Required for unique scholarship instances
from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a applicant


class ScholarshipInstance(models.Model):
    """Model representing a specific copy of a scholarship (i.e. that can be applied from the Archive)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular scholarship across whole Archive")
    scholarship = models.ForeignKey('Scholarship', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    deadline = models.DateField(null=True, blank=True)
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    applicants = models.ManyToManyField('Student')

    @property
    def is_pastdeadline(self):
        if self.deadline and date.today() > self.deadline:
            return True
        return False

    APPLICANT_STATUS = (
        ('d', 'Applied'),
        ('o', 'Waitlist'),
        ('a', 'Available'),
        ('r', 'Rewarded'),
    )

    status = models.CharField(
        max_length=1,
        choices=APPLICANT_STATUS,
        blank=True,
        default='d',
        help_text='Scholarship availability')

    class Meta:
        ordering = ['deadline']
        permissions = (("can_mark_awarded", "Set scholarship as applied"),)

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.scholarship.name)


class Donor(models.Model):
    """Model representing an donor."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular donor instance."""
        return reverse('donor-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)

class Student(models.Model):
    """Model representing an student."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular student")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gpa = models.DecimalField(max_digits = 3, decimal_places = 2)
    applied_scholarships = models.ManyToManyField(ScholarshipInstance)
#    rewarded_scholarships = models.ForeignKey(ScholarshipInstance)
    class Meta:
        ordering = ['last_name', 'first_name']

#    def get_absolute_url(self):
#        """Returns the url to access a particular donor instance."""
#        return reverse('donor-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)
