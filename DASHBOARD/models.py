from django.db import models

# Create your models here.
from django.db import models

class Budget(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    budget_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_used = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def percentage_used(self):
        if self.budget_goal > 0:
            return (self.budget_used / self.budget_goal) * 100
        return 0
