from django.db import models

# Create your models here.

class Feedback(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    message = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to='images/', null=True, max_length=255)

    def __repr__(self):
        return 'Image(%s, %s, %s, %s)' % (self.name, self.email, self.message, self.image)

    def __str__ (self):
        return self.email
