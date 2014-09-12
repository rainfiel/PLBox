# -*- coding: utf-8 -*-

import wx
import mgr

class servers(mgr.Page):
	def __init__(self):
		pass

	def create(self, panel, data):
		root = super(servers, self).create(panel, data)

		panel = self.panel

		self.srv_lb = wx.FindWindowByName("m_server_list", panel)
		panel.Bind(wx.EVT_LISTBOX, self.onSelectServer, self.srv_lb)

		return root

	def setServerList(self, srvs):
		self.srv_lb.Clear()
		for i, srv in enumerate(srvs):
			self.srv_lb.Append(srv)
			self.srv_lb.SetClientData(i, srv)

	def onSelectTarget(self, pl_name, os_name):
		self.refresh()

	def onSelectServer(self, evt):
		lb = evt.GetEventObject()
		print(lb.GetSelection())

	def refresh(self):
		pl_name, os_name = self.getTargetData()
		self.data = None
		if pl_name and os_name:
			self.data = mgr.Inst.getData(pl_name, os_name)
			assert(self.data)
		else:
			return

		if not self.data:
			if self.retryPrompt(u"加载数据出错，是否重试"):
				self.refresh()
			return

		srvs = self.data.get('urls',{}).get("SERVER_LIST")
		names = [ u"{:>4} {:<4}".format(i[1], i[2]) for i in srvs]
		self.setServerList(names)
