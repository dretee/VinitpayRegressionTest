import logging
import os

class RecordLogger:
    @staticmethod
    def log_generator_info():
        """
        Configures and returns a logger instance for logging informational messages.
        """
        log_dir = os.path.join(os.getcwd(), "Logs")  # Dynamically get Logs directory path
        log_file = os.path.join(log_dir, "Records.log")

        # Ensure Logs directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,  # Set log level directly
            format="%(asctime)s: %(levelname)s: %(message)s",
            datefmt="%d/%m/%Y %I:%M:%S %p"
        )

        # Return a named logger
        return logging.getLogger(__name__)

