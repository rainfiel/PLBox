
import wx
import wx.xrc as xrc
import json
import codecs

Inst = None

class Page(object):
	def __init__(self):
		self.panel = None

	def create(self, data, container):
		self.data = data
		self.container = container
		self.panel = None

		# wx.StaticText(self.panel, -1, self.data.desc, (10, 10))

		res = xrc.XmlResource("pages/"+self.data.pageModule+".xrc")
		if res:
			self.panel = res.LoadPanel(self.container, "root")

		if not self.panel:
			self.panel = wx.Panel(self.container)

		self.panel.SetAutoLayout(True)
		return self.panel

class Tool(object):
	def __init__(self, data):
		self.__dict__.update(data)
		pageModule = __import__("pages."+self.pageModule, fromlist=['pages'])
		self.page = getattr(pageModule, self.pageModule)()

	def createPage(self, container):
		return self.page.create(self, container)

class Mgr(object):
	def __init__(self, path):
		self.config = self.loadConfig(path)
		tools = self.config['tools']
		def fun(a, b):
			assert(a['id'] != b['id'])
			return a['id'] > b['id'] and 1 or -1
		tools.sort(fun)
		self.tools = [Tool(i) for i in tools]

	def platform(self):
		return [i['name'] for i in self.config['platform']]

	def os(self):
		return [i['name'] for i in self.config['os']]

	def loadConfig(self, path):
		f=codecs.open(path, 'r', 'utf8')
		return json.load(f, strict=False)

	def dataPath(self, PL, OS):
		root = self.config['data_root']
		return "%s\\%s\\%s\\debug\\launcher.json" % (root, PL, OS)

	def getData(self, PL, OS):
		path = self.dataPath(PL, OS)
		return self.loadConfig(path)

	def saveData(self, PL, OS, data):
		path = self.dataPath(PL, OS)
		f=codecs.open(path, 'w', 'utf-8')
		json.dump(data, f, sort_keys = True, indent = 4, ensure_ascii=False)
		f.close()

#---------------------helpers----------------------------
class EventHandler(object):
	def __init__(self, functor, arg):
		self.functor = functor
		self.arg = arg

	def __call__(self, evt):
		pl_name, os_name = getTargetData(self.arg)
		self.functor(pl_name, os_name)

def setupTargetData(panel, os_callback, pl_callback):
	os_lb = wx.FindWindowByName("m_os_lb", panel)
	for i, j in enumerate(Inst.os()):
		os_lb.Append(j)
		os_lb.SetClientData(i, j)
	panel.Bind(wx.EVT_LISTBOX, EventHandler(os_callback, panel), os_lb)

	pl_lb = wx.FindWindowByName("m_platform_lb", panel)
	for i, j in enumerate(Inst.platform()):
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

def init(path):
	global Inst
	Inst = Mgr(path)
