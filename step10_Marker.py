# -*- coding: utf-8 -*-
#Python utility "Marker". Allows to iteratively mark 4 points an all images in given folder via PyQt5 and OpenCV. Copyright (C) 2020 Anna Anikina
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#---------------------------------------------------------------------------+++

# embedded in python
import os
import sys
# pip install
import cv2
import pandas as pd
import PIL
from PyQt5 import QtCore, QtWidgets
# same folder
import step5_Printer
import Fonter
import gxd

class Marker( object ):
    
    """This object allows to mark 4 points in the image:
    1: letter left connector start (from previous letter to current one)
    2: letter left connector end (current letter)
    3: letter right connector start (current letter)
    4: letter right connector end (from current letter to next one)."""
    
    def __init__( self,
                  font,
                  *args, **kwargs ):
        super( Marker, self ).__init__( *args, **kwargs )
        
        self.fo = font
        self.pr = step5_Printer.Printer( font )
        self.__init_gui()
        
        self.iloc = 60
        self.AAAAAAAAAAAA()
        
        sys.exit( self.app.exec_() )
    
    def cv2_line_shift( self ):
        nlines = ( self.printer.my-self.printer.mary*2 )//self.printer.nl
        x = self.printer.mx-self.printer.marx
        for i in range(nlines):
            colour = (0,0,255) if i==0 else (0,255,0)
            y = self.printer.mary + self.printer.nl*i + self.line_shifter
            cv2.line( self.currentim, (self.printer.marx,y), (x,y), colour, 1)
            
    def cv2_load_image( self ):
        im = PIL.Image.open( self.selected['path'] )
        bg = PIL.Image.new( 'RGBA', im.size, (255,255,255) )
        bg.paste( im, (0,0), im )
        bg.save( 'marker.png' )
        self.currentim = cv2.imread( 'marker.png' )
        newX,newY = self.currentim.shape[1]*self.scaler, self.currentim.shape[0]*self.scaler
        self.currentim = cv2.resize(self.currentim,(int(newX),int(newY)))
            
    def cv2_reset_image( self ):
        self.cv2_load_image()
        self.line_shifter = int( self.w.line_shifter.text() )
        self.cv2_line_shift()
        
    def cv_2events( self, event, x, y, flags, param ):
        if event == cv2.EVENT_LBUTTONDOWN:
            k = self.fo.df['path']==self.selected['path']
            if self.point_type==1:
                self.fo.df.loc[k,'p1x']=x//self.scaler
                self.fo.df.loc[k,'p1y']=y//self.scaler
                cv2.circle(self.currentim,(x,y),2,(0,0,255),-1)
            if self.point_type==2:
                self.fo.df.loc[k,'p2x']=x//self.scaler
                self.fo.df.loc[k,'p2y']=y//self.scaler
                cv2.circle(self.currentim,(x,y),2,(0,100,200),-1)
            if self.point_type==3:
                self.fo.df.loc[k,'p3x']=x//self.scaler
                self.fo.df.loc[k,'p3y']=y//self.scaler
                cv2.circle(self.currentim,(x,y),2,(234,122,6),-1)
            if self.point_type==4:
                self.fo.df.loc[k,'p4x']=x//self.scaler
                self.fo.df.loc[k,'p4y']=y//self.scaler
                cv2.circle(self.currentim,(x,y),2,(255,0,0),-1)
            self.point_type += 1
            print( self.fo.df.iloc[self.iloc] )
            print( self.point_type )
        if event == cv2.EVENT_RBUTTONDOWN:
            k = self.fo.df['path']==self.selected['path']
            self.fo.df.loc[k,'p1x']=pd.np.nan
            self.fo.df.loc[k,'p1y']=pd.np.nan
            self.fo.df.loc[k,'p2x']=pd.np.nan
            self.fo.df.loc[k,'p2y']=pd.np.nan
            self.fo.df.loc[k,'p3x']=pd.np.nan
            self.fo.df.loc[k,'p3y']=pd.np.nan
            self.fo.df.loc[k,'p4x']=pd.np.nan
            self.fo.df.loc[k,'p4y']=pd.np.nan
            self.point_type = 5
            
    def save_df_changes( self ):
        self.fo.savefont()
        
    def cv2_something( self ):
        wint = 'Printed text:' # title cv2.namedWindow
        self.scaler = 5
        self.cv2_load_image()
        
        self.line_shifter = 20
        self.point_type = 1
        
        cv2.namedWindow( wint )
        cv2.setMouseCallback( wint, self.cv_2events )
        
        while True:
            k = self.fo.df['path']==self.selected['path']
            self.fo.df.loc[k,'p1x']=pd.np.nan
            self.fo.df.loc[k,'p1y']=pd.np.nan
            self.fo.df.loc[k,'p2x']=pd.np.nan
            self.fo.df.loc[k,'p2y']=pd.np.nan
            self.fo.df.loc[k,'p3x']=pd.np.nan
            self.fo.df.loc[k,'p3y']=pd.np.nan
            self.fo.df.loc[k,'p4x']=pd.np.nan
            self.fo.df.loc[k,'p4y']=pd.np.nan
            cv2.imshow( wint, self.currentim )
            key = cv2.waitKey(1) & 0xFF
            if key==27: break # esc
            elif key==49: self.point_type=1
            elif key==50: self.point_type=2
            elif key==51: self.point_type=3
            elif key==52: self.point_type=4
            elif key==13 or self.point_type>4: # enter
                self.save_df_changes()
                break
            elif key!=255: print('no effect key',key)
            
        cv2.destroyAllWindows()
        self.iloc+=1
        self.AAAAAAAAAAAA()
        
    def AAAAAAAAAAAA( self ):
        for _, row in self.fo.df.iterrows():
            self.selected = self.fo.df.iloc[self.iloc]
            self.cv2_something()
        
    @staticmethod
    def menu_exitact():
        QtCore.QCoreApplication.exit()
        
    def __init_gui( self ):
        self.app = QtWidgets.QApplication( sys.argv )
        
        self.w = gxd.EditorV2()
        self.w.line_shifter.textChanged.connect( self.cv2_reset_image )
        self.w.show()
        
def autorun():
    
    this_folder = os.path.dirname(__file__)
    fonts_folder = os.path.join(this_folder,'fonts')
    my_font_folder = os.path.join(fonts_folder,'step4kaggle_Editor')

    fo = Fonter.Fonter()
    fo.loadfont( 'body', my_font_folder )
    fo.selectfont( 'body' )
    ob = Marker( fo )

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# 2020
