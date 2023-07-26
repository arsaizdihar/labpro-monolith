import requests
from django.conf import settings


class ServiceRequest:
    @staticmethod
    def get_url(endpoint: str):
        return settings.SINGLE_API_URL + endpoint

    @staticmethod
    def get(endpoint: str, params: dict = None):
        return requests.get(ServiceRequest.get_url(endpoint),
                            headers={'Authorization': 'Bearer ' +
                                     settings.SERVICE_SECRET},
                            params=params
                            )

    @staticmethod
    def post(endpoint: str, data: dict = None):
        return requests.post(ServiceRequest.get_url(endpoint),
                             headers={'Authorization': 'Bearer ' +
                                      settings.SERVICE_SECRET, 'Content-Type': 'application/json'},
                             json=data)
