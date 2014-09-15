# -*- coding: utf-8 -*-

import wx
import mgr

class servers(mgr.Page):
	def __init__(self):
		pass

	def create(self, panel, data):
		root = super(servers, self).create(panel, data)

		panel = self.panel

		self.srv_lb = panel.m_server_list
		panel.Bind(wx.EVT_LISTBOX, self.onSelectServer, self.srv_lb)

		panel.Bind(wx.EVT_BUTTON, self.onOkBtn, panel.m_ok_btn)
		panel.Bind(wx.EVT_BUTTON, self.onDelBtn, panel.m_del_btn)
		panel.Bind(wx.EVT_BUTTON, self.onAddBtn, panel.m_add_btn)
		panel.Bind(wx.EVT_BUTTON, self.onAddConfirmBtn, panel.m_add_confirm_btn)

		self.targetIndex = None
		return root

	def onOkBtn(self, evt):
		if self.targetIndex == None:
			return
		if not self.panel.m_srv_pg.IsAnyModified():
			return
		self.updateTarget()
		self.saveAndReload(u"修改服务器配置")

	def onDelBtn(self, evt):
		if self.targetIndex == None:
			return
		if self.targetIndex < 0 or self.targetIndex >= len(self.srvs):
			return
		self.srvs.pop(self.targetIndex)
		self.saveAndReload(u"删除服务器配置")		

	def onAddBtn(self, evt):
		self.refresh()
		if not self.data:
			return

		self.panel.m_add_confirm_btn.Show()

	def onAddConfirmBtn(self, evt):
		newSrv = []
		if self.panel.m_srv_url1.GetValue() == None:
			return
		newSrv.append([self.panel.m_srv_url1.GetValue()])

		if self.panel.m_srv_id.GetValue() == None:
			return
		newSrv.append(self.panel.m_srv_id.GetValue())

		if self.panel.m_srv_name.GetValue() == None:
			return
		newSrv.append(self.panel.m_srv_name.GetValue())

		if self.panel.m_srv_stat.GetValue() == None:
			return
		newSrv.append(self.panel.m_srv_stat.GetValue())

		if self.panel.m_debug_srv.GetValue() == None:
			return
		newSrv.append(self.panel.m_debug_srv.GetValue())

		if self.panel.m_srv_port.GetValue() == None:
			return
		newSrv.append(self.panel.m_srv_port.GetValue())

		if self.panel.m_platform1.GetValue() == None:
			return
		newSrv.append([self.panel.m_platform1.GetValue()])

		self.srvs.append(newSrv)
		if self.saveAndReload(u"添加新的服务器"):
			self.panel.m_add_confirm_btn.Hide()

	def updateSrvList(self):
		self.srv_lb.Clear()
		for i, srv in enumerate(self.srvs):
			self.srv_lb.Append(u"{:>4} {:<4}".format(srv[1], srv[2]))
			self.srv_lb.SetClientData(i, srv)

		self.resetPG()

	def onSelectTarget(self, pl_name, os_name):
		self.refresh()

	def onSelectServer(self, evt):
		lb = evt.GetEventObject()
		self.targetIndex = lb.GetSelection()
		self.target_srv = self.srvs[self.targetIndex]
		self.refreshPG()

	def resetPG(self):
		self.targetIndex = None
		self.target_srv = [None for i in xrange(10)]
		self.target_srv[0] = (None,)
		self.target_srv[6] = (None,)
		self.refreshPG()

	def refreshPG(self):
		self.panel.m_srv_id.SetValue(self.target_srv[1])
		self.panel.m_srv_name.SetValue(self.target_srv[2])
		self.panel.m_srv_stat.SetValue(self.target_srv[3])
		self.panel.m_debug_srv.SetValue(self.target_srv[4])
		self.panel.m_srv_port.SetValue(self.target_srv[5])
		self.panel.m_srv_url1.SetValue(self.target_srv[0][0])
		self.panel.m_platform1.SetValue(self.target_srv[6][0])
		self.panel.m_add_confirm_btn.Hide()

	def updateTarget(self):
		modified = False
		if self.target_srv[1] != self.panel.m_srv_id.GetValue():
			self.target_srv[1] = self.panel.m_srv_id.GetValue()
			modified = True
		if self.target_srv[2] != self.panel.m_srv_name.GetValue():
			self.target_srv[2] = self.panel.m_srv_name.GetValue()
			modified = True
		if self.target_srv[3] != self.panel.m_srv_stat.GetValue():
			self.target_srv[3] = self.panel.m_srv_stat.GetValue()
			modified = True
		if self.target_srv[4] != int(self.panel.m_debug_srv.GetValue()):
			self.target_srv[4] = int(self.panel.m_debug_srv.GetValue())
			modified = True
		if self.target_srv[5] != self.panel.m_srv_port.GetValue():
			self.target_srv[5] = self.panel.m_srv_port.GetValue()
			modified = True
		if self.target_srv[0][0] != self.panel.m_srv_url1.GetValue():
			self.target_srv[0][0] = self.panel.m_srv_url1.GetValue()
			modified = True
		if self.target_srv[6][0] != self.panel.m_platform1.GetValue():
			self.target_srv[6][0] = self.panel.m_platform1.GetValue()
			modified = True
		return modified

	def refresh(self):
		self.srv_lb.Clear()
		self.resetPG()
		self.panel.m_add_confirm_btn.Hide()

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

		self.srvs = self.data.get('urls',{}).get("SERVER_LIST")
		self.updateSrvList()
