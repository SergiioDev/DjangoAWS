from django.db import models


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimestampModel):
    name = models.CharField(max_length=255)
    registration_code = models.CharField(max_length=50, unique=True)
    established_on = models.DateField()
    address = models.TextField(null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
