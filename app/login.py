# This script fetches the first login token and saves it as file in the current directory
import argparse

from teslapy import Tesla

parser = argparse.ArgumentParser(description="Tesla API token fetcher")
parser.add_argument("-f", "--token-file-path", help="Path for the token file inside the docker container", required=True)
parser.add_argument("-e", "--email", help="E-Mail address of Tesla account", required=True)

args = vars(parser.parse_args())

with Tesla(args["email"], cache_file=args["token_file_path"]) as tesla:
    if not tesla.authorized:
        print('Use browser to login. Page Not Found will be shown at success.')
        print('Open this URL: ' + tesla.authorization_url())
        tesla.fetch_token(authorization_response=input('Enter URL after authentication: '))

    print("Vehicle information:")
    print(tesla.vehicle_list()[0])
