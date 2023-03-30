from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Wallets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=25, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=100)

    def __str__(self):
        return self.user + " " + self.currency


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer')
    )

    wallet = models.ForeignKey(
        Wallets, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
