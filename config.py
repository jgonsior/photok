import os

class Config(object):
    USER_APP_NAME = 'photok'

    # we kind of don't use a mail server
    USER_SEND_PASSWORD_CHANGED_EMAIL=False
    USER_SEND_REGISTERED_EMAIL=False
    USER_SEND_USERNAME_CHANGED_EMAIL=False
    USER_ENABLE_CONFIRM_EMAIL=False

    if 'OPENSHIFT_APP_NAME' in os.environ:
        # we're obviously running the app now on openshift
        DEBUG = False
        TESTING = False
        CSREF_ENABLED=True
        SQLALCHEMY_DATABASE_URI=os.environ['OPENSHIFT_MYSQL_DB_URL'] + os.environ['OPENSHIFT_APP_NAME']
        SQLALCHEMY_ECHO = False
        Debug = False
        SECRET_KEY=os.environ['OPENSHIFT_SECRET_TOKEN']
    else:
        # hopefully this is on our local development machines :)
        SQLALCHEMY_DATABASE_URI ="sqlite:///testdb.db"
        DEBUG = True
        SECRET_KEY='rHh4lhSreFb0d7jktTMP53FuXz79hd4VzoEpVnER'
        CSRF_ENABLED=False
