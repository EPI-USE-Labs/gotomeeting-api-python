import requests
from typing import Dict


class UserResponse:

    def __init__(self, first_name, last_name, email, group_id, status, organizer_key, products,
                 max_num_attendees_allowed):

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.group_id = group_id
        self.status = status
        self.organizer_key = organizer_key
        self.products = products
        self. max_num_attendees_allowed = max_num_attendees_allowed

    @classmethod
    def create_from_response(cls, response_data: Dict):

        try:
            first_name = response_data["firstName"]
            last_name = response_data["lastName"]
            email = response_data["email"]
            group_id = response_data["groupId"]
            status = response_data["status"]
            organizer_key = response_data["organizerKey"]
            products = response_data["products"]
            max_num_attendees_allowed = response_data["maxNumAttendeesAllowed"]

            return cls(first_name=first_name, last_name=last_name, email=email, group_id=group_id, status=status,
                       organizer_key=organizer_key, products=products,
                       max_num_attendees_allowed=max_num_attendees_allowed)

        except KeyError:
            return None


class GroupResponse:

    def __init__(self, group_key, group_name, parent_key, status, num_organizers):
        self.group_key = group_key
        self.group_name = group_name
        self.parent_key = parent_key
        self.status = status
        self. num_organizers = num_organizers

    @classmethod
    def create_from_response(cls, response_data: Dict):

        try:
            group_key = response_data["groupKey"]
            group_name = response_data["groupName"]
            parent_key = response_data["parentKey"]
            status = response_data["status"]
            num_organizers = response_data["numOrganizers"]

            return cls(group_key=group_key, group_name=group_name, parent_key=parent_key, status=status,
                       num_organizers=num_organizers)

        except KeyError:
            return None
