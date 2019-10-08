from gotomeeting_manager import gotomanager


def test_create_user():
    gotomeeting = gotomanager.Manager(consumer_key="", consumer_secret="")
    gotomeeting.create_user(first_name="Thom", last_name="Schoff", email="tihan+test@labs.epiuse.com")


def test_request_tokens():
    gotomeeting = gotomanager.Manager(consumer_key="", consumer_secret="")
    gotomeeting._request_tokens(auth_code="")
