from apps.sms.services.sms_base_class import (SmsBaseHelper, SmsProvider)
from apps.sms.models.sms_log import SmsLog
from apps.sms.models.enums.status import Status
from apps.sms.models.sms_organization_provider import OrganizationSmsProvider
from apps.company.models.institution import Institution

from django.contrib.auth import get_user_model

import requests
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class SmsOrganizationHelper:

    def __init__(self, institution_id: int):
        self.institution_id = institution_id
        self.provider_type = self.get_sms_provider_type()

    def get_sms_provider_type(self) -> [SmsProvider, None]:
        """ """
        provider_type = None
        institution = Institution.objects.get(id=self.institution_id)
        user = institution.user
        organization_sms_provider = user.organizationsmsprovider_set.filter(
            is_active=True).first() if user.is_organization else None

        if not organization_sms_provider:
            logger.info(f"SmsOrganizationHelper: No sms provider for user {user.id}")
            return provider_type

        if str(institution.id) not in map(str, organization_sms_provider.institutions.values_list("id", flat=True)):
            logger.info(f"SmsOrganizationHelper: Institution {str(institution.id)} not found at sms providers data.")
            return provider_type

        if organization_sms_provider.title == SmsProvider.SMS_AERO.value:
            provider_type = SmsProvider.SMS_AERO
        elif organization_sms_provider.title == SmsProvider.TWILIO.value:
            provider_type = SmsProvider.TWILIO
        else:
            logger.info(f"SmsOrganizationHelper: Provider type not found for user id {user.id}.")
            return provider_type

        return provider_type

    def send_sms(self, to_phone: str, message: str) -> bool:
        if self.provider_type:
            institution = Institution.objects.get(id=self.institution_id)
            sms_provider = OrganizationSmsProvider.objects.get(
                user_id=institution.user_id,
                institutions=institution
            )
            if self.provider_type == SmsProvider.TWILIO:
                base_url = "https://api.twilio.com/2010-04-01"
                account_sid = sms_provider.api_login
                auth_token = sms_provider.api_key
                url = f"{base_url}/Accounts/{account_sid}/Messages.json"
                data = {
                    "From": sms_provider.from_phone,
                    "To": to_phone,
                    "Body": message
                }
                response = requests.post(
                    url, data=data, auth=(account_sid, auth_token)
                )
                if response.status_code == 201:
                    res = response.json()
                    user = User.objects.filter(phone=to_phone).first()
                    SmsLog.objects.create(
                        sms_id=res["sid"],
                        text=res["body"],
                        status=Status.SENT,
                        recipient_id=user.id if user else None,
                        phone=to_phone
                    )
                    logger.info(f"SmsOrganizationHelper: Message sent from provider id {sms_provider.id}")
                    return True
                else:
                    res = response.json()
                    user = User.objects.filter(phone=to_phone).first()
                    SmsLog.objects.create(
                        sms_id=res["code"],
                        text=res["message"],
                        status=Status.FAILED,
                        recipient_id=user.id if user else None,
                        phone=to_phone
                    )
                    logger.error(f"SmsOrganizationHelper: Message not sent from provider id {sms_provider.id}. Response: {res}")
                    return False

        return False

