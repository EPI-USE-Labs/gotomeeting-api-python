import os
from gotomeeting_manager import gotomanager

FIRSTNAME = "Chanel"
LASTNAME = "du Plessis"
EMAIL = "chanel@labs.epiuse.com"
PRODUCTS = "G2M"

if __name__ == "__main__":
    manager = gotomanager.Manager(path_to_config="./.creds")
    user = manager.create_user(first_name=FIRSTNAME, last_name=LASTNAME, email=EMAIL, products=PRODUCTS)
    # user = manager.get_user_by_email(email="tihan@labs.epiuse.com")
    print(user)
