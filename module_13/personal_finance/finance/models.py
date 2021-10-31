from django.db import models
from django.conf import settings
from django.utils.timezone import now


class TransactionCategory(models.Model):
    name = models.TextField(verbose_name="Name of category")
    code = models.CharField(max_length=10)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories"
    )


class Transaction(models.Model):
    created = models.DateTimeField(
        # auto_now_add=True для автоматического использования отметки времени при добавлении объекта.
        # Это также установит для поля значение blank=Trueи editable=False.
        default=now,
        verbose_name="Created timestamp"
    )
    amount = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2,
    )
    comment = models.TextField(verbose_name="Transaction comments", null=True)

    categories = models.ForeignKey(
        TransactionCategory,
        on_delete=models.CASCADE
        # ,related_name="transactions_category"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
