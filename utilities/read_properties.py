import configparser
import os

config = configparser.RawConfigParser()
config.read("./config/config.ini")

class ReadConfig:
    @staticmethod
    def getApplicationURL():
        return config.get('common info', 'base_url')

    @staticmethod
    def getBrowser():
        return config.get('common info', 'browser')
    
    @staticmethod
    def getImplicitWait():
        try:
            return int(config.get('common info', 'implicit_wait'))
        except:
            return 10
            
    @staticmethod
    def getExplicitWait():
        try:
            return int(config.get('common info', 'explicit_wait'))
        except:
            return 20

    @staticmethod
    def getLoginURL():
        return config.get('login', 'url')

    @staticmethod
    def getLoginEmail():
        return config.get('login', 'email')

    @staticmethod
    def getLoginPassword():
        return config.get('login', 'password')

    @staticmethod
    def getPaymentConfig():
        return {
            "gateway": config.get('payment', 'gateway_name'),
            "mode": config.get('payment', 'mode'),
            "card_number": config.get('payment', 'card_number'),
            "card_holder": config.get('payment', 'card_holder'),
            "card_expiry": config.get('payment', 'card_expiry'),
            "card_cvv": config.get('payment', 'card_cvv')
        }

    @staticmethod
    def getPaths():
        return {
            "test_data_dir": config.get('paths', 'test_data_dir'),
            "email_counter": config.get('paths', 'email_counter_file'),
            "dummy_jpg": config.get('paths', 'dummy_jpg'),
            "dummy_pdf": config.get('paths', 'dummy_pdf')
        }

    @staticmethod
    def getTimeouts():
        return {
            "stabilization": int(config.get('timeouts', 'stabilization_wait')),
            "page_load": int(config.get('timeouts', 'page_load_wait')),
            "otp_wait": int(config.get('timeouts', 'otp_wait')),
            "gateway_wait": int(config.get('timeouts', 'gateway_wait'))
        }
