# -*- coding: utf-8 -*-
import yaml

def construct_yaml_str(self, node):
    return self.construct_scalar(node)

# Override the default string handling function 
# to always return unicode objects
yaml.Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)

def docstream(f):
    return yaml.load_all(f)


