import colorama

class Logger:
    @staticmethod
    def init_logger():
        colorama.init(autoreset=True)

    @staticmethod
    def logerr(msg):
        print(colorama.Fore.RED + "ERROR : " + msg )

    @staticmethod
    def logwarn(msg):
        print(colorama.Fore.YELLOW + "WARN : " + msg)

    @staticmethod
    def log(msg):
        print(colorama.Fore.GREEN + "LOG : " + msg)