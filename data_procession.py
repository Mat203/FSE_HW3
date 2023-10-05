import requests
import json
import time
from datetime import datetime

def get_data(offset):
    url = f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}"
    response = requests.get(url)
    data = response.json()
    return data['data']

def update_user_data(user, previous_state):
    if user['isOnline']:
        if user['userId'] not in previous_state or not previous_state[user['userId']]['isOnline']:
            user['onlinePeriods'] = previous_state.get(user['userId'], {}).get('onlinePeriods', [])
            user['onlinePeriods'].append([datetime.now().isoformat(), None])
        else:
            user['onlinePeriods'] = previous_state[user['userId']]['onlinePeriods']
    else:
        if user['userId'] in previous_state and previous_state[user['userId']]['isOnline']:
            last_online_period = previous_state[user['userId']]['onlinePeriods'][-1]
            last_online_period[1] = datetime.now().isoformat()
            user['onlinePeriods'] = previous_state[user['userId']]['onlinePeriods']
        else:
            user['onlinePeriods'] = previous_state.get(user['userId'], {}).get('onlinePeriods', [])
    return user

previous_state = {} 

def fetch_and_update_data():
    offset = 0
    all_data = []

    while True:
        data = get_data(offset)

        if not data:
            break

        for d in data:
            user = { 'userId': d['userId'], 'isOnline': d['isOnline'], 'lastSeenDate': d['lastSeenDate'] }
            updated_user = update_user_data(user, previous_state)
            all_data.append(updated_user)
            previous_state[updated_user['userId']] = updated_user

        offset += len(data)

    with open('all_data.json', 'w') as f:
        json.dump(all_data, f)

def get_users_online(date):
    with open('all_data.json', 'r') as f:
        all_data = json.load(f)

    users_online = 0

    for user in all_data:
        for period in user['onlinePeriods']:
            start = datetime.fromisoformat(period[0])
            end = datetime.fromisoformat(period[1]) if period[1] else datetime.now()

            if start <= date <= end:
                users_online += 1
                break

    return users_online

def get_user_data(date, userId):
    with open('all_data.json', 'r') as f:
        all_data = json.load(f)

    user_data = next((user for user in all_data if user['userId'] == userId), None)

    if user_data is None:
        return None

    wasUserOnline = None
    nearestOnlineTime = None

    for period in user_data['onlinePeriods']:
        start = datetime.fromisoformat(period[0])
        end = datetime.fromisoformat(period[1]) if period[1] else datetime.now()

        if start <= date <= end:
            wasUserOnline = True
            break

    if wasUserOnline is None:
        wasUserOnline = False
        nearestPeriod = min(user_data['onlinePeriods'], key=lambda period: abs(date - datetime.fromisoformat(period[0])))
        nearestOnlineTime = nearestPeriod[0]

    return {'wasUserOnline': wasUserOnline, 'nearestOnlineTime': nearestOnlineTime}

def predict_users(date):
    #this will be feature 3
    return

def predict_user(date, userId):
    #here we will predict user (feature 4)
    return

if __name__ == "__main__":
    while True:
        fetch_and_update_data()
        time.sleep(10)