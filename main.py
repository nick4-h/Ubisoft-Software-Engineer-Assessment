from lib.r6LogsProcessor import OperatorLogProcessor, PlayerLogProcessor, process_logs, load_config

def main():
    # Load configuration
    config = load_config()

    # Instantiate the processors
    operator_processor = OperatorLogProcessor(config)
    player_processor = PlayerLogProcessor(config)

    # Pass the processors to the log processing function
    process_logs([operator_processor, player_processor])

if __name__ == "__main__":
    main()
