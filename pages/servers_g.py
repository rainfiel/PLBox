# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.propgrid as pg

###########################################################################
## Class root
###########################################################################

class root ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 511,307 ), style = wx.TAB_TRAVERSAL )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Step 2: 选择服务器" ), wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		m_server_listChoices = []
		self.m_server_list = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_server_listChoices, 0 )
		self.m_server_list.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Fixedsys" ) )
		
		bSizer5.Add( self.m_server_list, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		sbSizer2.Add( bSizer5, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_srv_pg = pg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_BOLD_MODIFIED|wx.propgrid.PG_DEFAULT_STYLE|wx.propgrid.PG_SPLITTER_AUTO_CENTER)
		self.m_srv_pg.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		
		self.m_propertyGridItem12 = self.m_srv_pg.Append( pg.PropertyCategory( u"服务器属性", u"服务器属性" ) ) 
		self.m_srv_name = self.m_srv_pg.Append( pg.StringProperty( u"服务器名", u"服务器名" ) ) 
		self.m_srv_id = self.m_srv_pg.Append( pg.IntProperty( u"服务器ID", u"服务器ID" ) ) 
		self.m_debug_srv = self.m_srv_pg.Append( pg.BoolProperty( u"测试服", u"测试服" ) ) 
		self.m_srv_stat = self.m_srv_pg.Append( pg.IntProperty( u"状态", u"状态" ) ) 
		self.m_propertyGridItem8 = self.m_srv_pg.Append( pg.PropertyCategory( u"服务器地址配置", u"服务器地址配置" ) ) 
		self.m_srv_port = self.m_srv_pg.Append( pg.IntProperty( u"端口", u"端口" ) ) 
		self.m_srv_url1 = self.m_srv_pg.Append( pg.StringProperty( u"服务器URL", u"服务器URL" ) ) 
		self.m_platform1 = self.m_srv_pg.Append( pg.StringProperty( u"平台登陆URL", u"平台登陆URL" ) ) 
		bSizer3.Add( self.m_srv_pg, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		sbSizer2.Add( bSizer3, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer8.Add( sbSizer2, 1, wx.EXPAND|wx.ALL, 5 )
		
		sbSizer21 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Step 3: 操作" ), wx.HORIZONTAL )
		
		self.m_ok_btn = wx.Button( self, wx.ID_ANY, u"确认修改", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer21.Add( self.m_ok_btn, 0, wx.ALL, 5 )
		
		self.m_del_btn = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer21.Add( self.m_del_btn, 0, wx.ALL, 5 )
		
		self.m_add_btn = wx.Button( self, wx.ID_ANY, u"添加", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer21.Add( self.m_add_btn, 0, wx.ALL, 5 )
		
		self.m_add_confirm_btn = wx.Button( self, wx.ID_ANY, u"确认添加", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer21.Add( self.m_add_confirm_btn, 0, wx.ALL, 5 )
		
		
		bSizer8.Add( sbSizer21, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer8 )
		self.Layout()
	
	def __del__( self ):
		pass
	

