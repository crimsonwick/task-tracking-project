from django.db import models

# Create your models here.
class Log(models.Model):
    """
    abstract class with common fields to keep track of changes.
    """
    created_by = models.BigIntegerField(db_column='Created_By', null=True, blank=True, default=0)
    created_on = models.DateTimeField(db_column='Created_On', auto_now_add=True)

    modified_by = models.BigIntegerField(db_column='Modified_By', null=True, blank=True, default=0)
    modified_on = models.DateTimeField(db_column='Modified_On', null=True, blank=True, auto_now_add=True)

    deleted_by = models.BigIntegerField(db_column='Deleted_By', null=True, blank=True, default=0)
    deleted_on = models.DateTimeField(db_column='Deleted_On', auto_now_add=True)

    class Meta:
        abstract = True