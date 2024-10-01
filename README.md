# 🌈R6 Siege Log Processor - Nic H.
_Analyzing millions of R6 Siege matches so you don’t have to!_ 🕵️‍♀️

## Intro
Welcome to the **R6 Siege Log Processor**! 👋

Ever wondered who the deadliest operators in R6 Siege are? Or perhaps you want to find out which players are topping the kill charts? With millions of matches every day, that’s a tough job—but don't worry, we’ve got you covered!

Sounds cool? Let’s dive in! 🏊‍♂️

### How it Works:
- Compute the **top 100 operators** based on the **average number of kills** per match over the last 7 days.
- Compute the **top 10 players** based on the **total number of kills** per match over the last 7 days.

Two reports are generated daily:
- `operator_top100_yyyymmdd.txt`: Contains the top 100 operators based on average kills.
- `player_top10_yyyymmdd.txt`: Contains the top 10 players based on total kills.

And guess what? It does all this every day, because operators and players need their daily dose of fame! 😎

### Main Features
- **Daily Reports**: Generates operator and player reports based on the last N days of matches.
- **Configurable**: Parameters like the number of top operators, players, log file path, and report path are configurable via a JSON config file.
- **Linux-friendly**: Can be scheduled with cron or other task schedulers for automated execution.

## 🗂Project Structure
```bash
r6-siege-log-processor/
├── config/
│   └── config.json                 # Configuration file (paths, number of days, etc.)
├── lib/
│   └── r6LogsProcessor.py          # Core log processing logic
├── main.py                         # Entry point for the program
├── README.md                       # Project documentation
├── requirements.txt                # Project dependencies
├── resources/
│   ├── r6_logs/                    # Folder containing log files
│   ├── reports/                    # Folder where generated reports are stored
├── ref_resources/
│   ├── r6_logs/                    # Log files for reference
│   ├── reports/                    # Report files for reference
├── tests/
│   ├── config/
│   ├── resources/
│   └── test_r6LogsProcessor.py     # Unit tests for the log processor
```

## Getting Started
### Prerequisites
- Python 3.10.11
- pip
### Setup
Clone the repository:

```bash
git clone <repository_url>
cd Ubisoft-Data-Processing-Assessment
```

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```
Ensure the `config/config.json` file is properly set up with the appropriate paths for log files, report files, and any other configuration parameters.

### Configuration
The `config.json` file contains key configuration settings for the log processing system:

```json
{
    "N_DAYS": 7,
    "TOP_N_OPERATOR_KILLS": 100,
    "TOP_N_PLAYERS": 10,
    "LOGS_FOLDER": "./resources/r6_logs",
    "REPORT_FOLDER": "./resources/reports"
}
```

- `N_DAYS`: Number of past days to include in the processing (default: 7).
- `TOP_N_OPERATOR_KILLS`: Number of top operators based on average kills to report (default: 100).
- `TOP_N_PLAYERS`: Number of top players based on total kills to report (default: 10).
- `LOGS_FOLDER`: Directory containing the log files.
- `REPORT_FOLDER`: Directory where reports will be generated.

## Running the Project
### Manually
The project can be executed from the terminal using:

```bash
python main.py
```
The script will process the log files from the last `N_DAYS` (as specified in `config.json`), and generate the two report files: `operator_top100_yyyymmdd.txt` and `player_top10_yyyymmdd.txt`.

### Scheduling with Cron
Because who’s up at 2 AM to manually run scripts, right? 😴

To automate the execution, schedule the script using a `cron` job on Linux. For example, to run the script daily at midnight, add the following line to crontab:

```bash
0 0 * * * cd /path_to_project/ && /usr/bin/python3 main.py >> path/to/logs/r6LogProcessor_execution_log_$(date +\%Y\%m\%d).log 2>&1
```
## Testing
Feeling skeptical? We got you covered! Unit tests are provided to ensure the correct functionality of the log processing system. The tests are located in the `tests/` folder.

To run the tests:

```bash
python -m pytest tests/
```
### Reference Resources
- **Log Files**: The folder `ref_resources/r6_logs/` contains log files for reference.
- **Generated Reports**: Expected reports are provided in the `ref_resources/reports/` folder.
## Future Improvements
- **Automated Trigger**: Implement a file watcher (e.g., using `inotify` or similar) to automatically trigger the script when new log files are added.
- **Performance Optimization**: Add parallel processing to handle large log volumes faster and cache processed logs for each day, then reuse them for the rolling N-days window.
