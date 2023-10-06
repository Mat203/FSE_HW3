import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import data_procession

class TestGetUserData(unittest.TestCase):
    @patch('json.load')
    @patch('builtins.open', new_callable=MagicMock)
    def test_Should_ReturnUserData_When_GetUserDataCalledWithValidDateAndUserId(self, mock_open, mock_load):
        user = {'userId': 'test_user', 'isOnline': True, 'onlinePeriods': [['2023-09-25T17:26:28.123456', None]]}
        mock_load.return_value = [user]
        date = datetime.now()

        result = data_procession.get_user_data(date, 'test_user')

        self.assertEqual(result['wasUserOnline'], True)
        self.assertEqual(result['nearestOnlineTime'], None)

    @patch('json.load')
    @patch('builtins.open', new_callable=MagicMock)
    def test_Should_ReturnNone_When_GetUserDataCalledWithInvalidUserId(self, mock_open, mock_load):
        user = {'userId': 'test_user', 'isOnline': True, 'onlinePeriods': [['2023-09-25T17:26:28.123456', None]]}
        mock_load.return_value = [user]
        date = datetime.now()

        result = data_procession.get_user_data(date, 'invalid_user')

        self.assertEqual(result, None)

unittest.main()
