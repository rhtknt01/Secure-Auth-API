from django.contrib.auth.models import BaseUserManager


class APIUserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None):
        if not email:
            raise ValueError('email is required')
        
        email = self.normalize_email(email)

        user = self.model(email=email)
        user.is_active = True
        user.set_password(password)

        user.save(using = self.db)

        return user
    
    def create_superuser(self, email, password=None):
       
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self.db)
    
        return user
        