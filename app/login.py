# This script fetches the first login token and saves it as file in the current directory
from teslapy import Tesla

from .config.settings import settings

with Tesla(settings.tesla_account_email) as tesla:
    if not tesla.authorized:
        print('Use browser to login. Page Not Found will be shown at success.')
        print('Open this URL: ' + tesla.authorization_url())
        tesla.fetch_token(authorization_response=input('Enter URL after authentication: '))

    print("Vehicle information:")
    print(tesla.vehicle_list()[0])
