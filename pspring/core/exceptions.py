class PayloadException(Exception):
    def __init__(self,*args):
        super().__init__(*args)
        self.response = args[2]
        self.statusCode = args[1]
