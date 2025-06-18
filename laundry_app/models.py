from django.db import models
from django.utils.crypto import get_random_string

class LaundryOrder(models.Model):
    LAUNDRY_TYPE_CHOICES = [
        ('daily_kiloan', 'Daily Kiloan'),
        ('cuci_setrika', 'Cuci & Setrika'),
        ('dry_cleaning', 'Dry Cleaning'),
        ('green_dry_cleaning', 'Green Dry Cleaning'),
        ('laundry_sepatu', 'Laundry Sepatu'),
        ('laundry_tas', 'Laundry Tas'),
        ('laundry_karpet', 'Laundry Karpet'),
        ('laundry_gorden', 'Laundry Gorden'),
        ('laundry_kulit', 'Laundry Kulit'),
        ('lainnya', 'Lainnya'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    e_invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    address = models.TextField()
    whatsapp = models.CharField(max_length=20)
    laundry_type = models.CharField(max_length=30, choices=LAUNDRY_TYPE_CHOICES)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.e_invoice_number:
            self.e_invoice_number = self.generate_e_invoice_number()
        super().save(*args, **kwargs)

    def generate_e_invoice_number(self):
        prefix = 'EF'
        unique = False
        while not unique:
            random_str = get_random_string(length=8, allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            e_invoice = f"{prefix}{random_str}"
            if not LaundryOrder.objects.filter(e_invoice_number=e_invoice).exists():
                unique = True
        return e_invoice

    def __str__(self):
        return f"{self.name} - {self.e_invoice_number}"
