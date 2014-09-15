# -*- coding: utf-8 -*-

import wx
import mgr

SHUTDOWN = 0
NORMAL = 1

class billboard(mgr.Page):
	def __init__(self):
		pass

	def create(self, panel, data):
		root = super(billboard, self).create(panel, data)

		panel = self.panel

		type_cb = wx.FindWindowByName("m_billboard_type", panel)
		panel.Bind(wx.EVT_COMBOBOX, self.onSelectType, type_cb)

		ok_btn = wx.FindWindowByName("m_ok_btn", panel)
		panel.Bind(wx.EVT_BUTTON, self.onOkBtn, ok_btn)

		del_btn = wx.FindWindowByName("m_del_btn", panel)
		panel.Bind(wx.EVT_BUTTON, self.onDelBtn, del_btn)

		return root

	def isModified(self):
		title = wx.FindWindowByName("m_billboard_title", self.panel)
		texts = wx.FindWindowByName("m_billboard_content", self.panel)
		return title.IsModified() or texts.IsModified()

	def onOkBtn(self, evt):
		if not self.isModified():
			return

		title = wx.FindWindowByName("m_billboard_title", self.panel)
		texts = wx.FindWindowByName("m_billboard_content", self.panel)

		title_str = title.GetValue()
		if not title_str: return

		text_str = texts.GetValue()
		if not text_str: return

		btype = self.getType()
		if btype == SHUTDOWN:
			typename=u"关服公告"
			self.data['notice'] = {"title":title_str, "text":text_str}
		else:
			typename=u"普通公告"
			self.data['billboard']=[{"title":title_str, "text":text_str}]

		self.saveAndReload(u"修改%s"%typename)

	def onDelBtn(self, evt):
		btype = self.getType()
		typename = ""
		if btype == SHUTDOWN:
			typename=u"关服公告"
			self.data.pop("notice", None)
		else:
			typename=u"普通公告"
			self.data.pop("billboard", None)

		self.saveAndReload(u"删除%s"%typename)

	def onSelectType(self, evt):
		self.refresh()

	def onSelectTarget(self, pl_name, os_name):
		self.refresh()

	def getType(self):
		type_cb = wx.FindWindowByName("m_billboard_type", self.panel)
		return type_cb.GetSelection()

	def refresh(self):
		btype = self.getType()

		pl_name, os_name = self.getTargetData()

		title = wx.FindWindowByName("m_billboard_title", self.panel)
		texts = wx.FindWindowByName("m_billboard_content", self.panel)

		title.SetValue("")
		texts.SetValue("")

		self.data = None
		if pl_name and os_name:
			self.data = mgr.Inst.getData(pl_name, os_name)
		else:
			return

		if not self.data:
			if self.retryPrompt(u"加载数据出错，是否重试"):
				self.refresh()
			return

		if btype == SHUTDOWN:
			notice = self.data.get("notice", None)
			if notice:
				title.SetValue(notice['title'])
				texts.SetValue(notice['text'])
		else:
			bb = self.data.get("billboard", None)
			if bb:
				title.SetValue(bb[0]['title'])
				texts.SetValue(bb[0]['text'])

