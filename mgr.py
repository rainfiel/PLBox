
import wx
import json
import codecs

Inst = None

class Page(object):
	def __init__(self):
		self.panel = None

	def create(self, panel, data):
		self.panel = panel
		self.data = data

		wx.StaticText(self.panel, -1, self.data.desc, (10, 10))

class Tool(object):
	def __init__(self, data):
		self.__dict__.update(data)
		pageModule = __import__("pages."+self.pageModule, fromlist=['pages'])
		self.page = getattr(pageModule, self.pageModule)()

	def createPage(self, panel):
		self.page.create(panel, self)

class Mgr(object):
	def __init__(self, path):
		self.config = self.loadConfig(path)
		tools = self.config['tools']
		def fun(a, b):
			assert(a['id'] != b['id'])
			return a['id'] > b['id'] and 1 or -1
		tools.sort(fun)
		self.tools = [Tool(i) for i in tools]

	def loadConfig(self, path):
		f=codecs.open(path, 'r', 'utf8')
		return json.load(f)

def init(path):
	global Inst
	Inst = Mgr(path)