# -*- coding: utf-8 -*-


class Dummy(object):


    help="dummy command"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("-f","--foo",help="print the FOO twice",default="booo")
        subparser.add_argument("param",nargs="+")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        print self.ns
        for i in [1,2]:
            print self.ns.foo

        
        
