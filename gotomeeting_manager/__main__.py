from gotomeeting_manager.gotomanager import Manager
from config.shared_config import SharedConfig


if __name__ == "__main__":
    conf = SharedConfig().config
    manager = Manager(consumer_key=conf["gotomeeting"]["key"], consumer_secret=conf["gotomeeting"]["secret"])
    # manager.create_user_in_group(firstname="Thomas",
    #                              lastname="Scholtz",
    #                              email="thomas@labs.epiuse.com",
    #                              group_name="EPI-USE Labs")
    # manager.get_user_by_email(email="thomas@labs.epiuse.com")
    # manager.delete_user_by_key("thomas@labs.epiuse.com")