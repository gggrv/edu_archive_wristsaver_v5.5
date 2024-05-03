# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# embedded in python
import os
import sys
# pip install
import bs4
import cv2
import pandas as pd
import PIL
from PIL import Image
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QApplication,
    )
# same folder
from txd import chop
import gxd
import Fonter

class PrinterForEditing( object ):
    
    """Special Printer.
    Allows to edit font letter properties: make this
    letter be printed higher/lower, more to the left/right; make next
    letter after this one be printed more to the left/right.
    Prints all possible letter versions (for example,
    if letter "a" has 50 versions, it will print a1,a2,a3...a50) for given
    small line of text.
    Example: line="test", output="ttteeeeessssssssssttt".
    """
    
    maxlu = 500 # printer's max last use
    page_counter = 0 # how many pages
    C = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    A = list( """., _+-=():;!?"'/%""" )
    
    def __init__( self,
                  font,
                  *args, **kwargs ):
        super().__init__( *args, **kwargs )
        
        self.fo = font
    
    def cv2_line_split( self ):
        nlines = ( self.style['height']-self.style['margin-top']-self.style['margin-bottom'] )//self.style['line-height']
        x = self.style['width']-self.style['margin-left']
        for i in range(nlines):
            colour = (0,0,255) if i==0 else (0,255,0)
            y = self.style['margin-top'] + self.style['line-height']*i + self.line_shifter
            cv2.line( self.currentim, (self.style['margin-left'],y), (x,y), colour, 1)
            
    def cv2_reset_image( self ):
        self.currentim = cv2.imread( 'editor.png' )
        self.line_shifter = int( self.W.line_shifter.text() )
        self.cv2_line_split()
        
    def cv2_events( self, event, x, y, flags, param ):
        if event == cv2.EVENT_LBUTTONDOWN:
            # a letter was chosen, clear the frame
            self.W.line_shifter.setText( str(self.line_shifter) )
            self.cv2_reset_image()
            
            # select the letter
            df = self.charsdf
            df['click'] = pd.np.abs(df['x']-x) + pd.np.abs(df['y']-y)
            letter = df.sort_values( 'click', ascending=True ).iloc[0]
            self.selected = letter
            print( self.selected )
            print( self.fo.df[self.fo.df['path']==self.selected['path']].iloc[0] )
            
            # paint the frame around it
            cv2.rectangle( self.currentim, (letter['x'],letter['y']),
                ( letter['x']+letter['size'][0],
                letter['y']+letter['size'][1] ),
                (0,0,255), 1 )
            
    def apply_df_changes( self ):
        """Writes changes to self.printer.df"""
        k = self.fo.df['path']==self.selected['path']
        
        # edited nx
        if self.editnext<0: self.fo.df.loc[k,'nx'] += \
            self.selected['x']-self.roifrom[0]
        # edited x
        else: self.fo.df.loc[k,'x'] += \
            self.roifrom[0]-self.selected['x']
        # edited y
        self.fo.df.loc[k,'y'] += self.roifrom[1]-self.selected['y']
        print( self.fo.df.loc[k] )
        print( 'applied' )
        
        # save the changes to the image
        #cv2.imwrite( 'editor.png', self.currentim )
            
    def save_df_changes( self ):
        self.fo.savefont()
            
    def cv2_moveletter( self, direction ):
        """Move, until ENTER is pressed."""
        if not self.editmode:
            self.editmode=True
            print( 'editing %s is ON... (press ENTER when finished, C to change)' % self.selected['path'] )
            print('-- editing x') if self.editnext>0 else print('-- editing nextx')
            # remember the piece of the image
            x,y = self.selected['x'],self.selected['y']
            w,h = self.selected['size'][0],self.selected['size'][1]
            self.roi = self.currentim[y:y+h,x:x+w]
            self.roifrom = [x,y,w,h]
            print( y,y+h,x,x+w )
        # reset the image
        self.currentim = cv2.imread( 'editor.png' )
        # paint the initial space in the remembered picture with white
        cv2.rectangle( self.currentim,
            (self.selected['x'],self.selected['y']),
            (self.selected['x']+self.selected['size'][0],
            self.selected['y']+self.selected['size'][1]),
            (255,255,255), -1 )
            
        # paste the coords of the remembered picture according to direction
        if   direction==119: self.roifrom[1]-=1 # w
        elif direction==115: self.roifrom[1]+=1 # s
        elif direction==97 : self.roifrom[0]-=1 # a
        elif direction==100: self.roifrom[0]+=1 # d
        print( self.selected['x']-self.roifrom[0], self.roifrom[1]-self.selected['y'] )
        # paste the actual remembered image to these coords
        x,y = self.roifrom[0],self.roifrom[1]
        w,h = self.roifrom[2],self.roifrom[3]
        self.currentim[y:y+h,x:x+w] = self.roi
        # restore lines
        self.line_shifter = int( self.W.line_shifter.text() )
        self.cv2_line_split()
        
    def cv2_something( self ):
        wint = 'Printed text:' # name of the cv2.namedWindow
        self.currentim = cv2.imread( 'editor.png' )
        self.line_shifter = 20
        self.selected = self.charsdf.iloc[0] # unique letter id
    
        self.editmode = False
        self.editnext = -1 # edit x → will be negative
        
        cv2.namedWindow( wint )
        cv2.setMouseCallback( wint, self.cv2_events )
        
        while True:
            cv2.imshow( wint, self.currentim )
            key = cv2.waitKey(1) & 0xFF
            if key==27: break # esc
            elif (key==119)|(key==115)|(key==97)|(key==100): # wsad
                self.cv2_moveletter( key )
            elif key==13 : # enter
                self.editmode = False 
                print( 'editing is OFF.' )
                self.apply_df_changes()
            elif key==99: # c
                self.editnext *= -1
                print('-- editing x') if self.editnext>0 else print('-- editing nextx')
            elif key!=255: print('no effect key',key)
                
            
        cv2.destroyAllWindows()
        
    @staticmethod
    def menu_exitact():
        QCoreApplication.exit()
        
    def __init_gui( self ):
        self.app = QApplication( sys.argv )
        
        this_folder = os.path.dirname(__file__)
        fonts_folder = os.path.join(this_folder,'fonts')
        my_font_folder = os.path.join(fonts_folder,'step4kaggle_Editor')
        
        self.W = gxd.EditorV2()
        self.W.fontdir.setText( my_font_folder )
        self.W.line_shifter.textChanged.connect( self.cv2_reset_image )
        self.W.ok.clicked.connect( self.save_df_changes )
        self.W.re.clicked.connect( self.prifile )
        self.W.show()
    
    def _hasnopool( self, pool ):
        if len(pool)==0: return self.fo.df[ self.fo.df['text']=='absent' ]
        return pool
            
    def choose_chars( self, text ):
        """Selects some letters from the font."""
        choices = []
        for iloc, l in enumerate( text ):
            pool = self.fo.df[ self.fo.df['text']==l ]
            pool = self._hasnopool(pool)
            for loc, row in pool.iterrows():
                choices.append( row['path'] )
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
        
        print(']]]',R,'[[[')
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
        
        charsdf = []
        iloc = 0
        while iloc<len(chars):
            np = False
            row = self.fo.df[ self.fo.df['path']==chars[iloc] ].iloc[0]
                
            # calc letter coords
            x = self.caret[0] + row['x']*self.style['size']
            y = self.caret[1] + row['y']*self.style['size']
            
            # hard limit reached - need new line/page?
            if (chars_per_line>=max_chars_per_line) & (x>=allowed_length):
                self._new_line( False )
                
            # recalc letter coords
            x = self.caret[0] + row['x']*self.style['size']
            y = self.caret[1] + row['y']*self.style['size']
            # move caret for this letter
            self.caret[0] += row['x']*self.style['size']
            
            charsdf.append( {
                'x'    : int(x),
                'y'    : int(y),
                'text' : '',
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
        name = 'editor'
        self.page.save( '%s.png' % name, 'PNG',
            dpi=(self.style['dpi'],self.style['dpi']) )
    
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
            im = PIL.Image.open( row['path'] )
            im = im.resize( row['size'], resample=PIL.Image.BILINEAR )
            self.page.paste( im, (row['x'],row['y']), im )
            
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
            
    def print_soup( self, soup ):
        for i, tag in enumerate( soup.find_all() ):
            self.apply_css_class_style( tag.name )
            
            self._new_line(True)
            chars = self.choose_chars( tag.text )
            charsdf = self.fit_chars( tag.text, chars )
            self._print_chars( charsdf )
            self._save_page()
            
            self.charsdf = charsdf
            print()
            print( '-'*10, tag.name )
            break
        
    def print_file( self, path ):
        self.wawawa = path
        root = os.path.split(path)[0]
        text = self._readf(path) if os.path.isfile(path) else path
        soup = bs4.BeautifulSoup( text, 'html.parser' )
        
        head = soup.select('head')[0]
        self._get_css( head, root )
        self.init_typwriter()
        self._new_page( True, 'init' )
        
        body = soup.select('body')[0]
        self.print_soup( body )
        
        self.__init_gui()
        self.cv2_something()
        sys.exit( self.app.exec_() )
        
    def prifile( self ):
        cv2.destroyAllWindows()
        root = os.path.split(self.wawawa)[0]
        text = self._readf(self.wawawa) if os.path.isfile(self.wawawa) else self.wawawa
        soup = bs4.BeautifulSoup( text, 'html.parser' )
        
        head = soup.select('head')[0]
        self._get_css( head, root )
        self.init_typwriter()
        self._new_page( True, 'init' )
        
        body = soup.select('body')[0]
        self.print_soup( body )
        
        self.__init_gui()
        self.cv2_something()
        sys.exit( self.app.exec_() )

def autorun():
    
    this_folder = os.path.dirname(__file__)
    fonts_folder = os.path.join(this_folder,'fonts')
    my_font_folder = os.path.join(fonts_folder,'step4kaggle_Editor')
    
    # setup fonts
    fo = Fonter.Fonter()
    fo.loadfont( 'body', my_font_folder )
    fo.selectfont( 'body' )
    
    # setup printer
    pr = PrinterForEditing( fo )
    
    # print html
    pr.print_file( os.path.join(this_folder,'printer_for_editing.html') )

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# 2018, 2019, 2020
