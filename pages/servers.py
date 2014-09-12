
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
		
		self.setServerList(("aaaa", "bbbb", "cccc"))

		return root

	def setServerList(self, srvs):
		for i, srv in enumerate(srvs):
			self.srv_lb.Append(srv)
			self.srv_lb.SetClientData(i, srv)

	def onSelectTarget(self, pl_name, os_name):
		self.refresh()

	def onSelectServer(self, evt):
		self.refresh()
		lb = evt.GetEventObject()
		print(lb.GetClientData(lb.GetSelection()))

	def refresh(self):
		pl_name, os_name = self.getTargetData()
		self.data = None
		if pl_name and os_name:
			self.data = mgr.Inst.getData(pl_name, os_name)
			assert(self.data)
		else:
			return

