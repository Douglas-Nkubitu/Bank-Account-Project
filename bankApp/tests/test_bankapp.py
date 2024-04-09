import unittest
from ..bankapp import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()      

    def test_get_balance(self):
        response = self.app.get('/balance')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('balance', data)

    def test_deposit_correct_amount(self):
        response = self.app.post('/deposit', json={'amount': 10000})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Deposit successful')

    def test_exceed_max_per_transaction(self):
        response = self.app.post('/deposit', json={'amount': 41000})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Exceeded Maximum Deposit Per Transaction')

    def test_deposit_wrong_value(self):
        response = self.app.post('/deposit', json={'amount': -500})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid amount')

    def test_exceed_deposit_frequency_tries(self):
        for x in range(5):
            response = self.app.post('/deposit', json={'amount': 10000})

            if x == 4:
                self.assertEqual(response.status_code, 400)
                data = response.get_json()
                self.assertIn('error', data)
                self.assertEqual(data['error'], 'Exceeded Maximum Deposit Frequency Per Day')

    def test_exceed_deposit_per_day(self):
        for x in range(5):
            response = self.app.post('/deposit', json={'amount': 40000})

            if x == 4:
                self.assertEqual(response.status_code, 400)
                data = response.get_json()
                self.assertIn('error', data)
                self.assertEqual(data['error'], 'Exceeded Maximum Deposit Per Day')

    def test_withdrawal(self):
        response = self.app.post('/withdrawal', json={'amount': 5000})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Withdrawal successful')

if __name__ == '__main__':
    unittest.main()