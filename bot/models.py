from django.db import models

# Create your models here.
from django.db import models


class Transaction(models.Model):
    """Each interaction with target server is assumed
    a Transaction. Model class holds transaction details"""
    TR_TYPES = (
        ('D', 'On Demand'),
        ('A', 'Automatic'),
    )

    STATUSES = (
        ('S', 'Success'),
        ('F', 'Failure'),
        ('U', 'Unknown'),
    )

    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUSES, default='U')
    chat_id = models.IntegerField(default=0)
    text = models.CharField(max_length=100, default='')
    response = models.CharField(max_length=300, default='')
    tr_type = models.CharField(max_length=10, choices=TR_TYPES, default='A')
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ('timestamp',)

