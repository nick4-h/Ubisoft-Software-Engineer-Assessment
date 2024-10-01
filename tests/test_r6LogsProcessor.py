import unittest
import os
from datetime import datetime, timedelta
import glob
from lib.r6LogsProcessor import PlayerLogProcessor, OperatorLogProcessor, process_logs, load_config

class TestProcessR6Logs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load test configuration
        cls.config = load_config('./tests/config/config.json')
        cls.operator_processor = OperatorLogProcessor(cls.config)
        cls.player_processor = PlayerLogProcessor(cls.config)

        # Create mock log data for testing
        cls.mock_log_data = [
            "player1,match1,operator1,5",
            "player2,match1,operator1,3",
            "player1,match2,operator2,2",
            "player2,match2,operator1,4",
            "player1,match3,operator2,1",
        ]

        # Setup mock log files
        cls.setup_mock_log_files()

    @classmethod
    def setup_mock_log_files(cls):
        # Create mock log files for the last N days as defined in the test configuration
        today = datetime.today()
        for i in range(cls.config['N_DAYS']):
            day = (today - timedelta(days=i)).strftime('%Y%m%d')
            log_file_path = os.path.join(cls.config['LOGS_FOLDER'], f'r6-matches-{day}.log')
            with open(log_file_path, 'w') as file:
                file.write('\n'.join(cls.mock_log_data))

    def test_player_report_content(self):
        """Test the generated player report content."""
        process_logs([self.player_processor])

        # Define expected player report content
        today = datetime.today().strftime('%Y%m%d')
        expected_report_content = "player1|match1:35,match2:14,match3:7\nplayer2|match2:28,match1:21\n"
        
        # Verify the generated player report
        report_file_path = os.path.join(self.config['REPORT_FOLDER'], f'player_top{self.config["TOP_N_PLAYERS"]}_{today}.txt')
        with open(report_file_path, 'r') as report_file:
            actual_report_content = report_file.read()
        
        self.assertEqual(actual_report_content, expected_report_content, f"Player report content mismatch: {actual_report_content}")

    def test_operator_report_content(self):
        """Test the generated operator report content."""
        process_logs([self.operator_processor])

        # Define expected operator report content
        today = datetime.today().strftime('%Y%m%d')
        expected_report_content = "operator1|match1:4.00,match2:4.00\noperator2|match2:2.00,match3:1.00"
        
        # Verify the generated operator report
        report_file_path = os.path.join(self.config['REPORT_FOLDER'], f'operator_top{self.config["TOP_N_OPERATOR_KILLS"]}_{today}.txt')
        with open(report_file_path, 'r') as report_file:
            actual_report_content = report_file.read()

        self.assertEqual(actual_report_content, expected_report_content, f"Operator report content mismatch: {actual_report_content}")

    @classmethod
    def tearDownClass(cls):
        # Clean up by removing any files created during the tests
        folders = [cls.config['LOGS_FOLDER'], cls.config['REPORT_FOLDER']]
        
        for folder in folders:
            if os.path.exists(folder):
                files = glob.glob(os.path.join(folder, '*'))
                for file_path in files:
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        print(f"Error removing file {file_path}: {e}")

if __name__ == "__main__":
    unittest.main()
