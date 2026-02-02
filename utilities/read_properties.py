import configparser

config = configparser.RawConfigParser()
config.read("./config/config.ini")

class ReadConfig:
    @staticmethod
    def getApplicationURL():
        url = config.get('common info', 'baseURL')
        return url

    @staticmethod
    def getBrowser():
        browser = config.get('common info', 'browser')
        return browser
    
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
