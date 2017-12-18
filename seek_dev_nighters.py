import requests
import pytz
import datetime


def load_attempts():
    response = requests.get(
        'http://devman.org/api/challenges/solution_attempts'
    ).json()
    pages = response['number_of_pages']
    for page in range(1, pages+1):
        response = requests.get(
            'http://devman.org/api/challenges/'
            'solution_attempts', params={'page': page}
        )
        response_dict = response.json()
        for record in response_dict['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def get_user_local_time(user):
    user_time_zone = pytz.timezone(user['timezone'])
    local_time = datetime.datetime.fromtimestamp(
        user['timestamp'],
        user_time_zone
    )
    return local_time


if __name__ == '__main__':
    for attempt in load_attempts():
        user_time = get_user_local_time(attempt)
        if 0 <= int(user_time.strftime('%H')) < 6:
            print(
                'User {} post your code at {}'.format(
                    attempt['username'],
                    user_time.strftime('%H:%M:%S')
                )
            )
