import os
import NodegraphAPI
from Katana import KatanaFile
from Katana import RenderManager

def getRenderNodes():
    renderNodeDict = {}
    for n in NodegraphAPI.GetAllNodesByType('Render'):
        renderNodeDict[n.getName()] = n
    macro = NodegraphAPI.GetNode('BatchRender')
    rNodeParam = macro.getParameter('user.render_node')
    rHints = {'widget': 'popup', 'options': renderNodeDict.keys()}
    rNodeParam.setHintString(repr(rHints))

    renderSettDict = {}
    for s in NodegraphAPI.GetAllNodesByType('RenderSettings'):
        renderSettDict[s.getName()] = s
    macro = NodegraphAPI.GetNode('BatchRender')
    rSettParam = macro.getParameter('user.settings_node')
    sHints = {'widget': 'popup', 'options': renderSettDict.keys()}
    rSettParam.setHintString(repr(sHints))

getRenderNodes()
