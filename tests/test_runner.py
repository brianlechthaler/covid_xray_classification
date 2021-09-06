import unittest
from covid_xray_classsification.cmd import Runner

class RunnerTestCase(unittest.TestCase):
    def test_successful_exit_code(self):
        echo_test_cmd = Runner(['echo', 'test'])
        echo_test_cmd.run()
        self.assertEqual(echo_test_cmd.result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
