# -*- coding: utf-8 -*-

import os
import wx
import wx.xrc as xrc
import json
import codecs
import requests
import json

from launcher import *

Inst = None
LOG_URL = "https://testcmk.ejoy.com/dl/DPL/create"
headers = {'Content-type': 'application/json; charset=utf-8', 'Accept': 'application/json'}
SCP = "pscp -P %d -i %s launcher.json %s@%s%s"

class Page(object):
	def __init__(self):
		self.panel = None
		self.processing = False

	#---------interface--------------------------
	def onSelectTarget(self, pl_name, os_name):
		pass
	#--------------------------------------------

	def process(self, name, functor, args):
		ret = Inst.postToSlack(u"```准备执行操作:[%s]```"%name)
		if not ret:
			if self.retryPrompt(u"log服务器出错,是否重试?"):
				self.process(name, functor, args)
			return

		ret = functor(*args)
		if not ret:
			ret = Inst.postToSlack(u"[%s], 失败!:fu:"%name)
			if self.retryPrompt(u"执行操作失败,是否重试?"):
				self.process(name, functor, args)
			return
		else:
			ret = Inst.postToSlack(u"[%s], 成功!:metal:"%name)
			self.retryPrompt(u"执行成功", wx.OK)

	def create(self, data, container):
		self.data = data
		self.container = container
		self.panel = None

		# wx.StaticText(self.panel, -1, self.data.desc, (10, 10))

		self.root = wx.Panel( self.container, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.root.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		bSizer = wx.BoxSizer( wx.VERTICAL )

		if getattr(self.data, "needTarget", False):
			res = xrc.XmlResource("pages/target.xrc")
			self.targetPanel = res.LoadPanel(self.root, "root")
			setupTargetData(self.targetPanel, self.onSelectTarget, self.onSelectTarget)

			bSizer.Add(self.targetPanel, 0, wx.ALL|wx.EXPAND, 5)

			# line = wx.StaticLine( self.root, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
			# bSizer.Add(line, 0, wx.ALL|wx.EXPAND, 5)

		res = xrc.XmlResource("pages/"+self.data.pageModule+".xrc")
		if res:
			self.panel = res.LoadPanel(self.root, "root")

		if not self.panel:
			self.panel = wx.Panel(self.container)

		bSizer.Add(self.panel, 0, wx.ALL|wx.EXPAND, 5)
		self.root.SetSizer(bSizer)
		self.root.Layout()

		return self.root

	def getTargetData(self):
		return getTargetData(self.targetPanel)

	def retryPrompt(self, msg, style=wx.YES_NO):
		dlg = wx.MessageDialog(self.container, msg, u'提示',
													style
													#wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
													)
		ok = dlg.ShowModal() == wx.ID_YES
		dlg.Destroy()
		return ok

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

		self.localConfig = self.loadConfig("local_config.json")
		launcherInit(self)

#------------------launcher config----------------------------
	def platform(self):
		return [i['name'] for i in self.config['platform']]

	def os(self):
		return [i['name'] for i in self.config['os']]

	def loadConfig(self, path):
		if not os.path.exists(path):
			return None
		f=codecs.open(path, 'r', 'utf8')
		return json.load(f, strict=False)

	def dataPath(self, PL, OS):
		if not self.localConfig:
			return None

		root = self.localConfig['dataRoot']
		return "%s/%s/%s/debug/launcher.json" % (root, PL, OS)

	def dataDir(self, PL, OS):
		if not self.localConfig:
			return None

		root = self.localConfig['dataRoot']
		return "%s/%s/%s/debug" % (root, PL, OS)

	def getData(self, PL, OS):
		path = self.dataPath(PL, OS)
		if not path:
			return None

		resp = requests.get(path)
		if not resp.ok:
			print(resp.status_code)
			return None
		return resp.json()

	def saveData(self, PL, OS, data):
		if not self.loadConfig:
			return False
		path = "%s/%s/debug" % (PL, OS)
		scpCfg = self.localConfig['scp']
		if not scpCfg:
			return False

		try:
			f=codecs.open("launcher.json", 'w', 'utf-8')
			json.dump(data, f, sort_keys = True, indent = 4, ensure_ascii=False)
			f.close()
		except:
			return False

		cmd = SCP % (scpCfg['port'], scpCfg['ppk'], scpCfg['username'], scpCfg['url'], path)
		return os.system(cmd) == 0

#----------------------------common--------------------------------
	def postLog(self, data):
		if not self.localConfig:
			return False
		data['type'] = "PLBOX"
		resp = requests.post(self.localConfig['logSrv'], data="data="+json.dumps(data), headers=headers)
		return resp.ok

	def postToSlack(self, data):
		if not self.localConfig or not self.localConfig['slack']:
			return False
		cfg = self.localConfig['slack']
		url = "https://slack.com/api/chat.postMessage"
		params = {'channel':cfg['channel'], 'text':'*'+data+'*', 'username':cfg['username'],\
					'token':cfg['token'], }
		resp = requests.post(url, data=params, verify=False)
		print(resp)
		return resp.ok

def init(path):
	global Inst
	Inst = Mgr(path)
