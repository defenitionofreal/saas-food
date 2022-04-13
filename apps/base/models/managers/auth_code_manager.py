from django.db.models import Manager
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
from random import randint


class AuthCodeManager(Manager):
    def active(self):
        from_date = now() - timedelta(
            seconds=settings.AUTHENTICATION_CODE_EXPIRED)
        return self.filter(is_active=True, created_at__gt=from_date)

    def _generate_code(self, user):
        attempts_count = 0
        active_codes = set(self.active().filter(user=user).values_list(
            "code", flat=True))

        generated_code = None
        while attempts_count < settings.MAX_GENERATE_ATTEMPTS_COUNT and not generated_code:
            code = randint(1000, 9999)
            if str(code) not in active_codes:
                generated_code = code
            attempts_count += 1

        if attempts_count >= settings.MAX_GENERATE_ATTEMPTS_COUNT or not generated_code:
            raise ValueError(
                f"Превышено количество попыток создания кода {settings.MAX_GENERATE_ATTEMPTS_COUNT} для {user.pk}")

        return generated_code

    def generate(self, user):
        code = self._generate_code(user)
        instance = self.create(user=user, code=code)
        return instance
