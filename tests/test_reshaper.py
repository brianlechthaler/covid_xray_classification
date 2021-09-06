import unittest
from covid_xray_classification.data import Reshaper
from pandas import DataFrame
from subprocess import run
from os.path import isfile


class ReshaperTestCase(unittest.TestCase):
    def test_something(self):
        run(['touch', '1'])
        run(['touch', '2'])

        df = DataFrame({'filename': ['1', '2'],
                        'classification': ['one', 'two']})

        reshape_task = Reshaper(df, input_folder='./', output_folder='test_data')

        reshape_task.reshape()

        self.assertEqual(
            isfile('./test_data/one/1'),
            True
        )

        run(['rm', '-rf', 'test_data'])

if __name__ == '__main__':
    unittest.main()
