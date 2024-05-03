# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# embedded in python
import os
# pip install
import pandas as pd
# same folder

class Fonter( object ):
    
    """Helper class, provides access to one font in given folder."""
    
    columns_to_keep = [ 'path','text','x','y','p1x','p1y','p2x','p2y','p3x','p3y','p4x','p4y','w','h','nx','ny','nl','pl','lu']
    styles = {}
    
    def __init__( self,
                  *args, **kwargs ):
        super( Fonter, self ).__init__( *args, **kwargs )
        
    def _load_orientiers( self ):
        self.avg_w = self.df['w'].mean()
        self.avg_h = self.df['h'].mean()
    
    def _loadfont_df( self, fontdir ):
        """Reads data only from df.xls."""
        # get all df from used subfolders
        dfs = []
        for root, subs, files in os.walk( fontdir ):
            # look at flies in root folder
            for file in files:
                if not 'df.xls' in files: break
                df = pd.read_excel( os.path.join(root,'df.xls') )
                df['pathbc'] = df['path'] # filename backup
                df['path'] = [ os.path.join(root,f) for f in df['path'] ]
                df['pack'] = root
                dfs.append(df)
                break
            # look at files in subfolders
            for sub in subs:
                if not 'df.xls' in files: continue
                if sub=='unused': continue
                df = pd.read_excel( os.path.join(root,sub,'df.xls') )
                df['pathbc'] = df['path'] # filename backup
                df['path'] = [ os.path.join(root,sub,f) for f in df['path'] ]
                df['pack'] = os.path.join(root,sub)
                dfs.append(df)
            break
        df = pd.concat( dfs, axis=0, sort=False )
        
        return df
    
    def loadfont( self, style, fontdir ):
        """This function loads df.xls with specific font into self.df."""
        df = self._loadfont_df( fontdir )
        df['im'] = [ False for _ in range( len(df['path']) ) ]
        df['text'] = df['text'].astype( str )
        
        self.styles.setdefault( style, df )
        
    def selectfont( self, style ):
        self.df = self.styles[ style ]
        
        self._load_orientiers()
        
    def mark_loaded_chars( self, chars ):
        needed = self.df['path'].isin(chars)
        absent = self.df['im']==False
        self.df.loc[ needed & absent, 'im' ] = True
           
    def _savefont_df( self ):
        # split one df into subfolders
        roots = list( self.df['pack'].unique() )
        for counter, root in enumerate(roots):
            df = self.df[ self.df['pack']==root ].copy()
            df['path'] = df['pathbc']
            dest = os.path.join( root,'df.xls' )
            for col in self.columns_to_keep:
                if not col in df:
                    df[col] = pd.NA
            df.to_excel( dest, index=False, columns=self.columns_to_keep )
    
    def savefont( self ):
        for style in self.styles.keys():
            self.selectfont( style )
            self._savefont_df()
    
#---------------------------------------------------------------------------+++
# 2020
