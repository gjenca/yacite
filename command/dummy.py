

class Dummy(object):


    help="dummy command"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("-f","--foo",help="print the FOO twice",default="booo")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        for i in [1,2]:
            print self.ns.foo

        
        
