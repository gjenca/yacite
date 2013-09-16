import yacite.command
from yacite.utils.misc import Argument

for mod_name in dir(yacite.command):
    mod=yacite.command.__dict__[mod_name]
    if type(mod).__name__=='module': 
        for sname in dir(mod):
            if sname=='YaciteCommand':
                continue
            obj=mod.__dict__[sname]
            if type(obj) is type and issubclass(obj,yacite.command.command.YaciteCommand):
                print sname
                print obj.__doc__
                for arg in obj.arguments:
                    if type(arg) is Argument:
                        print arg.args, arg.kwargs['help']
                        
