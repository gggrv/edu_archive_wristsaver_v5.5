# -*- coding: utf-8 -*-

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
