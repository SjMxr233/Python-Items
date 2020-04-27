
class Utils:
    @staticmethod
    def LoadQss(style):
        with open(style,'r') as p:
            return p.read()
