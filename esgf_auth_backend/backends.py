import os

from myproxy_logon import myproxy_logon, GetException

from django.contrib.auth.models import User
from django.conf import settings
if not settings.configured:
    settings.configure()

class ESGF_Auth_Backend:
    """
    Custom backend to log-in with an ESGF OpenID. Saves a certificate + private
    key as settings.proxy_cert_dir/username.pem
    (eg: /esgserver/proxycerts/jsmith.pem)
    """
    def authenticate(self, username=None, password=None):
        try:
            myproxy_logon(settings.ESGF_HOST,
                    username,
                    password,
                    os.path.join(settings.PROXY_CERT_DIR,
                                    username + '.pem').encode("UTF-8"),
                    lifetime=43200,
                    port=settings.ESGF_PORT
                    )
        except GetException as e:
            # myproxy_logon failed, so return None instead of a User
            #
            # TODO: When Django 1.6 comes out, this should be changed to:
            #
            #     raise PermissionDenied
            #
            # This will prevent the possibility of someone listing multiple
            # authentication backends in their settings.py, thus allowing an
            # attacker to authenticate as any user simply by using the default
            # password assigned to all users created by this auth backend.
            return None
            
        # if we make it here, the username and password were good
        # (myproxy_logon throws GetException if login fails)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Create a new user. Note that we can set password
            # to anything, because unless another authentication backend is
            # listed in settings.py's AUTHENTICATION_BACKENDS, this password
            # will never be seen.
            user = User(username=username,
                        password='password is not used, ESGF handles authentication for us')
            user.is_staff = False
            user.is_superuser = False
            user.save()
        return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None