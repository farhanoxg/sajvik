from django.db import models

class College(models.Model):
    institute_name = models.CharField(max_length=255)
    program_name = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    seat_type = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    closing_rank = models.IntegerField()

    class Meta:
        managed = False 
        db_table = 'sajvik_data' 

    def __str__(self):
        return f"{self.institute_name} ({self.program_name})"
