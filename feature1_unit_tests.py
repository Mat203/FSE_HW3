import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
import data_procession
from datetime import timezone

class TestGetData(unittest.TestCase):
    @patch('requests.get')
    def test_Should_ReturnData_When_GetDataCalledWithValidOffset(self, mock_get):
        mock_response = MagicMock()
        expected_data = {'data': 'test_data'}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        result = data_procession.get_data(0)

        self.assertEqual(result, expected_data['data'])

class TestUpdateUserData(unittest.TestCase):
    def test_Should_ReturnUpdatedUser_When_UpdateUserDataCalledWithValidUserAndPreviousState(self):
        user = {'userId': 'test_user', 'isOnline': True}
        previous_state = {'test_user': {'isOnline': False, 'onlinePeriods': []}}

        result = data_procession.update_user_data(user, previous_state)

        self.assertEqual(result['onlinePeriods'][0][1], None)

class TestFetchAndUpdateData(unittest.TestCase):
    @patch('json.dump')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('data_procession.get_data')
    def test_Should_UpdateAllData_When_FetchAndUpdateDataCalled(self, mock_get_data, mock_open, mock_dump):
        mock_get_data.side_effect = [[{'userId': 'test_user', 'isOnline': True, 'lastSeenDate': '2023-09-25T17:26:28.123456+03:00'}], []]

        data_procession.fetch_and_update_data()

        self.assertEqual(len(data_procession.previous_state), 1)
        self.assertEqual(len(data_procession.previous_state['test_user']['onlinePeriods']), 1)

class TestGetUsersOnline(unittest.TestCase):
    @patch('json.load')
    @patch('builtins.open', new_callable=MagicMock)
    def test_Should_ReturnUsersOnline_When_GetUsersOnlineCalledWithValidDate(self, mock_open, mock_load):
        user = {'userId': 'test_user', 'isOnline': True, 'onlinePeriods': [['2023-09-25T17:26:28.123456', None]]}
        mock_load.return_value = [user]
        date = datetime.now()

        result = data_procession.get_users_online(date)

        self.assertEqual(result, 1)

unittest.main()
