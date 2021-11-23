from django.contrib.auth.models import User
from . import models
def getUserRole(request):
    role=str(request.user)
    if role !="AnonymousUser":
        user=User.objects.get(username=role)
        account = models.Account.objects.filter(user=user).values('role')[0]
        role=account['role']        
    return role