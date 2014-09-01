
import wx
import mgr

mgr.init("config.json")

#----------------------------------------------------------------------------

class Books(wx.Choicebook):
    def __init__(self, parent, id, log):
        wx.Choicebook.__init__(self, parent, id)
        self.log = log

        # Now make a bunch of panels for the choice book
        count = 1
        for tool in mgr.Inst.tools:
            win = wx.Panel(self)
            self.AddPage(win, tool.name)
            tool.createPage(win)

        self.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGING, self.OnPageChanging)


    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

#----------------------------------------------------------------------------

def runTest(frame, nb, log):
    testWin = Books(nb, -1, log)
    return testWin

#----------------------------------------------------------------------------

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])



