from django.db import models

class Feeder(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DT(models.Model):
    CAPACITY_CHOICES = [
        ('25', '25 kVA'),
        ('63', '63 kVA'),
        ('100', '100 kVA'),
        ('160', '160 kVA'),
        ('250', '250 kVA'),
        ('315', '315 kVA'),
        ('500', '500 kVA'),
        # Add more as needed
    ]
    name = models.CharField(max_length=100)
    feeder = models.ForeignKey(Feeder, related_name="dts", on_delete=models.CASCADE)
    capacity = models.CharField(max_length=10, choices=CAPACITY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.capacity} kVA) ({self.feeder.name})"
        #return f"{self.name}  ({self.feeder.name})"

class LocationEntry(models.Model):
    name = models.CharField(max_length=100)  # Example field
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"


# models.py (add this model)

class FeederDTSelection(models.Model):
    feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE)
    dt = models.ForeignKey(DT, on_delete=models.CASCADE)
    start_point_lat = models.DecimalField(max_digits=9, decimal_places=6)
    start_point_lng = models.DecimalField(max_digits=9, decimal_places=6)
    end_point_lat = models.DecimalField(max_digits=9, decimal_places=6)
    end_point_lng = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.feeder.name} - {self.dt.name}"
