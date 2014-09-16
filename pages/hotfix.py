# -*- coding: utf-8 -*-

import os
import wx
import mgr
import svn
import hashlib
import  wx.lib.filebrowsebutton as filebrowse

import MakePatch

SHUTDOWN = 0
NORMAL = 1

def get_file_md5(path):
	f = open(path, 'rb')
	checksum = hashlib.md5(f.read()).hexdigest()
	f.close()
	return checksum

class hotfix(mgr.Page):
	def __init__(self):
		self.targetDir = None

	def create(self, panel, data):
		root = super(hotfix, self).create(panel, data)

		panel = self.panel

		ok_btn = wx.FindWindowByName("m_ok_btn", panel)
		panel.Bind(wx.EVT_BUTTON, self.onOkBtn, ok_btn)

		return root

	def preCreate(self, sizer):
		dirSizer = wx.StaticBoxSizer( wx.StaticBox( self.root, wx.ID_ANY, u"工作路径" ), wx.HORIZONTAL )

		self.dbb = filebrowse.DirBrowseButton(
				self.root, -1, size=(-1, -1), changeCallback = self.dbbCallback
		)
		dirSizer.Add(self.dbb, 1, wx.ALL|wx.EXPAND, 5 )

		sizer.Add(dirSizer, 0, wx.ALL|wx.EXPAND, 5)

	def dbbCallback(self, evt):
		targetDir = self.dbb.GetValue()
		if targetDir and targetDir.endswith("\\tech"):
			self.targetDir = targetDir
			self.versionFile = "%s\\rawres\\script\\PL\\version\\script_version.lua"%self.targetDir
			self.resFile = "%s\\..\\pili\\res_bin\\"%self.targetDir
			self.packTool = "%s\\..\\pili\\pack_script.bat"%self.targetDir
			self.scriptBin = "%s\\..\\pili\\script_bin\\script.script"%self.targetDir

			if not os.path.exists(self.versionFile) or not os.path.exists(self.resFile):
				self.targetDir = None
		else:
			self.targetDir = None
		if not self.targetDir:
			self.versionFile, self.resFile = None, None

	def onSelectTarget(self, pl_name, os_name):
		self.refresh()

	def onOkBtn(self, evt):
		if not self.targetDir or not self.targetdata:
			return
		pl_name, os_name = self.getTargetData()
		if not pl_name or not os_name:
			return

		self.process(u"制作热更新<platform:%s, os:%s>"%(pl_name,os_name), \
								self.makePatch, (pl_name, os_name))

	def makePatch(self, pl_name, os_name):
		#step 1: update bin res and script version
		if not svn.update(self.resFile):
			if self.retryPrompt(u"更新svn出错，是否重试"):
				self.makePatch()
			return "svn up res files failed"
		if not svn.update(self.versionFile):
			if self.retryPrompt(u"更新svn出错，是否重试"):
				self.makePatch()
			return "svn up versioin file failed"

		#step 2: sync scipt version to remote data,
		#plus one and pack_script.bat will plus script version one too
		current = self._read_lua_version()
		print("remote data version:%d"%self.targetdata['script_version'])
		print("current local version:%d"%current)
		self.targetdata['script_version'] = current + 1

		#step 3: pack script
		#os.system(self.packTool)

		#step 4: generate file list
		files = []
		targets = mgr.Inst.patchFiles()
		if "script.script" in targets:
			checksum = get_file_md5(self.scriptBin).decode('utf-8')
			urls = ["%s/%s" % (self.patchURLRoot, "script.script")]
			item = {"md5":checksum, "name":"script.script", "urls":urls}
			files.append(item)

		upload = [self.scriptBin]
		for tar in targets:
			if tar == "script.script":
				continue
			p = self.resFile+tar
			upload.append(p)
			checksum = get_file_md5(p).decode('utf-8')
			urls = ["%s/%s" % (self.patchURLRoot, tar)]
			item = {"md5":checksum, "name":tar, "urls":urls}
			files.append(item)
		self.targetdata["files"] = files

		#step 5: upload hotfix files
		if not mgr.Inst.uploadFiles(pl_name, os_name, upload):
			return "upload hotfix files failed"

		#step 6: upload config json file
		return mgr.Inst.saveData(pl_name, os_name, self.targetdata)

		# import json
		# import codecs
		# f = codecs.open("test.json", 'w', 'utf-8')
		# json.dump(files, f, sort_keys = True, indent = 4, ensure_ascii=False)
		# f.close()

	def refresh(self):
		pl_name, os_name = self.getTargetData()

		self.targetdata = None
		if pl_name and os_name:
			self.targetdata = mgr.Inst.getData(pl_name, os_name)
		else:
			return

		if not self.targetdata:
			if self.retryPrompt(u"加载数据出错，是否重试"):
				self.refresh()
			return
		self.patchURLRoot = mgr.Inst.dataDir(pl_name, os_name)


#----------------------hepers-------------------
	def _read_lua_version(self):
		f = open(self.versionFile, 'r')
		txt = f.read()
		f.close()
		txt = txt.strip()
		version = txt.split(" ")[-1]
		return int(version)
