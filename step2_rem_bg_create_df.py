# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# embedded in python
import os
# pip install
import pandas as pd
import PIL
from PIL import Image
# same folder
        
def clean_pics( fs ):
    for file in fs:
        if file[-4:]!='.png': continue
        imread = PIL.Image.open( file )
        if imread.mode=='RGB': imread=imread.convert('RGBA')
        newdata = []
        for pixel in imread.getdata():
            alpha = int( 255-pd.np.max(pixel[:3]) )
            newdata.append( (pixel[0],pixel[1],pixel[2],alpha) )
        imread.putdata( newdata )
        imread.save( os.path.join('..',file) )
        
def v1( fs ):
    """
    Removes backgrounds from the images and creates empty df.xls.
    """
    
    paths = []
    ws, hs = [], []
    for f in fs:
        imread = PIL.Image.open( f )
        if imread.mode=='RGB': imread=imread.convert('RGBA')
        
        oldata = imread.getdata()
        newdata = []
        for pixel in oldata:
            R,G,B = 12,12,12 # pen color, thicker = darker
            alpha = 255 - pixel[0]
            alpha += 0.1*alpha # enlarge 10%
            if alpha>255: alpha = 255
            alpha = int(alpha)
            # forgot
            #R,G,B = pixel[0],pixel[1],pixel[2]
            #alpha = pixel[3]*4
            newdata.append( (R,G,B,alpha) )
            imread.putdata( newdata )
        name = os.path.split( f )[-1]
        path = f#os.path.join(dest,name)
        imread.save( path )
        
        # for df
        name = os.path.split( f )[-1]
        paths.append( name )
        ws.append( imread.size[0] )
        hs.append( imread.size[1] )
            
    df = pd.DataFrame()
    total = len(fs)
    if total>0:
        df['path'] = paths
        df['x'] = [ 0 for i in range( total ) ]
        df['y'] = [ 0 for i in range( total ) ]
        df['nx'] = [ 0 for i in range( total ) ] # next x
        df['ny'] = [ 0 for i in range( total ) ] # next y
        df['w'] = ws # width
        df['h'] = hs # height
        df['lu'] = [ 0 for i in range( total ) ] # last used
        df.to_excel( 'df.xls', index=False )

def autorun():
    
    this_folder = os.path.dirname(__file__)
    folder_with_letter_images = os.path.join(this_folder,'fonts','step2kaggle_rem_bg_create_df')
    for root, subs, fs in os.walk(folder_with_letter_images):
        os.chdir(root)
        v1(fs)
    print( 'Done!' )

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# 2019, 2020
