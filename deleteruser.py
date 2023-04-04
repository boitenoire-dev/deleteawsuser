import boto3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-u',
    '--username',
    help="A comma separated list of users to inactivate",
    required=True
)

args = parser.parse_args()

session = boto3.Session(profile_name="[profile name in .aws/credentials file]")
iam_client = session.client('iam')

username = [un for un in args.username.split(',')]

def delete_user_keys(username):
    '''
    This function loops through the user names provided in in the CLI prompt and returns then deactivates the key
    of said user. If user exists, but doesn't have a key the script will notify of that situation.
    :param username:
    '''

    for user in username:
        try:
            list_of_keys = iam_client.list_access_keys(
                UserName=user,
            )
            if len(list_of_keys['AccessKeyMetadata']) == 0:
                print(f"{user} exists but has no key")
            else:
                for key_id in list_of_keys['AccessKeyMetadata']:
                    if key_id['AccessKeyId']:
                        print(f"{user}'s key is {key_id['AccessKeyId']}")
                        list_of_keys = iam_client.delete_access_key(
                            UserName=user,
                            AccessKeyId=key_id['AccessKeyId']
                        )
                        print(f"{user}'s key {key_id['AccessKeyId']} was deleted")

        except iam_client.exceptions.NoSuchEntityException as e:
            print(e)


def delete_user_login(username):
    '''
    This function loops through the user names provided in in the CLI prompt and returns then deletes the login profile
    of said user. If user exists, but doesn't have a key the script will notify of that situation.
    :param username:
    '''
    for user in username:
        try:
            response = iam_client.delete_login_profile(
                UserName=user,
            )
            print(response)
            print(f"{user} had their profile deleted")
        except iam_client.exceptions.NoSuchEntityException as e:
            print(e)


def main():
    delete_user_keys(username)
    delete_user_login(username)


if __name__ == '__main__':
    main()
