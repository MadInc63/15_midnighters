import requests
import pytz
import datetime


def load_attempts():
    pages = 1
    for page in range(1, pages+1):
        response = requests.get('http://devman.org/api/challenges/'
                                'solution_attempts', params={'page': page})
        json_data = response.json()
        number_of_pages = json_data['number_of_pages']
        for record in json_data['records']:
            yield {
                   'username': record['username'],
                   'timestamp': record['timestamp'],
                   'timezone': record['timezone'],
                  }
        if page == number_of_pages:
            print('This URL has only {} pages and '
                  'all of them are received'.format(page))
            break


def get_midnighters(users):
    user_time_zone = pytz.timezone(users['timezone'])
    timestamp = datetime.datetime.fromtimestamp(int(users['timestamp']))
    user_time = user_time_zone.localize(timestamp)
    if 0 <= int(user_time.strftime('%H')) < 6:
        print('User {} post your code at {}'.format(users['username'],
                                                    user_time.strftime
                                                    ('%H:%M:%S')))


if __name__ == '__main__':
    for user in load_attempts():
        get_midnighters(user)
