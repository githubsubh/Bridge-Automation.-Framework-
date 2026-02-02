import logging
import inspect
import os

class LogGen:
    @staticmethod
    def loggen():
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        
        # Check if handler already exists to avoid duplicate logs
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # Create logs directory if it doesn't exist
            if not os.path.exists("./logs"):
                os.makedirs("./logs")
                
            fileHandler = logging.FileHandler("logs/automation.log")
            formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
            
        return logger
