import unittest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from data_procession import predict_users


class TestPredictUsers(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='[{"userId": 1, "isOnline": true, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T18:38:28", null]]}]')
    def test_predict_users_single_user_online(self, mock_file):
        date = datetime.now()
        result = predict_users(date)
        self.assertEqual(result['onlineUsers'], 1)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"userId": 1, "isOnline": false, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T18:38:28", "2023-10-05T19:38:28"]]}]')
    def test_predict_users_single_user_offline(self, mock_file):
        date = datetime.now() + timedelta(hours=2)
        result = predict_users(date)
        self.assertEqual(result['onlineUsers'], 0)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"userId": 1, "isOnline": true, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T18:38:28", null]]}, {"userId": 2, "isOnline": false, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T17:38:28", "2023-10-05T18:38:28"]]}]')
    def test_predict_users_multiple_users(self, mock_file):
        date = datetime.now()
        result = predict_users(date)
        self.assertEqual(result['onlineUsers'], 1)

unittest.main()

