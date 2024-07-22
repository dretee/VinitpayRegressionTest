import logging

class RecordLogger:
    """
    A utility class for configuring and generating loggers.
    """

    @staticmethod
    def log_generator_info():
        """
        Configures and returns a logger instance for logging informational messages.
        """
        logging.basicConfig(
            filename="C:\\Users\\BAB AL SAFA\\PycharmProjects\\VnitpayAutomation\\Logs\\Records.log",
            format="%(asctime)s: %(levelname)s: %(message)s",
            datefmt="%d/%m/%Y %I:%M:%S %p"
        )

        # Create a logger object
        logger = logging.getLogger()

        # Set the log level to INFO
        logger.setLevel(logging.INFO)

        return logger

