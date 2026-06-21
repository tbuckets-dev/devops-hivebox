import unittest
from unittest.mock import patch, MagicMock
import app

class TestHiveboxApp(unittest.TestCase):
    
    @patch('app.get_temperature_boxes')
    def test_get_average_temperature_no_boxes(self, mock_get_boxes):
        mock_get_boxes.return_value = []
        avg, error = app.get_average_temperature_from_boxes()
        self.assertIsNone(avg)
        self.assertEqual(error, "No temperature boxes found")

    @patch('app.get_temperature_boxes')
    def test_get_average_temperature_success(self, mock_get_boxes):
        # Mock 3 valid boxes
        mock_boxes = [
            {'sensors': [{'title': 'temp', 'lastMeasurement': {'value': '20.0'}}]},
            {'sensors': [{'title': 'temp', 'lastMeasurement': {'value': '22.0'}}]},
            {'sensors': [{'title': 'temp', 'lastMeasurement': {'value': '24.0'}}]}
        ]
        mock_get_boxes.return_value = mock_boxes
        
        avg, error = app.get_average_temperature_from_boxes(num_boxes=3)
        self.assertIsNone(error)
        self.assertAlmostEqual(avg, 22.0)

    def test_get_latest_temperature_valid(self):
        box = {'sensors': [{'title': 'DHT11 temp', 'lastMeasurement': {'value': '25.5'}}]}
        temp = app.get_latest_temperature(box)
        self.assertEqual(temp, 25.5)

    def test_get_latest_temperature_invalid(self):
        box = {'sensors': [{'title': 'DHT11 temp', 'lastMeasurement': {'value': 'invalid'}}]}
        temp = app.get_latest_temperature(box)
        self.assertIsNone(temp)

if __name__ == '__main__':
    unittest.main()
