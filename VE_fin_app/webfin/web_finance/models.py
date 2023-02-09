from django.db import models

class categories(models.Model):
    description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"ID({self.id}): {self.description}"

class User(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    login = models.CharField(max_length=255, unique=True)
    pswrd = models.CharField(max_length=255)
    prediction = models.FloatField()

    def __str__(self):
        return f"ID({self.id}): {self.name} {self.surname} {self.email} \
                 {self.login} {self.pswrd} {self.prediction}"

class spendings(models.Model):
    date = models.DateTimeField()
    amount = models.FloatField()
    category = models.ForeignKey(categories, null=True, on_delete=models.SET_NULL)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"ID({self.id}): {self.date} {self.amount} {self.category} {self.user}"

