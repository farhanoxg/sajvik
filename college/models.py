from django.db import models

class College(models.Model):
    # id = models.AutoField(primary_key=True) 
    # year = models.IntegerField()
    # institute_type = models.CharField(max_length=255)
    institute_name = models.CharField(max_length=255)
    program_name = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    seat_type = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    # opening_rank = models.IntegerField()
    closing_rank = models.IntegerField()

    class Meta:
        managed = False 
        db_table = 'sajvik_data' 

    def __str__(self):
        return f"{self.institute_name} ({self.program_name})"
