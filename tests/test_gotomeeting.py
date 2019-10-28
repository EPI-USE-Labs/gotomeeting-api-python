from gotomeeting_manager import gotomanager

TEST_FIRSTNAME = ""
TEST_LASTNAME = ""
TEST_EMAIL = ""
TEST_USER_KEY = ""
TEST_GROUP_NAME = ""
TEST_PRODUCTS = []



def test_create_user():
    gotomeeting = gotomanager.Manager()
    gotomeeting.create_user(first_name=TEST_FIRSTNAME, last_name=TEST_LASTNAME, email=TEST_EMAIL)


def test_create_user_in_group():
    gotomeeting = gotomanager.Manager()
    gotomeeting.create_user_in_group(first_name=TEST_LASTNAME, last_name=TEST_LASTNAME, email=TEST_EMAIL,
                                     group_name=TEST_GROUP_NAME)


def test_get_user_by_email():
    gotomeeting = gotomanager.Manager()
    user = gotomeeting.get_user_by_email(email=TEST_EMAIL)


def test_get_user_by_key():
    gotomeeting = gotomanager.Manager()
    user = gotomeeting.get_user_by_key(key=TEST_USER_KEY)


def test_get_all_users():
    gotomeeting = gotomanager.Manager()
    users = gotomeeting.get_all_users()


def test_get_groups():
    gotomeeting = gotomanager.Manager()
    user = gotomeeting.get_groups()


def test_update_user():
    gotomeeting = gotomanager.Manager()
    user = gotomeeting.update_user_products(email=TEST_EMAIL, products=TEST_PRODUCTS)


def test_suspend_user():
    gotomeeting = gotomanager.Manager()
    user = gotomeeting.suspend_user(email=TEST_EMAIL)
