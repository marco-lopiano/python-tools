import maya.cmds as cmds
import os

def openLastScene():
       # setting up progect directory
       cmds.SetProject()

       # gathering scene info
       projDir = cmds.workspace(q=True, rd=True)
       scenes = []
       if 'scene' in cmds.workspace(q=True, frl=True):
              sceneDirectory = os.path.join(projDir, cmds.workspace(fre='scene'))
              for scene in os.listdir(sceneDirectory):
                  if '.ma' in scene or '.mb' in scene:
                      scenes.append(scene)

       latest = scenes[-1]
       openDir = sceneDirectory + '/' + latest

       # open last scene found
       cmds.file(new=True, force=True)
       cmds.file(openDir, open=True)

