import logging
import inspect
import os
import time
import atexit

class LogGen:
    _logger = None
    _log_file_path = None

    @staticmethod
    def loggen():
        if LogGen._logger is not None:
            return LogGen._logger

        logger_name = "AutomationLogger"
        logger = logging.getLogger(logger_name)
        
        # Check if handler already exists to avoid duplicate logs
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # Create logs directory if it doesn't exist
            if not os.path.exists("./logs"):
                os.makedirs("./logs")
                
            # 1. Timestamped Log File
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            LogGen._log_file_path = f"logs/automation_{timestamp}.log"
            fileHandler = logging.FileHandler(LogGen._log_file_path)
            formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

            # 2. Console Handler (StreamHandler)
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(formatter)
            logger.addHandler(consoleHandler)

            # Register cleanup to generate reverse log
            atexit.register(LogGen.generate_reverse_log)

        LogGen._logger = logger
        return logger

    @staticmethod
    def generate_reverse_log():
        """Generates a log file with latest entries at the top."""
        if not LogGen._log_file_path or not os.path.exists(LogGen._log_file_path):
            return
            
        try:
            with open(LogGen._log_file_path, 'r') as f:
                lines = f.readlines()
            
            reverse_path = LogGen._log_file_path.replace(".log", "_reversed.log")
            with open(reverse_path, 'w') as f:
                f.writelines(reversed(lines))
                
            # Optional: Also create a generic 'latest_reversed.log' for easy access
            with open("logs/latest_reversed.log", 'w') as f:
                f.writelines(reversed(lines))
                
        except Exception as e:
            print(f"Failed to generate reverse log: {e}")

