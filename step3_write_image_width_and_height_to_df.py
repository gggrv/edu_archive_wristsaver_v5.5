# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# embedded in python
import os
# pip install
import pandas as pd
import PIL
from PIL import Image
# same folder
        
def v1( root ):
    oldf = os.path.join(root,'df.xls')
    df = pd.read_excel( oldf )
    os.rename( oldf, oldf+' bc changed4' )
    
    """This function reads each individual image in root folder and writes
    its dims into corresponding df."""
    
    #"""
    ws, hs = [], []
    for path in df['path']:
        imread = PIL.Image.open( os.path.join(root,path) )
        
        # for df
        ws.append( imread.size[0] )
        hs.append( imread.size[1] )
    df['w'] = ws # width
    df['h'] = hs # height
    #"""
    
    #df['nx'], df['ny'] = df['nextx'], df['nexty']
    #df = df.drop( columns=['L','R','nextx','nexty'] )
    
    #df['nl'] = df['nextl']
    #df = df.drop( columns=['nextl'] )
    
    """
    pois = ['p1x','p1y','p2x','p2y','p3x','p3y','p4x','p4y']
    for poi in pois:
        mask = df[poi].isna()
        df.loc[ mask, poi ] = 0
    """
    
    #df['lu'] = [ 0 for i in range( len(df['path']) ) ] # last used
    
    df.to_excel( os.path.join( root, 'df.xls' ), index=False )

def autorun():
    
    this_folder = os.path.dirname(__file__)
    folder_with_letter_images = os.path.join(this_folder,'fonts','step3kaggle_write_image_width_and_height_to_df')
    for root, subs, fs in os.walk(folder_with_letter_images):
        v1( root )
    
    print( 'Done!' )

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# 2019, 2020
