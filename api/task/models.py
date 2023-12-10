from django.db import models
from main.models import Log
# from django.utils.text import slugify
from api.users.models import User

class StatusManager(models.Manager):
    def create_status(self,incStatus):
        status = self.create(name=incStatus)
        return status

class Status(Log):
    """
    Statuses for a task
    """

    CHOICES = ['Pending','Progress','Complete','Rejected']

    name = models.CharField(max_length=255, db_column='Name', default='Pending')
    # code = models.SlugField(db_column='Code', default='')
    # access_level = models.IntegerField(max_length=255, choices=CHOICES, db_column='CurrentStatus', default=STATUS_PENDING_CODE)

    class Meta:
        db_table = 'Statuses'

    def __str__(self):
        return f'{self.name}'

    objects = StatusManager()

    # def save(self,*args,**kwargs):
    #     try:
    #         if not self.pk:
    #             self.code = slugify(self.name)
    #         super().save()
    #     except Exception:
    #         raise

class TaskManager(models.Manager):
    def create_task(self, argTitle, argDesc, argTimeEst, user, argStatus):
        task = self.create(title=argTitle, description=argDesc, time_estimation=argTimeEst, assigned_to=user, status=argStatus)
        return task

class Task(Log):
    title = models.CharField(max_length=255, db_column='Title')
    description = models.TextField(db_column='Description', null=True)
    assigned_to = models.ForeignKey(User, db_column='AssignedTo', null=False, blank=False, on_delete=models.CASCADE) # make it foreign key -> on del models.Protect ,until user deletes all his tasks it cant be removed
    time_estimation = models.TimeField(auto_now_add=False, null=True)
    status = models.ForeignKey(Status, db_column='StatusID', on_delete=models.SET_NULL, null=True) #models.SET_NULL: if any status removed then null sets on this field of task


    class Meta:
        db_table = 'Tasks'

    def __str__(self):
        return f'{self.title}'

    objects = TaskManager()