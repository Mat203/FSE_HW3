import unittest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from data_procession import predict_user

class TestPredictUser(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='[{"userId": 1, "isOnline": true, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T18:38:28", null]]}]')
    def test_Should_ReturnOnlineChanceAndPrediction_When_PredictUserCalledWithOnlineUser(self, mock_file):
        date = datetime.now()
        result = predict_user(date, 1, 0.5)
        self.assertEqual(result['willBeOnline'], True)
        self.assertEqual(result['onlineChance'], 1)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"userId": 1, "isOnline": false, "lastSeenDate": "2023-10-05T18:38:28", "onlinePeriods": [["2023-10-05T18:38:28", "2023-10-05T19:38:28"]]}]')
    def test_Should_ReturnOnlineChanceAndPrediction_When_PredictUserCalledWithOfflineUser(self, mock_file):
        date = datetime.now() + timedelta(hours=2)
        result = predict_user(date, 1, 0.5)
        self.assertEqual(result['willBeOnline'], False)
        self.assertEqual(result['onlineChance'], 0)

unittest.main()
