import requests
from typing import Dict


class UserResponse:

    def __init__(self, key, first_name, last_name, email, admin, locale, license_keys, group_key, group_name, products,
                 status):
        self.key = key
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.group_key = group_key
        self.group_name = group_name
        self.locale = locale
        self.license_keys = license_keys
        self.products = products
        self.admin = admin
        self.status = status

    @classmethod
    def create_from_dict(cls, user_data: Dict):
        key = user_data.get("key", None)
        first_name = user_data.get("firstName", None)
        last_name = user_data.get("lastName", None)
        email = user_data.get("email", None)
        locale = user_data.get("locale", None)
        license_keys = user_data.get("licenseKeys", None)
        group_key = user_data.get("groupKey", None)
        group_name = user_data.get("groupName", None)
        admin = user_data.get("admin", False)
        products = user_data.get("products", None)
        status = user_data.get("status", None)

        return cls(key=key, first_name=first_name, last_name=last_name, email=email, admin=admin, locale=locale,
                   license_keys=license_keys, group_key=group_key, group_name=group_name, products=products,
                   status=status)

    def to_dict(self) -> Dict:
        user = {
            "key": self.key,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "group_key": self.group_key,
            "group_name": self.group_name,
            "locale": self.locale,
            "license_keys": self.license_keys,
            "products": self.products,
            "admin": self.admin,
            "status": self.status
        }

        return user


class GroupResponse:

    def __init__(self, key, name, user_keys, total_member_count):
        self.key = key
        self.name = name
        self.user_keys = user_keys
        self.total_member_count = total_member_count

    @classmethod
    def create_from_dict(cls, group_data: Dict):
        key = group_data.get("groupKey", None)
        name = group_data.get("groupName", None)
        user_keys = group_data.get("userKeys", None)
        total_member_count = group_data.get("totalMemberCount", None)

        return cls(key=key, name=name, user_keys=user_keys, total_member_count=total_member_count)

    def to_dict(self) -> Dict:
        group = {
            "key": self.key,
            "name": self.name,
            "user_keys": self.user_keys,
            "total_member_count": self.total_member_count
        }

        return group

