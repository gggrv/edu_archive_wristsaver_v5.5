# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# embedded in python
from time import sleep
import os
# pip install
import bs4#
import pandas as pd
import PIL
from PIL import Image
# same folder
import Fonter
from txd import chop

class Printer( object ):
    
    maxlu = 500 # printer's max last use
    page_counter = 0 # how many pages
    C = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    A = list( """., _+-=():;!?"'/%""" )
    
    def __init__( self,
                  font,
                  *args, **kwargs ):
        super( Printer, self ).__init__( *args, **kwargs )
        
        self.fo = font
    
    def _hasnopool( self, pool ):
        if len(pool)==0: return self.fo.df[ self.fo.df['text']=='absent' ]
        return pool
            
    @staticmethod
    def _hastailL( pool, has ):
        if len(pool)==0: return pool
        
        dx = pool['p1x']-pool['p2x']
        dy = pool['p1y']-pool['p2y']
        if has: return pool[ (dx*dx + dy*dy)>=10 ]
        return pool[ (dx*dx + dy*dy)<10 ]
    
    @staticmethod
    def _hastailR( pool, has ):
        if len(pool)==0: return pool
        
        dx = pool['p3x']-pool['p4x']
        dy = pool['p3y']-pool['p4y']
        if has: return pool[ (dx*dx + dy*dy)>=10 ]
        return pool[ (dx*dx + dy*dy)<10 ]
    
    def _hasprev( self, pool, pl, has ):
        if len(pool)==0: return pool
        
        candidates = pool[ pool['pl'].notna() ] if 'pl' in pool.columns else []
        if len(candidates)==0: return pool
        
        ok = []
        for loc, row in candidates.iterrows():
            pls = row['pl'].split("''")
            if pl in pls: ok.append( row )
        
        if len(ok)>0 and has: return pd.DataFrame( ok )
        # candidates exist, but none is sitable
        if len(ok)==0: return pool[ pool['pl'].isna() ]
        no = ~( pool['path'].isin(ok['path']) )
        return pool[ no & ( pool['pl'].isna() ) ]
    
    def _hasnext( self, pool, nl, has ):
        if len(pool)==0: return pool
        
        candidates = pool[ pool['nl'].notna() ]
        if len(candidates)==0: return pool
        
        ok = []
        for loc, row in candidates.iterrows():
            nls = row['nl'].split("''")
            if nl in nls: ok.append( row )
        
        if len(ok)>0 and has: return pd.DataFrame( ok )
        # candidates exist, but none is sitable
        if len(ok)==0: return pool[ pool['nl'].isna() ]
        no = ~( pool['path'].isin(ok['path']) )
        return pool[ no & ( pool['nl'].isna() ) ]
    
    def _hasminlu( self, pool, iloc ):
        pool = pool[ pool['lu']==pool['lu'].min() ] # minimum last use
        sample = pool.sample().iloc[0] # choose 1 line
        
        # ++/-- last use for selected row
        mask = self.fo.df['path']==sample['path']
        value = self.fo.df[mask]['lu'].iloc[0]
        if value>=self.maxlu: self.fo.df.loc[mask,'lu']=0 # reset
        else: self.fo.df.loc[mask,'lu']=self.fo.df[mask]['lu'].iloc[0]+1
        
        return dict(sample) # this is faster
            
    def choose_chars( self, text ):
        """Selects some letters from the font."""
        choices = []
        tl = len( text )-1
        for iloc, l in enumerate( text ):
            pool = self.fo.df[ self.fo.df['text']==l ]
            # first letter of the word?
            if iloc==0: pool=self._hastailL(pool,False)
            # which letter was before it?
            else: pool = self._hasprev( pool, text[iloc-1], True )
            
            # last letter of the word?
            if iloc==tl: pool=self._hastailR(pool,False)
            # which letter will be next?
            else: pool = self._hasnext( pool, text[iloc+1], True )
            
            pool = self._hasnopool(pool) # what to choose?
            choice = self._hasminlu( pool, iloc )
            choices.append( choice['path'] ) # done
            
        return choices
        
    def _get_css( self, head, root ):
        """Creates dictionary self.css."""
        csspath = chop( str(head.select('link')[0]),'"','"')
        csstext = self._readf( os.path.join(root,csspath) )
        css = {}
        for tagtext in csstext.split('}'):
            css.setdefault( chop(tagtext,0,'{'), chop(tagtext,'{',None) )
        self.css = css
        
    def apply_css_class_style( self, tag='body' ):
        """Parses given class css, updates dictionary self.style."""
        if not tag in self.css.keys(): tag='body'
        styles = {}
        for line in self.css[tag].split('\n'):
            if len(line)==0: continue
            k = chop( line,0,':' )
            v = chop( line,':',';' )
            if v[-2:]=='px': v = int(v[:-2])
            elif v[-1:]=='%': v = float(v[:-1])/100
            elif v.isnumeric(): v = int(v)
            styles.setdefault( k, v )
        for k in styles.keys(): self.style[k]=styles[k]
    
    def init_typwriter( self ):
        """Sets initial values for the typewriter."""
        self.style = {} # reset
        self.apply_css_class_style() # set self.style lines from tag <body>
        self.w = self.style['width'] # page size
        self.h = self.style['height']
        self.caret = [0,0] # reset caret
        
    def _new_line( self, red ):
        self.caret[0] = self.style['margin-left']+pd.np.random.randint(-4,4)
        self.caret[1] += self.style['line-height']+pd.np.random.randint(-2,4)
        if red: self.caret[0]+=self.style['text-indent']
        
    def _new_page( self, red, mode ):
        if mode=='fit':
            self.caret[1] = self.style['margin-top']+self.style['line-height']
            self.caret[0] = self.style['margin-left']
        elif mode=='print':
            self.page_counter += 1
            self.page = PIL.Image.new( 'RGBA', (self.w,self.h), (255,255,255) )
        elif mode=='init':
            self.page_counter += 1
            self.page = PIL.Image.new( 'RGBA', (self.w,self.h), (255,255,255) )
            self.caret[1] = self.style['margin-top']
        
    def _perenos( self, text, iloc ):
        # whats up with this letter?
        if text[iloc] in self.A:
            for j in range( len(text[iloc:]),0,-1 ):
                try:
                    if text[j] in self.A: return j+iloc
                except IndexError:
                    if text[j] in self.A: return j+iloc
            return iloc
        
        # whats to the left of this letter?
        l, L = iloc, text[:iloc]
        for i in range(5):
            l = l-1 if len(L)>i else l
            if text[l] in self.A: return l
        
        # whats to the right of this letter?
        l, R = iloc, text[iloc:]
        l, r = iloc,iloc
        for i in range(1,5):
            l = r
            r = r+1 if len(R)>i else r
            if i<4:
                if (text[l] in self.C) & (text[r] in self.C): return r
                elif (text[l] in self.C) & (text[r] in self.A):
                    for j in range( len(text[r:]),0,-1 ):
                        if text[j] in self.A: return j+r
                elif text[l] in self.C: return l
            if text[r] in self.A:
                for j in range( len(text[r:]),0,-1 ):
                    if text[j] in self.A: return j+r
        
        if len(R)>=1: return r+1
        
    def _perenos_tire( self, text, iloc ):
        L, R = text[:iloc], text[iloc:]
        if len(L)>1:
            if text[iloc-1] in self.A: return False
        if len(R)>1:
            if text[iloc+1] in self.A: return False
        return True
        
    def fit_chars( self, text, chars ):
        text = list(text)
        max_chars_per_line = ((self.w-self.style['margin-right']-\
            self.style['margin-left'])//self.fo.avg_w)/self.style['size']
        chars_per_line = 0
        allowed_length = self.w-self.style['margin-left']-self.style['margin-right']*2
        ploc = None
        
        shift = 0
        charsdf = []
        iloc = 0
        while iloc<len(text):
            print(text[iloc],end='') # debug
            np = False
            if text[iloc]=='\n': # last iteration contained hyphen
                self._new_line(False)
                iloc += 1
                chars_per_line = 0
                ploc = None
                continue
            elif (text[iloc] in self.A)&(chars_per_line==0): # sign at the beginning
                if text[iloc]=='-' and text[iloc+1]=='\n': pass
                else:
                    temp = ''.join( text[iloc-chars_per_line:iloc-1] )
                    print( '\r'+temp,end='' ) # debug
                    iloc += 1
                    continue
                
            row = self.fo.df[ self.fo.df['path']==chars[iloc] ].iloc[0]
                
            # calc letter coords
            x = self.caret[0] + row['x']*self.style['size']
            y = self.caret[1] + row['y']*self.style['size']
            
            # hard limit reached - need new line/page?
            if (chars_per_line>=max_chars_per_line) & (x>=allowed_length):
                if iloc!=ploc: ploc=self._perenos(text,iloc)
                if iloc>ploc: # scroll back
                    temp = ''.join( text[iloc-chars_per_line:ploc-1] )
                    print( '\r'+temp,end='' ) # debug
                    #print(ploc,text[ploc],iloc,len(charsdf),shift,charsdf[ploc-shift:])
                    shift = iloc-len(charsdf)
                    charsdf = charsdf[:ploc-shift]
                    iloc = ploc
                    self.caret = charsdf[-1]['caret']
                    continue
                elif iloc==ploc:
                    text.insert( iloc, '\n' )
                    chars.insert( iloc, None )
                    if self._perenos_tire(text,iloc):
                        text.insert( iloc, '-' )
                        chars.insert( iloc, self.choose_chars('-')[0] )
                    chars_per_line = 0
                    ploc = None
                    continue
            if self.caret[1]+self.style['line-height']+self.style['line-height']>=self.h-self.style['margin-bottom']:    
                np = True
                self._new_page( False, 'fit' )
            
            # recalc letter coords
            x = self.caret[0] + row['x']*self.style['size']
            y = self.caret[1] + row['y']*self.style['size']
            # move caret for this letter
            self.caret[0] += row['x']*self.style['size']
            
            charsdf.append( {
                'x'    : int(x),
                'y'    : int(y),
                'text' : text[iloc],
                'path' : chars[iloc],
                'np'   : np,
                'caret': self.caret,
                'size' : ( int(row['w']*self.style['size']),
                    int(row['h']*self.style['size']) ),
                } )
    
            # move caret for next letter
            self.caret[0] += (row['nx'] + row['w'])*self.style['size']
            self.caret[1] += row['ny']*self.style['size']
            # counters
            iloc += 1
            chars_per_line += 1
            
        return pd.DataFrame( charsdf )
    
    @staticmethod
    def _readf( path ):
        with open( path, 'r', encoding='utf-8' ) as f: return f.read()
        
    @staticmethod
    def _cache_chars( chars, dest ):
        """Saves chosen chars into text file."""
        with open( dest, 'a', encoding='utf-8' ) as f:
            f.write( '\n'.join(chars) )
            f.write('\n')
        
    def _save_page( self ):
        name = str( self.page_counter )
        dpi = self.style['dpi']
        try:
            self.page.save( '%s.png' % name, 'PNG', dpi=(dpi,dpi) )
        except PermissionError:
            sleep(1)
            self._save_page()
    
    def _print_chars( self, charsdf ):
        for loc, row in charsdf.iterrows():
            if row['path']==None: continue
            #print(row['text'],end='') # debug
            
            if row['np']:
                self._save_page()
                self._new_page( False, 'print' )
                #self.page_counter += 1
                #self.page = PIL.Image.new( 'RGBA', (self.w,self.h), (255,255,255) )
                
            # print this letter
            with PIL.Image.open( row['path'] ) as im:
                im = im.resize( row['size'], resample=PIL.Image.BILINEAR )
                try:
                    self.page.paste( im, (row['x'],row['y']), im )
                except ValueError:
                    pass
            
        return pd.DataFrame( charsdf )
    
    def _print_table( self, soup ):
        trs = soup.select( 'tr' )
        ncols = len(trs)
        table_w = self.style['width']-(self.style['margin-left']+\
            self.style['margin-right'])-self.style['padding']*2
        
        trw = table_w/ncols
        trb = 0
        
        self.style['margin-left']+=self.style['padding']
        self.style['margin-right']+=self.style['padding'] + trw*(ncols-1) + \
            trw*(ncols-2)
        y = self.caret[1]
        for tr in trs:
            chardfs = []
            self.caret[1] = y
            self.style['margin-right']-= (trw+trb)
            
            tds = tr.select('td')
            for td in tds:
                self._new_line(True)
                print( '\n',self.style['margin-left'], self.caret[0],self.style['margin-right'] )
                # get and save the list of letters
                chars = self.choose_chars( td.text )
                charsdf = self.fit_chars( td.text, chars ) # +word breaks
                chardfs.append( charsdf )
            for charsdf in chardfs:
                self._print_chars( charsdf )
                
            self._save_page()
            #print()
            self.style['margin-left']+=trw+trb
            
    def print_int( self, soup ):
        pass
            
    def print_soup( self, soup ):
        tags_inside = 0
        for i, tag in enumerate( soup.find_all() ):
            self.apply_css_class_style( tag.name )
            
            if tag.name=='table': continue#self._print_table( tag )
            if tag.name=='tr': continue
            if tag.name=='td': continue
            if tag.name=='img':
                h = chop( str(tag), 'height="', 'px' )
                self.caret[1] += int( h )
                continue
            
            self._new_line(True)
            chars = self.choose_chars( tag.text )
            charsdf = self.fit_chars( tag.text, chars )
            #x = str(datetime.datetime.now()).replace(':','')
            #charsdf.to_excel( x+'.xls', index=False )
            self._print_chars( charsdf )
            self._save_page()
            print()
            print( '-'*10, tag.name )
            
            
            
            # skip duplicating
            tags_inside = len( tag.find_all() )
            if i<i+tags_inside: continue
            
            
        
        
        
            """
            
            
            if tag.name=='table':
                self._calctable( tag )
                continue
            elif tag.name in ['tr','td','br']: continue
            self._new_line(True)
            """
            
            """
            # technical division into blocks
            for block in tag.text.split( self.blocksep ):
                # get and save list of letters
                chars = self.choose_chars( block )
                charsdf = self.fit_chars( block, chars ) # +word breaks
                #self._cache_chars( chars, os.path.join(root,'chars.dat') )
                
                # place letters on the page
                self._print_chars( charsdf )
                
            self._save_page()
            print()
            print( '-'*10, tag.name )
            """
        
    def print_file( self, path ):
        self.blocksep = '\n\n' # technical splitter
        
        root = os.path.split(path)[0]
        text = self._readf(path) if os.path.isfile(path) else path
        soup = bs4.BeautifulSoup( text, 'html.parser' )
        
        head = soup.select('head')[0]
        self._get_css( head, root )
        self.init_typwriter()
        self._new_page( True, 'init' )
        
        body = soup.select('body')[0]
        self.print_soup( body )
        self.fo.savefont() # save new last use

def autorun():
    
    this_folder = os.path.dirname(__file__)
    fonts_folder = os.path.join(this_folder,'fonts')
    my_font_folder = os.path.join(fonts_folder,'step4kaggle_Editor')
    
    # setup fonts
    fo = Fonter.Fonter()
    fo.loadfont( 'body', my_font_folder )
    fo.selectfont( 'body' )
    
    # setup printer
    pr = Printer( fo )
    
    # print html
    pr.print_file( 'giant_lecture.html' )

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# 2018, 2019, 2020
