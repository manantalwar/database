from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class Course(models.Model):
    department = models.CharField(max_length=16, help_text='Department string, like COMPSCI or MATH.')
    number = models.IntegerField(validators=[validators.MinValueValidator(100), validators.MaxValueValidator(999)], help_text='Course number, like the 187 in COMPSCI 187.')
    name = models.CharField(max_length=64, help_text='The human-legible name of the course, like "Programming with Data Structures."')

    def __str__(self):
        return f'{self.department} {self.number}: {self.name}'


class LRCDatabaseUser(AbstractUser):
    courses_tutored = models.ManyToManyField(Course)


class TutoringShift(models.Model):
    tutor = models.ForeignKey(to=LRCDatabaseUser, on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.tutor} in {self.location} at {self.start}'


class TutoringShiftChangeRequest(TutoringShift):
    target = models.ForeignKey(to=TutoringShift, related_name='tutoring_shift_change_request_target', on_delete=models.CASCADE, help_text='Tutoring shift to edit.')
    reason = models.CharField(max_length=512, help_text='Explanation for why this change is being requested.')
    approved = models.BooleanField(default=False, help_text='Whether the request is approved or not.')
    approved_by = models.ForeignKey(to=LRCDatabaseUser, null=True, default=None, on_delete=models.CASCADE, help_text='The user (if any) who approved the change request.')
    approved_on = models.DateTimeField(help_text='When the request was approved.')


class Hardware(models.Model):

    name = models.CharField(max_length=200)
    isAvailable = models.BooleanField(True)

    #inventory = models.ForeignKey('Inventory', on_delete=CASCADE)

    def __str__(self):
        return self.name + " , " + self.product_ID

    def checkAvailability(self):
        return self.isAvailable

    def changeAvailability(self):
        if self.checkAvailability == True:
            self.isAvailable = False
        else:
            self.isAvailable = True

    def getName(self):
        return self.name

    def changeName(self, newName):
        self.name = newName

    def getID(self):
        return self.product_ID
    
    def changeID(self, newID):
        self.product_ID = newID