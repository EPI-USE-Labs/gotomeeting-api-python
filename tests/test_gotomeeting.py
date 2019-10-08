from gotomeeting_manager import gotomanager


def test_create_user():
    gotomeeting = gotomanager.Manager(consumer_key="qj37k793dpfOQgGWtif35m4nSxWpbZiM", consumer_secret="D0wQWFxFMT7hQ5Qy")
    gotomeeting.create_user(firstname="Thom", lastname="Schoff", email="tihan+test@labs.epiuse.com")


def test_request_tokens():
    gotomeeting = gotomanager.Manager(consumer_key="qj37k793dpfOQgGWtif35m4nSxWpbZiM",
                                      consumer_secret="D0wQWFxFMT7hQ5Qy")
    gotomeeting._request_tokens(auth_code="77ff1d20fdd12fb9a5c19d00d0add887")
