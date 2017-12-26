import requests
import pytz
import datetime


def load_attempts():
    url = 'http://devman.org/api/challenges/solution_attempts'
    page = 1
    while True:
        response = requests.get(
            url,
            params={'page': page}
        ).json()
        for record in response['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }
        if page == response['number_of_pages']:
            break
        page += 1


def get_user_local_time(user):
    user_time_zone = pytz.timezone(user['timezone'])
    local_time = datetime.datetime.fromtimestamp(
        user['timestamp'],
        user_time_zone
    )
    return local_time


if __name__ == '__main__':
    for attempt in load_attempts():
        midnight = 0
        sunrise = 6
        user_time = get_user_local_time(attempt)
        if midnight <= int(user_time.strftime('%H')) < sunrise:
            print(
                'User {} post your code at {}'.format(
                    attempt['username'],
                    user_time.strftime('%H:%M:%S')
                )
            )
