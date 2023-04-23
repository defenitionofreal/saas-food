from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, email, password=None,
                    is_organization=False, is_customer=False):
        if phone and email is None:
            user = self.model(phone=phone,
                              is_organization=is_organization,
                              is_customer=is_customer)
        elif email and phone is None:
            user = self.model(email=self.normalize_email(email),
                              is_organization=is_organization,
                              is_customer=is_customer)
        elif phone and email:
            user = self.model(phone=phone,
                              email=self.normalize_email(email),
                              is_organization=is_organization,
                              is_customer=is_customer)
        else:
            raise ValueError("User must have a phone or email")

        if not password:
            raise ValueError("User must have a password")

        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.is_superuser = False
        user.is_promo = False
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not password:
            raise ValueError("User must have a password")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_promo = False
        user.is_active = True
        user.save(using=self._db)
        return user
