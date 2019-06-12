# -*- coding: utf-8 -*-
import yaml

def construct_yaml_str(self, node):
    return self.construct_scalar(node)

# Override the default string handling function 
# to always return unicode objects
yaml.Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)

def unicode_representer(dumper, uni):
    node = yaml.ScalarNode(tag=u'tag:yaml.org,2002:str', value=uni)
    return node

# This is necessary to dump ASCII string normally
yaml.add_representer(unicode, unicode_representer)

def load_all(f,**kwargs):
    for d in yaml.safe_load_all(f,**kwargs):
        for key in d:
            if type(d[key]) is unicode:
                try:
                    d[key]=int(d[key])
                except ValueError:
                    pass
        yield d

yaml_load=yaml.load

def dump(obj,**kwargs):
    return yaml.dump(obj,encoding="utf-8",allow_unicode=True,**kwargs)

def load(f,**kwargs):
    return yaml.safe_load(f,**kwargs)

