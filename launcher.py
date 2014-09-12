
import wx

__all__ = ["setupTargetData", "getTargetData", "launcherInit"]

Config = None

def launcherInit(cfg):
	global Config
	Config = cfg

class EventHandler(object):
	def __init__(self, functor, arg):
		self.functor = functor
		self.arg = arg

	def __call__(self, evt):
		pl_name, os_name = getTargetData(self.arg)
		self.functor(pl_name, os_name)

def setupTargetData(panel, os_callback, pl_callback):
	os_lb = wx.FindWindowByName("m_os_lb", panel)
	for i, j in enumerate(Config.os()):
		os_lb.Append(j)
		os_lb.SetClientData(i, j)
	panel.Bind(wx.EVT_LISTBOX, EventHandler(os_callback, panel), os_lb)

	pl_lb = wx.FindWindowByName("m_platform_lb", panel)
	for i, j in enumerate(Config.platform()):
		pl_lb.Append(j)
		pl_lb.SetClientData(i, j)
	panel.Bind(wx.EVT_LISTBOX, EventHandler(pl_callback, panel), pl_lb)

def getTargetData(panel):
	os_lb = wx.FindWindowByName("m_os_lb", panel)
	select = os_lb.GetSelection()
	os_name = None
	if select != -1:
		os_name = os_lb.GetClientData(select)

	pl_lb = wx.FindWindowByName("m_platform_lb", panel)
	select = pl_lb.GetSelection()
	pl_name = None
	if select != -1:
		pl_name = pl_lb.GetClientData(pl_lb.GetSelection())

	return pl_name, os_name
