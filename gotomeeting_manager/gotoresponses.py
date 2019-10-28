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
    def create_from_dict(cls, user_data: Dict):
        first_name = user_data["firstName"]
        last_name = user_data["lastName"]
        email = user_data["email"]
        group_id = user_data["groupId"]
        status = user_data["status"]
        organizer_key = user_data["organizerKey"]
        try:
            products = user_data["products"]
        except KeyError:
            products = ""
        max_num_attendees_allowed = user_data["maxNumAttendeesAllowed"]

        return cls(first_name=first_name, last_name=last_name, email=email, group_id=group_id, status=status,
                   organizer_key=organizer_key, products=products,
                   max_num_attendees_allowed=max_num_attendees_allowed)

    def to_dict(self) -> Dict:
        user = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "group_id": self.group_id,
            "status": self.status,
            "organizer_key": self.organizer_key,
            "products": self.products,
            "max_num_attendees_allowed": self.max_num_attendees_allowed
        }

        return user


class GroupResponse:

    def __init__(self, group_key, group_name, parent_key, status, num_organizers):
        self.group_key = group_key
        self.group_name = group_name
        self.parent_key = parent_key
        self.status = status
        self. num_organizers = num_organizers

    @classmethod
    def create_from_dict(cls, group_data: Dict):
        group_key = group_data["groupkey"]
        group_name = group_data["groupName"]
        parent_key = group_data["parentKey"]
        status = group_data["status"]
        num_organizers = group_data["numOrganizers"]

        return cls(group_key=group_key, group_name=group_name, parent_key=parent_key, status=status,
                   num_organizers=num_organizers)

    def to_dict(self) -> Dict:
        group = {
            "group_key": self.group_key,
            "group_name": self.group_name,
            "parent_key": self.parent_key,
            "status": self.status,
            "num_organizers": self.num_organizers
        }

        return group

