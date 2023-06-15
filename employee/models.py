from django.db import models

from core.model import CoreModel, CoreModelSoftDelete
# Create your models here.


class Department(CoreModelSoftDelete):
    title = models.CharField(max_length=100)


class Employee(CoreModelSoftDelete):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department,  on_delete=models.DO_NOTHING, db_constraint=False)
    birthdate = models.DateField(null=True, blank=True)
