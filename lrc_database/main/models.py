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
    isAvailable = models.BooleanField()
    reserved_dates = []
    #need to store all time periods for reserved loans for each
    #piece of hardware

    def __str__(self):
        return f'{self.name}, {self.product_ID}'
class Loan(models.Model):
    target = models.ForeignKey(to=Hardware, related_name='hardware_requested', on_delete=models.CASCADE, help_text='Equipment being requested' )
    loan_start = models.DateTimeField('start time and date of loan')
    loan_return = models.DateTimeField(help_text='return time and date of loan')
    recipient = models.ForeignKey(to=LRCDatabaseUser, on_delete=models.CASCADE)

    def checkAvailabilty(self):
        for loans in self.target.reserved_dates:
            #self is same as existing loan
            if self.loan_start == loans.loan_start and self.loan_end == loans.loan_end:
                return False
            #self wants to end after another loan has started
            if self.loan_return > loans.loan_start and self.loan_return < loans.loan_return:
                return False
            #self is completely within the bounds of another loan
            if self.loan_start > loans.loan_start and self.loan_return < loans.loan_return:
                return False
            #self starts before another loan ends
            if self.loan_start > loans.start and self.loan_start < loans.loan_return:
                return False
        self.add_loan()
        return True
                

    def add_loan(self):
        self.target.reserved_dates.append(self)

    def __str__(self):
        if self.checkAvailability():
            return f'{self.recipient}\nLoan Start Date: {self.start_loan}\nLoan End Date: {self.return_loan}\nItem: {self.target}'
        else:
            return f'Item: {self.target} is unavailable at that designated time'

    # def checkAvailability(self):
    #     return self.isAvailable

    # def changeAvailability(self):
    #     if self.checkAvailability == True:
    #         self.isAvailable = False
    #     else:
    #         self.isAvailable = True

    # def getName(self):
    #     return self.name

    # def changeName(self, newName):
    #     self.name = newName

    # def getID(self):
    #     return self.product_ID
    
    # def changeID(self, newID):
    #     self.product_ID = newID