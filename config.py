import os
from datetime import timedelta

class Config(object):
    USER_APP_NAME = 'photok'

    # we kind of don't use a mail server
    USER_SEND_PASSWORD_CHANGED_EMAIL=False
    USER_SEND_REGISTERED_EMAIL=False
    USER_SEND_USERNAME_CHANGED_EMAIL=False
    USER_ENABLE_CONFIRM_EMAIL=False
    SQLALCHEMY_TRACK_MODIFICATIONS=True

    # URLs                        # Default
    USER_CHANGE_PASSWORD_URL      = '/user/change-password'
    USER_CHANGE_USERNAME_URL      = '/user/change-username'
    USER_CONFIRM_EMAIL_URL        = '/user/confirm-email/<token>'
    USER_EMAIL_ACTION_URL         = '/user/email/<id>/<action>'     # v0.5.1 and up
    USER_FORGOT_PASSWORD_URL      = '/user/forgot-password'
    USER_INVITE_URL               = '/user/invite'                  # v0.6.2 and up
    USER_LOGIN_URL                = '/user/login'
    USER_LOGOUT_URL               = '/user/logout'
    USER_MANAGE_EMAILS_URL        = '/user/manage-emails'
    USER_REGISTER_URL             = '/user/register'
    USER_RESEND_CONFIRM_EMAIL_URL = '/user/resend-confirm-email'    # v0.5.0 and up
    USER_RESET_PASSWORD_URL       = '/user/reset-password/<token>'


    if 'OPENSHIFT_APP_NAME' in os.environ:
        # we're obviously running the app now on openshift
        DEBUG = False
        TESTING = False
        CSRF_ENABLED=True
        SQLALCHEMY_DATABASE_URI=os.environ['OPENSHIFT_MYSQL_DB_URL'] + os.environ['OPENSHIFT_APP_NAME']
        SQLALCHEMY_ECHO = False
        SECRET_KEY=os.environ['OPENSHIFT_SECRET_TOKEN']
    else:
        # hopefully this is on our local development machines :)
        SQLALCHEMY_DATABASE_URI ="sqlite:///testdb.db"
        DEBUG = True
        SECRET_KEY='rHh4lhSreFb0d7jktTMP53FuXz79hd4VzoEpVnER'
        CSRF_ENABLED=False
        JWT_EXPIRATION_DELTA=timedelta(days=10)
