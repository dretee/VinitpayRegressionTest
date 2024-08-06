import configparser

configs = configparser.RawConfigParser()
configs.read(r"C:\Users\BAB AL SAFA\PycharmProjects\VnitpayRegressionTest\Configurations\config.ini")

class ReadProperties:

    @staticmethod
    def getTestPageURL():
        try:
            url = configs.get("common data", "TestHomeUrl")
            return url
        except configparser.NoSectionError:
            print("Error: 'common data' section not found in config.ini")
            return None
        except configparser.NoOptionError:
            print("Error: 'TestHomeUrl' option not found under 'common data' section in config.ini")
            return None

    @staticmethod
    def getProductionPageURL():
        try:
            url = configs.get("common data", "ProductionHomeURL")
            return url
        except configparser.NoSectionError:
            print("Error: 'common data' section not found in config.ini")
            return None
        except configparser.NoOptionError:
            print("Error: 'ProductionHomeURL' option not found under 'common data' section in config.ini")
            return None

    @staticmethod
    def getUserDetails():
        try:
            UserEmail = configs.get("common data", "EXISTING_Test_EMAIL")
            UserPassword = configs.get("common data", "EXISTING_Test_PASSWORD")
            return UserEmail, UserPassword
        except configparser.NoSectionError:
            print("Error: 'common data' section not found in config.ini")
            return None, None
        except configparser.NoOptionError:
            print("Error: 'EXISTING_Test_EMAIL' or 'EXISTING_Test_PASSWORD' option not found"
                  " under 'common data' section in config.ini")
            return None, None
