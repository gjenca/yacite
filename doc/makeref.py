import os
import yacite.command
from yacite.utils.misc import Argument,MexGroup
from jinja2 import Template,FileSystemLoader,Environment
import sys

def collect_args(args):

    posargs=[]
    optargs=[]
    for arg in args:
        if type(arg) is Argument:
            if arg.args[0][0]=="-":
                optargs.append(arg)
            else:
                posargs.append(arg)
        elif type(arg) is MexGroup:
            pos_grp,opt_grp=collect_args(arg.arguments)
            posargs.extend(pos_grp)
            optargs.extend(opt_grp)
    return posargs,optargs 

env=Environment(loader=FileSystemLoader("templates"))
t=env.get_template("usage.md")
for mod_name in dir(yacite.command):
    mod=yacite.command.__dict__[mod_name]
    if type(mod).__name__=='module': 
        for sname in dir(mod):
            if sname=='YaciteCommand':
                continue
            obj=mod.__dict__[sname]
            if type(obj) is type and \
                issubclass(obj,yacite.command.command.YaciteCommand):
                posargs,optargs=collect_args(obj.arguments)
                usage_lines=[]
                for line in os.popen("yacite %s -h" % obj.name):
                    if not line.strip():
                        break
                    usage_lines.append(line)
                usage="".join(usage_lines)
                usage=usage.replace("usage:","**USAGE:** `")
                usage=usage+'`'
                sys.stdout.write(t.render(help=obj.__doc__,name=obj.name,posargs=posargs,optargs=optargs,usage=usage).encode('utf-8'))
