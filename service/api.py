import requests
from django.conf import settings


def response_wrapper(response: requests.Response):
    return response.ok, response.json()


class ServiceRequest:
    @staticmethod
    def get_url(endpoint: str):
        return settings.SINGLE_API_URL + endpoint

    @staticmethod
    def get(endpoint: str, params: dict = None):
        return response_wrapper(requests.get(ServiceRequest.get_url(endpoint),
                                             headers={'Authorization': 'Bearer ' +
                                                      settings.SERVICE_SECRET},
                                             params=params
                                             ))

    @staticmethod
    def post(endpoint: str, data: dict = None):
        return response_wrapper(requests.post(ServiceRequest.get_url(endpoint),
                                              headers={'Authorization': 'Bearer ' +
                                                       settings.SERVICE_SECRET, 'Content-Type': 'application/json'},
                                              json=data))
