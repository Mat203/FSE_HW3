import unittest
from unittest.mock import patch
from datetime import datetime, timedelta

import data_procession

class TestModuleIntegration(unittest.TestCase):
    @patch('data_procession.requests.get')
    def test_Should_UpdateData_When_UserStatusChanges(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {'data': [{'userId': '1', 'isOnline': True, 'lastSeenDate': '2023-10-06T08:35:30'}]}

        data_procession.fetch_and_update_data()

        self.assertEqual(len(data_procession.previous_state), 1)

        mock_response.json.return_value = {'data': [{'userId': '1', 'isOnline': False, 'lastSeenDate': '2023-10-06T08:35:30'}]}

        data_procession.fetch_and_update_data()

        self.assertFalse(data_procession.previous_state['1']['isOnline'])

    @patch('data_procession.requests.get')
    def test_Should_ReturnUsersOnline_When_GetDataCalledWithValidOffset(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {'data': [{'userId': '1', 'isOnline': True, 'lastSeenDate': '2023-10-06T08:35:30'}]}

        data_procession.fetch_and_update_data()

        self.assertEqual(len(data_procession.previous_state), 1)

        users_online = data_procession.get_users_online(datetime.now())
        self.assertEqual(users_online, 1)

    @patch('data_procession.requests.get')
    def test_Should_ReturnCorrectPrediction_When_PredictUserCalledWithValidData(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {'data': [{'userId': '1', 'isOnline': True, 'lastSeenDate': '2023-10-06T08:35:30'}]}

        data_procession.fetch_and_update_data()

        self.assertEqual(len(data_procession.previous_state), 1)

        user_prediction = data_procession.predict_user(datetime.now(), '1', 0.5)
        self.assertIsNotNone(user_prediction)
        self.assertIn('willBeOnline', user_prediction)
        self.assertIn('onlineChance', user_prediction)

    @patch('data_procession.requests.get')
    def test_Should_ReturnUsersOnlinePrediction_When_GetDataCalledWithValidOffset(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {'data': [{'userId': '1', 'isOnline': True, 'lastSeenDate': '2023-10-06T08:35:30'}]}

        data_procession.fetch_and_update_data()

        user_data = data_procession.get_user_data(datetime.now(), '1')
        self.assertTrue(user_data['wasUserOnline'])

        prediction = data_procession.predict_users(datetime.now())
        self.assertEqual(prediction['onlineUsers'], 1)


unittest.main()
