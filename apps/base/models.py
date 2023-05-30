from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    deleted = models.DateField(auto_now=True)
    historical = HistoricalRecords(user_model="users.User", inherit=True)

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
    

    class Meta:
        abstract = True