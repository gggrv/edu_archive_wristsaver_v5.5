# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

def chop( text, L, R, mode='abs' ):
    """Chops text in primitive way."""
    A, B = 0, len(text) # iloc, will change
    
    # if L exists
    if type(L)==int: A = L
    elif type(L)==str: A = text.find(L)+len(L)
    text = text[A:]
    
    # if R exists
    if type(R)==int: B = R
    elif type(R)==str:
        B = text.find(R)
        if B==-1: B=len(text)
    
    return text[:B].strip()

def xxx( i, total, text, w=10, ok='+', no='x' ):
    """
    Prints a progress bar in the console. How to use:
    paste into some cycle.
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    per100 = i/total
    nfilled = int( w*per100 )
    info, bar = chop(str(100*per100),None,'.'), ok*nfilled+no*(w-nfilled)
    line = ( '\r%s %s %s' ) % ( text, bar, info+'%' )
    print( line, end='\r' )
    if i==total: print()

def readf( path, mode='r' ):
    with open( path, mode, encoding='utf-8' ) as f:
        return f.read()

#---------------------------------------------------------------------------+++
# 2018, 2020
