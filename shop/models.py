from django.db import models
from django.conf import settings

class PurchaseRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sport_type = models.CharField(max_length=100)
    goals = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    program_file = models.FileField(upload_to='programs', blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ref_id = models.CharField(max_length=100, blank=True, null=True)
    pen_card = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request by {self.user.username} - {self.sport_type}"
