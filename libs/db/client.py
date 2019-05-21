from mongoengine import connect

from libs.config.config import DATABASE

client_url = "mongodb://{dbuser}:{dbpassword}@{host}/?authSource=admin".format(
    dbuser=DATABASE["user"], dbpassword=DATABASE["password"], host=DATABASE["host"]
)


def connect_to_database():
    connect(db=DATABASE["name"], host=client_url)
