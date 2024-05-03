# -*- coding: utf-8 -*-
#Python utility "Minimal Widgets". Contains several custom widgets, made with PyQt5. Copyright (C) 2019 Anna Anikina
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
# pip install
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
    )
# same folder

class EditorV2( QWidget ):
    
    def __init__( self,
                  *args, **kwargs ):
        super( EditorV2, self ).__init__( *args, **kwargs )
        
        self.__init_gui()
        
    def __init_gui_textarea( self ):
        vbox = QVBoxLayout()
        
        fontdir = QLabel( self )
        fontdir.setText( 'Path to font:' )
        self.fontdir = QLineEdit( self )
        
        line_shifter = QLabel( self )
        line_shifter.setText( 'Line shift:' )
        self.line_shifter = QLineEdit( self )
        
        self.ok = QPushButton( self )
        self.ok.setText( 'Save changes' )
        self.re = QPushButton( self )
        self.re.setText( "Re-render (reloads font)" )
        
        vbox.addWidget( fontdir )
        vbox.addWidget( self.fontdir )
        vbox.addWidget( line_shifter )
        vbox.addWidget( self.line_shifter )
        vbox.addWidget( self.ok )
        vbox.addWidget( self.re )
        
        self.setLayout( vbox )
        
    def __init_gui( self ):
        self.setWindowFlags( Qt.WindowStaysOnTopHint )
        self.setWindowTitle( 'Font Browser' )
        self.__init_gui_textarea()

class Marker( QWidget ):
    
    def __init__( self,
                  *args, **kwargs ):
        super( Marker, self ).__init__( *args, **kwargs )
        
        self.__init_gui()
        
    def init_textarea( self ):
        vbox = QVBoxLayout()
        
        fontdir = QLabel( self )
        fontdir.setText( 'Path to font:' )
        self.fontdir = QLineEdit( self )
        
        line_shifter = QLabel( self )
        line_shifter.setText( 'Line shift:' )
        self.line_shifter = QLineEdit( self )
        
        self.ok = QPushButton( self )
        self.ok.setText( 'Save changes' )
        self.re = QPushButton( self )
        self.re.setText( "Re-render (reloads font)" )
        
        vbox.addWidget( fontdir )
        vbox.addWidget( self.fontdir )
        vbox.addWidget( line_shifter )
        vbox.addWidget( self.line_shifter )
        vbox.addWidget( self.ok )
        vbox.addWidget( self.re )
        
        self.setLayout( vbox )
        
    def __init_gui( self ):
        self.setWindowFlags( Qt.WindowStaysOnTopHint )
        self.setWindowTitle( 'Marker Painter' )
        self.__init_gui_textarea()
    
#---------------------------------------------------------------------------+++
# 2019
