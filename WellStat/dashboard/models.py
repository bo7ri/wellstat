from django.db import models

# Create your models here.
from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    medical_documents = models.FileField(upload_to='medical_documents/', blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class RiskAssessment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    risk_factors = models.TextField()
    risk_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.risk_score}"