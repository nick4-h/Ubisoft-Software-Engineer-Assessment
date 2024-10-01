import json
import os
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any


def load_config(config_file: str = r'.\config\config.json') -> Dict[str, Any]:
    """
    Load the JSON configuration file.

    Args:
        config_file (str): JSON configuration file path. Defaults to './config/config.json'.

    Returns:
        Dict[str, Any]: Configuration dictionary.
    """
    with open(config_file, 'r') as file:
        return json.load(file)


config = load_config()


class LogProcessor(ABC):
    """
    Abstract base class for log processors.
    """

    def __init__(self):
        """
        Initialize the log processor.
        """
        self.data = defaultdict(lambda: defaultdict(int))

    @abstractmethod
    def process_log_line(self, line: str) -> None:
        """
        Abstract method to process a single log line.

        Args:
            line (str): A line from the log file to be processed.
        """
        pass

    @property
    def summary(self) -> Dict[str, Dict[str, Any]]:
        """
        Property that returns the processed data summary.

        Returns:
            Dict[str, Dict[str, Any]]: Summary of processed log data.
        """
        return self.data

    @abstractmethod
    def generate_report(self, date: str) -> None:
        """
        Abstract method to generate a report based on the processed data.

        Args:
            date (str): The date string used in the report file naming.
        """
        pass


class OperatorLogProcessor(LogProcessor):
    """
    Class for processing operator log data.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the operator log processor with a configuration.

        Args:
            config (Dict[str, Any]): Configuration dictionary.
        """
        super().__init__()
        self.config = config
        self.data = defaultdict(lambda: defaultdict(lambda: {'kills': 0, 'matches': 0}))

    def process_log_line(self, line: str) -> None:
        """
        Process a single log line and update operator kill statistics.

        Args:
            line (str): A line from the log file.
        """
        player_id, match_id, operator_id, nb_kills = line.strip().split(',')
        self.data[operator_id][match_id]['kills'] += int(nb_kills)
        self.data[operator_id][match_id]['matches'] += 1

    def generate_report(self, date: str) -> None:
        """
        Generate a report of top operators based on kills per match.

        Args:
            date (str): The date string used in the report file naming.
        """
        report_lines = []
        for operator_id, match_data in self.data.items():
            sorted_matches = sorted(
                match_data.items(), 
                key=lambda x: (-x[1]['kills'] / x[1]['matches'], x[0])
            )[:self.config['TOP_N_OPERATOR_KILLS']]
            
            match_report = ",".join(
                f"{match_id}:{data['kills'] / data['matches']:.2f}" 
                for match_id, data in sorted_matches
            )
            report_lines.append(f"{operator_id}|{match_report}")
        
        report_path = os.path.join(
            self.config['REPORT_FOLDER'], 
            f'operator_top{self.config["TOP_N_OPERATOR_KILLS"]}_{date}.txt'
        )
        with open(report_path, 'w') as file:
            file.write('\n'.join(report_lines))


class PlayerLogProcessor(LogProcessor):
    """
    Class for processing player log data.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the player log processor.

        Args:
            config (Dict[str, Any]): Configuration dictionary.
        """
        super().__init__()
        self.config = config

    def process_log_line(self, line: str) -> None:
        """
        Process a single log line and update player kill statistics.

        Args:
            line (str): A line from the log file.
        """
        player_id, match_id, operator_id, nb_kills = line.strip().split(',')
        self.data[player_id][match_id] += int(nb_kills)

    def generate_report(self, date: str) -> None:
        """
        Generate a report of top players based on total kills per match.

        Args:
            date (str): The date string used in the report file naming.
        """
        player_top_n = []
        for player_id, match_kills in self.data.items():
            sorted_matches = sorted(
                match_kills.items(), 
                key=lambda x: (-x[1], x[0])
            )[:self.config['TOP_N_PLAYERS']]
            
            report_string = f"{player_id}|" + ",".join(
                f"{match_id}:{nb_kills}" 
                for match_id, nb_kills in sorted_matches
            )
            player_top_n.append(report_string)

        report_path = os.path.join(
            self.config['REPORT_FOLDER'], 
            f'player_top{self.config["TOP_N_PLAYERS"]}_{date}.txt'
        )
        with open(report_path, 'w') as file:
            file.write("\n".join(player_top_n) + "\n")


def process_logs(processors: List[LogProcessor]) -> None:
    """
    Process logs.

    Args:
        processors (List[LogProcessor]): List of log processors.
    """
    today = datetime.today().strftime('%Y%m%d')
    log_files = get_last_n_days_log_files(processors[0].config)

    # Process daily logs for each processor
    for processor in processors:
        for log_file in log_files:
            with open(log_file, 'r') as file:
                for idx, line in enumerate(file):
                    try:
                        processor.process_log_line(line)
                    except Exception as e:
                        print(f"Error processing log line ({idx}) in file {log_file}: {e}")
        processor.summary

        # Generate reports for each processor
        processor.generate_report(today)


def get_last_n_days_log_files(config: Dict[str, Any]) -> List[str]:
    """
    Retrieve log file paths for the last N days.

    Args:
        config (Dict[str, Any]): Configuration dict.

    Returns:
        List[str]: List of log file paths from the last N days.

    Raises:
        FileNotFoundError: If no log files are found for the last N days.
    """
    today = datetime.today()
    log_files = []
    
    for i in range(config['N_DAYS']):
        day = (today - timedelta(days=i)).strftime('%Y%m%d')
        log_file = os.path.join(config['LOGS_FOLDER'], f'r6-matches-{day}.log')
        if os.path.exists(log_file):
            log_files.append(log_file)
        else:
            print(f"Log file for {day} not found.")
    
    if not log_files:
        raise FileNotFoundError(f"No log files found for the last {config['N_DAYS']} days.")
    
    return log_files
