from django.contrib.auth.models import BaseUserManager
from api.utilities import generate_unique_user_id

class APIUserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None):
        if not email:
            raise ValueError('email is required')
        
        email = self.normalize_email(email)

        user = self.model(email=email)
        user.is_active = True
        user.set_password(password)
        user.user_id = generate_unique_user_id(user)

        user.save(using = self.db)

        return user
    
    def create_superuser(self, email, password=None):
       
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.user_id = generate_unique_user_id(user)

        user.save(using=self.db)
    
        return user
        