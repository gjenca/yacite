# -*- coding: utf-8 -*-


def keys_to_cmp(sort_keys):

    sgn_fieldnames=[]
    for k in sort_keys:
        if k[0]=="~":
            sgn_fieldnames.append((-1,k[1:]))
        else:
            sgn_fieldnames.append((1,k))
    
    def cmp_keys(d1,d2):
        
        for sgn,fieldname in sgn_fieldnames:
            c=cmp(d1[fieldname],d2[fieldname])*sgn
            if c:
                return c
        return 0
    
    return cmp_keys

