import os
import NodegraphAPI
from Katana import KatanaFile
from Katana import RenderManager
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton

# style sheet for progress bar
UI_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: right
}

QProgressBar::chunk {
    background-color: green;
    width: 10px;
    margin: 1px
}

"""

# class for progress bar visual feedback
class ProgressBar(QWidget):
    def UI(self):
        self.setWindowTitle('Rendering')
        self.resize(500, 100)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(25, 30, 450, 40)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setStyleSheet(UI_STYLE)

        self.show()

    def Increase_Step(self, val):
        self.progressBar.setValue(self.progressBar.value() + val)

# output in render log
def messageHandler( sequenceID, message ):
  print message

# getting project frame range
def frameRange():
    macro = NodegraphAPI.GetNode('BatchRender')
    frame_in =  int(macro.getParameter('user.frame_range.i0').getValue(0))
    frame_out =  int(macro.getParameter('user.frame_range.i1').getValue(0))
    c_range = range(frame_in, frame_out+1)
    return c_range

# render function
def batchRender():
    RenderNode = NodegraphAPI.GetNode('BatchRender').getParameter('user.render_node').getValue(0)
    renderSettingsNode = NodegraphAPI.GetNode('BatchRender').getParameter('user.settings_node').getValue(0)

    range = frameRange()
    #root = NodegraphAPI.GetRootNode()

    renderSettings = RenderManager.RenderingSettings()
    renderSettings.mode=RenderManager.RenderModes.DISK_RENDER
    renderSettings.asynchRenderMessageCB=messageHandler
    renderSettings.asynch=False

    res = NodegraphAPI.GetNode('BatchRender').getParameter('user.resolution').getValue(0)
    NodegraphAPI.GetNode(str(renderSettingsNode)).getParameter('args.renderSettings.resolution.value').setValue(str(res),0)

    demo = ProgressBar()
    demo.UI()
    val = 100/range[-1]

    for frame in range:
        demo.Increase_Step(val)
        print '-' * 80
        print '\nRendering Node "%s" frame %s...' % (RenderNode, frame)
        renderSettings.frame = frame
        RenderManager.StartRender('diskRender', node=NodegraphAPI.GetNode(RenderNode), settings=renderSettings)


batchRender()
