import NodegraphAPI
import re
import os
import converter
from PyQt5.QtWidgets import QFileDialog

'''
Texture naming convention
@@@     assetName_optionalInfo_mapType.extension     @@@
'''

class TextToMat(object):

    def call_for_directory(self):
        self.directory = QFileDialog.getExistingDirectory()
        return self.directory

    def checkForConversion(self):
        pass

    def check_type(self, texture):
        outputs = []
        if 'diffuse' in texture.lower():
            outputs = ['baseColor', 'RGB']
        elif 'height' in texture.lower():
            outputs = ['bumpMapping', 'R']
        elif 'metallic' in texture.lower():
            outputs = ['metallic', 'R']
        elif 'roughness' in texture.lower():
            outputs = ['roughness', 'R']
        elif 'normal' in texture.lower():
            outputs = ['bumpNormal', 'RGB']
        elif 'specular' in texture.lower():
            outputs = ['specular', 'R']
        else:
            return False
        return outputs

    def group_by_name(self, directory):
        dir_content = os.listdir(directory)
        list_of_list = []
        filters = []
        for i in dir_content:
            tmp = i.split('_')[0]
            if tmp not in filters:
                filters.append(tmp)
        for f in filters:
            sub_list = [i for i in dir_content if f in i]
            list_of_list.append(sub_list)
        return list_of_list


    def create_shader_from_textures(self):
        texture_dir = self.call_for_directory()
        textures = self.group_by_name(texture_dir)

        shader_group_list = []
        for texture_list in textures:
            # create group
            groupNode = NodegraphAPI.CreateNode('Group', NodegraphAPI.GetRootNode())

            # create shader
            shader = NodegraphAPI.CreateNode('PrmanShadingNode', groupNode)
            shader.getParameter('nodeType').setValue('PxrDisney',0)
            NodegraphAPI.SetNodePosition(shader, (150,-100))

            #create network
            network = NodegraphAPI.CreateNode('NetworkMaterial', groupNode)
            network.addInputPort('prmanBxdf')
            NodegraphAPI.SetNodePosition(network, (150,-200))

            # connect shader to network
            shader_port = shader.getOutputPorts()[0]
            network_port = network.getInputPorts()[0]
            shader_port.connect(network_port)

            #connect netwotk to out group
            network_out = network.getOutputPorts()[0]
            tmp_dot = NodegraphAPI.CreateNode('Dot', NodegraphAPI.GetRootNode())
            tmp_dot_in = tmp_dot.getInputPorts()[0]
            network_out.connect(tmp_dot_in)
            tmp_dot.delete()

            # create textures
            x, y = 0, 0
            for text in texture_list:

                master_name = text.split('_')[0]

                # setting group, network and shader node name
                groupNode.setName('{}_MAT'.format(master_name))
                network.getParameter('name').setValue('{}_network_material'.format(master_name),0)
                shader.getParameter('name').setValue('{}_shader'.format(master_name),0)

                shader_group_list.append(groupNode)

                texture_node = NodegraphAPI.CreateNode('PrmanShadingNode', groupNode)
                NodegraphAPI.SetNodePosition(texture_node, (x,y))

                texture_node.getParameter('nodeType').setValue('PxrTexture', 0)
                texture_node.checkDynamicParameters()
                shader.checkDynamicParameters()

                # set texture path
                full_path = str(os.path.normpath(os.path.join(texture_dir, text)))
                texture_node.getParameter('parameters.filename.value').setValue(full_path, 0)
                texture_node.getParameter('parameters.filename.enable').setValue(float(True), 0)

                # set node name
                last = self.check_type(text)[0]
                node_name = 'texture_{}_{}'.format(master_name, last)
                texture_node.getParameter('name').setValue(node_name, 0)

                port_to, port_from = self.check_type(text)
                filter_text = re.compile("^{}$".format(port_from))
                filter_shader = re.compile("^{}$".format(port_to))

                try:
                    texture_port = [t for t in texture_node.getOutputPorts() if filter_text.match( t.getName().replace('result', ''))][0]
                    shader_port = [s for s in shader.getInputPorts() if filter_shader.match(s.getName())][0]
                    texture_port.connect(shader_port)
                except:
                    pass

                x+=200

            pos_x = 0
            for mat in shader_group_list:
                NodegraphAPI.SetNodePosition(mat, (pos_x*50, 0))
                pos_x += 1
