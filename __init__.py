bl_info = {
    "name": "mdx_tools",
    "author": "Warden",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Warcraft 3: Reforged mdx import/export tools",
    "wiki_url": "https://github.com/Warden0317/mdx_tools/blob/master/README.md",
    "tracker_url": "https://github.com/Warden0317/mdx_tools/issues",
    "category": "Import-Export",
    }

import bpy
from bpy.props import StringProperty
from bpy.props import IntProperty
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
from . import mdl

def loadarmature(armature, bones, pivotpoints):
    ms2fps = bpy.context.scene.render.fps / 1000
    for index,b in enumerate(armature.pose.bones):
        bone = mdl.Bone()
        bone.ObjectId = index
        bone.Name = b.name
        if b.parent:
            bone.ParentName = b.parent.name
        bones.append(bone)

        pivotpoints.Location.append(list(armature.matrix_world @ b.bone.head_local))
        # pivotpoints.Location.append(list(b.bone.head_local))

    for bone in bones:
        if bone.ParentName:
            bone.Parent = list(filter(lambda b: b.Name == bone.ParentName, bones))[0].ObjectId

    if armature.animation_data:
        fcurves = armature.animation_data.action.fcurves
        for fcurve in fcurves:
            if(len(fcurve.data_path.split('"'))==3):
                bonename = fcurve.data_path.split('"')[1]
                bone = list(filter(lambda b: b.Name == bonename, bones))[0]
                if fcurve.data_path.split('.')[-1] == 'location':
                    for keyframe in fcurve.keyframe_points:
                        if str(round(keyframe.co[0]/ms2fps)) not in bone.Translation:
                            bone.Translation[str(round(keyframe.co[0]/ms2fps))] = [0,0,0]
                        if fcurve.array_index == 0:
                            bone.Translation[str(round(keyframe.co[0]/ms2fps))][0] = keyframe.co[1]*20
                        elif fcurve.array_index == 1:
                            bone.Translation[str(round(keyframe.co[0]/ms2fps))][2] = keyframe.co[1]*20
                        else:
                            bone.Translation[str(round(keyframe.co[0]/ms2fps))][1] = -keyframe.co[1]*20
                elif fcurve.data_path.split('.')[-1] == 'rotation_quaternion':
                    for keyframe in fcurve.keyframe_points:
                        if str(round(keyframe.co[0]/ms2fps)) not in bone.Rotation:
                            bone.Rotation[str(round(keyframe.co[0]/ms2fps))] = [0,0,0,0]
                        if fcurve.array_index == 0:
                            bone.Rotation[str(round(keyframe.co[0]/ms2fps))][3] = keyframe.co[1]
                        elif fcurve.array_index == 1:
                            bone.Rotation[str(round(keyframe.co[0]/ms2fps))][0] = keyframe.co[1]
                        elif fcurve.array_index == 2:
                            bone.Rotation[str(round(keyframe.co[0]/ms2fps))][2] = keyframe.co[1]
                        else:
                            bone.Rotation[str(round(keyframe.co[0]/ms2fps))][1] = -keyframe.co[1]
                elif fcurve.data_path.split('.')[-1] == 'scale':
                    for keyframe in fcurve.keyframe_points:
                        if str(round(keyframe.co[0]/ms2fps)) not in bone.Scaling:
                            bone.Scaling[str(round(keyframe.co[0]/ms2fps))] = [0,0,0]
                        if fcurve.array_index == 0:
                            bone.Scaling[str(round(keyframe.co[0]/ms2fps))][0] = keyframe.co[1]
                        if fcurve.array_index == 1:
                            bone.Scaling[str(round(keyframe.co[0]/ms2fps))][2] = keyframe.co[1]
                        else:
                            bone.Scaling[str(round(keyframe.co[0]/ms2fps))][1] = -keyframe.co[1]

class Classic_MDL_import(bpy.types.Operator, ImportHelper):
    bl_idname = "classicmdl.import"
    bl_label = "Import mdl"

    filter_glob : StringProperty(
        default="*.mdl",
        options={'HIDDEN'},
    )

    def execute(self, context):
        print("Import", self.properties.filepath)

        file = open(self.properties.filepath, 'r')

        version = mdl.Version()
        model = mdl.Model()
        sequences = mdl.Sequences()
        texture = mdl.Textures()
        material = mdl.Materials()
        geosets = []
        bones = []
        pivotpoints = mdl.PivotPoints()

        line = file.readline()
        while line:
            label,*parameter = line.split(" ")
            if label == "Version":
                version.read(file)
            elif label == "Model":
                model.read(file,parameter[0])
            elif label == "Sequences":
                sequences.read(file)
            elif label == "Textures":
                texture.read(file)
            elif label == "Materials":
                material.read(file)
            elif label == "Geoset":
                geoset = mdl.Geoset()
                geoset.read(file)
                geosets.append(geoset)
            elif label == "Bone":
                bone = mdl.Bone()
                bone.read(file,parameter[0])
                bones.append(bone)
            elif label == "PivotPoints":
                pivotpoints.read(file,parameter[0])
            else:
                i = 0
                while file.readline()[0:1] != '}':
                    i = i + 1
            line = file.readline()

        armature = bpy.data.armatures.new(name="Armature")
        action = bpy.data.actions.new(name="action")

        ms2fps = bpy.context.scene.render.fps / 1000

        armatureObject = bpy.data.objects.new("Armature", armature)
        armatureObject.location = bpy.context.scene.cursor.location
        bpy.context.scene.collection.objects.link(armatureObject)
        bpy.context.scene.view_layers[0].objects.active = armatureObject

        armatureObject.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')

        editBones = []
        for index,bone in enumerate(bones):
            editBone = armature.edit_bones.new(bone.Name)
            editBone.head = (pivotpoints.Location[index][0],pivotpoints.Location[index][1],pivotpoints.Location[index][2])
            editBone.tail = (pivotpoints.Location[index][0],pivotpoints.Location[index][1],pivotpoints.Location[index][2]+0.5)
            editBones.append(editBone)

            if(bone.Translation):
                datapath = 'pose.bones["' + bone.Name + '"].location'
                for i in range(3):
                    if i == 0:
                        fcurve = action.fcurves.new(datapath,index = 0,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Translation))
                        j = 0
                        for k,v in bone.Translation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[0]/20)
                            j += 1
                    elif i == 1:
                        fcurve = action.fcurves.new(datapath,index = 1,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Translation))
                        j = 0
                        for k,v in bone.Translation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[2]/20)
                            j += 1
                    else:
                        fcurve  = action.fcurves.new(datapath,index = 2,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Translation))
                        j = 0
                        for k,v in bone.Translation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,-v[1]/20)
                            j += 1
                        
            if(bone.Rotation):
                datapath = 'pose.bones["' + bone.Name + '"].rotation_quaternion'
                for i in range(4):
                    if i == 0:
                        fcurve  = action.fcurves.new(datapath,index = 0,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Rotation))
                        j = 0
                        for k,v in bone.Rotation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[3])
                            j += 1
                    elif i == 1:
                        fcurve  = action.fcurves.new(datapath,index = 1,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Rotation))
                        j = 0
                        for k,v in bone.Rotation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[0])
                            j += 1
                    elif i == 2:
                        fcurve  = action.fcurves.new(datapath,index = 2,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Rotation))
                        j = 0
                        for k,v in bone.Rotation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[2])
                            j += 1
                    else:
                        fcurve  = action.fcurves.new(datapath,index = 3,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Rotation))
                        j = 0
                        for k,v in bone.Rotation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,-v[1])
                            j += 1

            if(bone.Scaling):
                datapath = 'pose.bones["' + bone.Name + '"].scale'
                for i in range(3):
                    if i == 0:
                        fcurve  = action.fcurves.new(datapath,index = 0,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Scaling))
                        j = 0
                        for k,v in bone.Scaling.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[0])
                            j += 1
                    elif i == 1:
                        fcurve  = action.fcurves.new(datapath,index = 1,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Scaling))
                        j = 0
                        for k,v in bone.Scaling.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[2])
                            j += 1
                    else:
                        fcurve  = action.fcurves.new(datapath,index = 2,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Scaling))
                        j = 0
                        for k,v in bone.Scaling.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,-v[1])
                            j += 1
            
        for index,bone in enumerate(bones):
            if bone.Parent != -1:
                editBones[index].parent = editBones[bone.Parent]

        armatureObject.animation_data_create()
        armatureObject.animation_data.action = action

        for index,geoset in enumerate(geosets):
            mesh = bpy.data.meshes.new(geoset.Name)
            mesh.from_pydata(geoset.Vertices, [], geoset.Faces)
            for index2,vertex in enumerate(mesh.vertices):
                vertex.normal = geoset.Normals[index2]
                
            uvLayer = mesh.uv_layers.new()
            vi_uv = {i: (u, 1.0 - v) for i, (u, v) in enumerate(geoset.TVertices)}
            per_loop_list = [0.0] * len(mesh.loops)
            for loop in mesh.loops:
                per_loop_list[loop.index] = vi_uv[loop.vertex_index]
            per_loop_list = [uv for pair in per_loop_list for uv in pair]
            uvLayer.data.foreach_set('uv',per_loop_list)

            meshObject = bpy.data.objects.new(geoset.Name, mesh)

            vertexGroups = []

            for i in range(len(bones)):
                vertexGroup = meshObject.vertex_groups.new(name = bones[i].Name)
                vertexGroups.append(vertexGroup)
            for vertexIndex in range(len(geoset.VertexGroup)):
                GroupIndex = geoset.VertexGroup[vertexIndex]
                Groupcount = len(geoset.Groups[GroupIndex])
                if(Groupcount == 1):
                    vertexGroups[geoset.Groups[GroupIndex][0]].add([vertexIndex],1,'REPLACE')
                elif(Groupcount == 2):
                    vertexGroups[geoset.Groups[GroupIndex][0]].add([vertexIndex],0.5,'REPLACE')
                    vertexGroups[geoset.Groups[GroupIndex][1]].add([vertexIndex],0.5,'REPLACE')
                elif(Groupcount == 3):
                    vertexGroups[geoset.Groups[GroupIndex][0]].add([vertexIndex],0.333333,'REPLACE')
                    vertexGroups[geoset.Groups[GroupIndex][1]].add([vertexIndex],0.333333,'REPLACE')
                    vertexGroups[geoset.Groups[GroupIndex][2]].add([vertexIndex],0.333333,'REPLACE')
                else:
                    vertexGroups[geoset.Groups[GroupIndex][0]].add([vertexIndex],0.25,'REPLACE')
                    vertexGroups[geoset.Groups[GroupIndex][1]].add([vertexIndex],0.25,'REPLACE')
                    vertexGroups[geoset.Groups[GroupIndex][2]].add([vertexIndex],0.25,'REPLACE')
                    vertexGroups[geoset.Groups[GroupIndex][3]].add([vertexIndex],0.25,'REPLACE')
            modifier = meshObject.modifiers.new('UseArmature', 'ARMATURE')
            modifier.object = armatureObject
            modifier.use_bone_envelopes = False
            modifier.use_vertex_groups = True
            bpy.context.scene.collection.objects.link(meshObject)
        return {'FINISHED'}

class Reforged_MDL_import(bpy.types.Operator, ImportHelper):
    bl_idname = "reforgedmdl.import"
    bl_label = "Import mdl"
    filter_glob : StringProperty(
        default="*.mdl",
        options={'HIDDEN'},
    )

    LOD : IntProperty(
        description="LevelOfDetail", 
        name="LOD",
        default = 0, 
        min = 0,
        max = 3,
        step = 1,
    )
    
    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text = 'LOD')
        col.prop(self, 'LOD')
    
    def execute(self, context):
        print("Import", self.properties.filepath)

        file = open(self.properties.filepath, 'r')

        version = mdl.Version()
        model = mdl.Model()
        sequences = mdl.Sequences()
        texture = mdl.Textures()
        material = mdl.Materials()
        geosets = []
        bones = []
        line = file.readline()
        while line:
            label,*parameter = line.split(" ")
            if label == "Version":
                version.read(file)
            elif label == "Model":
                model.read(file,parameter[0])
            elif label == "Sequences":
                sequences.read(file)
            elif label == "Textures":
                texture.read(file)
            elif label == "Materials":
                material.read(file)
            elif label == "Geoset":
                geoset = mdl.Geoset()
                geoset.read(file)
                geosets.append(geoset)
            elif label == "Bone":
                bone = mdl.Bone()
                bone.read(file,parameter[0])
                bones.append(bone)
            elif label == "PivotPoints":
                pivotpoints = mdl.PivotPoints()
                pivotpoints.read(file,parameter[0])
            else:
                i = 0
                while file.readline()[0:1] != '}':
                    i = i + 1
            line = file.readline()

        armature = bpy.data.armatures.new(name="Armature")
        action = bpy.data.actions.new(name="action")

        ms2fps = bpy.context.scene.render.fps / 1000

        armatureObject = bpy.data.objects.new("Armature", armature)
        armatureObject.location = bpy.context.scene.cursor.location
        bpy.context.scene.collection.objects.link(armatureObject)
        bpy.context.scene.view_layers[0].objects.active = armatureObject
        armatureObject.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        editBones = []
        for index,bone in enumerate(bones):
            editBone = armature.edit_bones.new(bone.Name)
            editBone.head = (pivotpoints.Location[index][0],pivotpoints.Location[index][1],pivotpoints.Location[index][2])
            editBone.tail = (pivotpoints.Location[index][0],pivotpoints.Location[index][1],pivotpoints.Location[index][2]+0.5)
            editBones.append(editBone)
            if(bone.Translation):
                datapath = 'pose.bones["' + bone.Name + '"].location'
                for i in range(3):
                    if i == 0:
                        fcurve = action.fcurves.new(datapath,index = 0,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Translation))
                        j = 0
                        for k,v in bone.Translation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[0]/20)
                            j += 1
                    elif i == 1:
                        fcurve = action.fcurves.new(datapath,index = 1,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Translation))
                        j = 0
                        for k,v in bone.Translation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[2]/20)
                            j += 1
                    else:
                        fcurve  = action.fcurves.new(datapath,index = 2,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Translation))
                        j = 0
                        for k,v in bone.Translation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,-v[1]/20)
                            j += 1
                        
            if(bone.Rotation):
                datapath = 'pose.bones["' + bone.Name + '"].rotation_quaternion'
                for i in range(4):
                    if i == 0:
                        fcurve  = action.fcurves.new(datapath,index = 0,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Rotation))
                        j = 0
                        for k,v in bone.Rotation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[3])
                            j += 1
                    elif i == 1:
                        fcurve  = action.fcurves.new(datapath,index = 1,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Rotation))
                        j = 0
                        for k,v in bone.Rotation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[0])
                            j += 1
                    elif i == 2:
                        fcurve  = action.fcurves.new(datapath,index = 2,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Rotation))
                        j = 0
                        for k,v in bone.Rotation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[2])
                            j += 1
                    else:
                        fcurve  = action.fcurves.new(datapath,index = 3,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Rotation))
                        j = 0
                        for k,v in bone.Rotation.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,-v[1])
                            j += 1

            if(bone.Scaling):
                datapath = 'pose.bones["' + bone.Name + '"].scale'
                for i in range(3):
                    if i == 0:
                        fcurve  = action.fcurves.new(datapath,index = 0,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Scaling))
                        j = 0
                        for k,v in bone.Scaling.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[0])
                            j += 1
                    elif i == 1:
                        fcurve  = action.fcurves.new(datapath,index = 1,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Scaling))
                        j = 0
                        for k,v in bone.Scaling.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,v[2])
                            j += 1
                    else:
                        fcurve  = action.fcurves.new(datapath,index = 2,action_group = bone.Name)
                        fcurve.keyframe_points.add(count = len(bone.Scaling))
                        j = 0
                        for k,v in bone.Scaling.items():
                            fcurve.keyframe_points[j].co = (int(k)*ms2fps,-v[1])
                            j += 1
        for index,bone in enumerate(bones):
            if bone.Parent != -1:
                editBones[index].parent = editBones[bone.Parent]
        
        armatureObject.animation_data_create()
        armatureObject.animation_data.action = action


        for index,geoset in enumerate(geosets):
            if(geoset.LevelOfDetail == 0):
                mesh = bpy.data.meshes.new(geoset.Name)
                mesh.from_pydata(geoset.Vertices, [], geoset.Faces)
                for index2,vertex in enumerate(mesh.vertices):
                    vertex.normal = geoset.Normals[index2]
                
                uvLayer = mesh.uv_layers.new()
                vi_uv = {i: (u, 1.0 - v) for i, (u, v) in enumerate(geoset.TVertices)}
                per_loop_list = [0.0] * len(mesh.loops)
                for loop in mesh.loops:
                    per_loop_list[loop.index] = vi_uv[loop.vertex_index]
                per_loop_list = [uv for pair in per_loop_list for uv in pair]
                uvLayer.data.foreach_set('uv',per_loop_list)

                meshObject = bpy.data.objects.new(geoset.Name, mesh)

                vertexGroups = []

                for i in range(len(bones)):
                    vertexGroup = meshObject.vertex_groups.new(name = bones[i].Name)
                    vertexGroups.append(vertexGroup)
                for vertexIndex in range(len(geoset.SkinWeights)):
                    for i in range(4):
                        if int(geoset.SkinWeights[vertexIndex][i+4]) != 0:
                            vertexGroups[int(geoset.SkinWeights[vertexIndex][i])].add([vertexIndex],float(geoset.SkinWeights[vertexIndex][i+4])/255.0, 'REPLACE')
                modifier = meshObject.modifiers.new('UseArmature', 'ARMATURE')
                modifier.object = armatureObject
                modifier.use_bone_envelopes = False
                modifier.use_vertex_groups = True
                bpy.context.scene.collection.objects.link(meshObject)

        return {'FINISHED'}

class Classic_MDL_export(bpy.types.Operator, ExportHelper):
    bl_idname = "classicmdl.export"
    bl_label = "Export mdl"
    filename_ext = ".mdl"

    filter_glob : StringProperty(default="*.mdl", options={'HIDDEN'})

    def execute(self, context):
        print("Export", self.properties.filepath)

        

        version = mdl.Version()
        model = mdl.Model()
        texture = mdl.Textures()
        material = mdl.Materials()
        geosets = []
        bones = []
        pivotpoints = mdl.PivotPoints()
        meshcount = 0

        file = open(self.properties.filepath, 'w')
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                # depsgraph = context.evaluated_depsgraph_get()
                # mesh =  bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph), preserve_all_data_layers=True, depsgraph=depsgraph)
                mesh = obj.data
                mesh.transform(obj.matrix_world)
                geoset = mdl.Geoset()
                mesh.calc_loop_triangles()

                armature = None
                for modifier in obj.modifiers:
                    if modifier.type == 'ARMATURE' and modifier.use_vertex_groups:
                        armature = modifier.object

                if armature is not None:
                    loadarmature(armature,bones,pivotpoints)
                    
                #     bone_names = set(b.name for b in armature.object.data.bones)

                for vertex in mesh.vertices:
                    geoset.Vertices.append([vertex.co[0]*20,vertex.co[1]*20,vertex.co[2]*20])
                    geoset.Normals.append([vertex.normal[0],vertex.normal[1],vertex.normal[2]])
                    
                    vgroups = sorted(vertex.groups[:], key=lambda x:x.weight, reverse=True)
                    if len(vgroups):
                        group = list(list(filter(lambda b: b.Name == obj.vertex_groups[vg.group].name, bones))[0].ObjectId for vg in vgroups if vg.weight > 0.25)[:3]
                    if group not in geoset.Groups:
                        geoset.Groups.append(group)
                    
                    geoset.VertexGroup.append(geoset.Groups.index(group))
                for group in geoset.Groups:
                    for g in group:
                        bones[g].GeosetId = meshcount
                geoset.TVertices = [[0.0,0.0]] * len(geoset.Vertices)
                for tri in mesh.loop_triangles:
                    geoset.Faces.append((tri.vertices[0],tri.vertices[1],tri.vertices[2]))
                    for i in range(3):
                        geoset.TVertices[mesh.loops[tri.loops[i]].vertex_index] = [mesh.uv_layers.active.data[tri.loops[i]].uv[0],1 - mesh.uv_layers.active.data[tri.loops[i]].uv[1]]
                geosets.append(geoset)
                meshcount += 1

        version.FormatVersion = 800
        model.Name = "test"
        model.NumGeosets = meshcount
        model.BlendTime = 150
        model.NumBones = len(bones)

        version.write(file)
        model.write(file)
        texture.write(file)
        material.write(file)
        for geoset in geosets:
            geoset.write(file)
        for bone in bones:
            bone.write(file)
        pivotpoints.write(file)
        return {'FINISHED'}



class Reforged_MDL_export(bpy.types.Operator, ExportHelper):
    bl_idname = "reforgedmdl.export"
    bl_label = "Export mdl"
    filename_ext = ".mdl"

    filter_glob : StringProperty(default="*.mdl", options={'HIDDEN'})

    def execute(self, context):
        print("Export", self.properties.filepath)

        version = mdl.Version()
        model = mdl.Model()
        texture = mdl.Textures()
        material = mdl.Materials()
        geosets = []
        bones = []
        pivotpoints = mdl.PivotPoints()
        meshcount = 0

        file = open(self.properties.filepath, 'w')
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                # depsgraph = context.evaluated_depsgraph_get()
                # mesh =  bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph), preserve_all_data_layers=True, depsgraph=depsgraph)
                mesh = obj.data
                geoset = mdl.Geoset()
                mesh.calc_loop_triangles()
                mesh.calc_tangents()


                armature = None
                for modifier in obj.modifiers:
                    if modifier.type == 'ARMATURE' and modifier.use_vertex_groups:
                        armature = modifier.object

                if armature is not None:
                    loadarmature(armature,bones,pivotpoints)
                
                for vertex in mesh.vertices:
                    geoset.Vertices.append([vertex.co[0]*20,vertex.co[1]*20,vertex.co[2]*20])
                    geoset.Normals.append([vertex.normal[0],vertex.normal[1],vertex.normal[2]])
                    

                    vgroups = sorted(vertex.groups[:], key=lambda x:x.weight, reverse=True)[:4]
                    skin = list(list(filter(lambda b: b.Name == obj.vertex_groups[vg.group].name, bones))[0].ObjectId for vg in vgroups)
                    weight = list(vg.weight*255 for vg in vgroups)
                    geoset.SkinWeights.append(skin + [0] * (4-len(skin)) + weight + [0] * (4-len(weight)))

                    # vgroups = sorted(vertex.groups[:], key=lambda x:x.weight, reverse=True)
                    # if len(vgroups):
                    #     group = list(list(filter(lambda b: b.Name == obj.vertex_groups[vg.group].name, bones))[0].ObjectId for vg in vgroups if vg.weight > 0.25)[:3]
                    # if group not in geoset.Groups:
                    #     geoset.Groups.append(group)
                    
                    # geoset.VertexGroup.append(geoset.Groups.index(group))
                
                geoset.TVertices = [[0.0,0.0]] * len(geoset.Vertices)
                geoset.Tangents = [[0.0,0.0,0.0]] * len(geoset.Vertices)
                for tri in mesh.loop_triangles:
                    geoset.Faces.append((tri.vertices[0],tri.vertices[1],tri.vertices[2]))
                    for i in range(3):
                        geoset.Tangents[mesh.loops[tri.loops[i]].vertex_index] = list(mesh.loops[tri.loops[i]].tangent)
                        geoset.TVertices[mesh.loops[tri.loops[i]].vertex_index] = [mesh.uv_layers.active.data[tri.loops[i]].uv[0],1 - mesh.uv_layers.active.data[tri.loops[i]].uv[1]]
                for i in range(len(bones)):
                    geoset.Groups.append([i])
                geosets.append(geoset)
                meshcount += 1
        
        version.FormatVersion = 1000
        model.Name = "test"
        model.NumGeosets = meshcount
        model.BlendTime = 150
        model.NumBones = len(bones)

        version.write(file)
        model.write(file)
        texture.write(file)
        material.write(file)
        for geoset in geosets:
            geoset.write(file)
        for bone in bones:
            bone.write(file)
        pivotpoints.write(file)
        return {'FINISHED'}


classes = {
    Classic_MDL_import,
    Reforged_MDL_import,
    Classic_MDL_export,
    Reforged_MDL_export,
}

def classic_mdl_import(self, context):
    self.layout.operator("classicmdl.import", text="War3 Classic mdl (.mdl)")

def reforged_mdl_import(self, context):
    self.layout.operator("reforgedmdl.import", text="War3 Reforged mdl (.mdl)")

def classic_mdl_export(self, context):
    self.layout.operator("classicmdl.export", text="War3 Classic mdl (.mdl)")

def reforged_mdl_export(self, context):
    self.layout.operator("reforgedmdl.export", text="War3 Reforged mdl (.mdl)")

def register():
    for c in classes: 
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file_import.append(classic_mdl_import)
    bpy.types.TOPBAR_MT_file_import.append(reforged_mdl_import)
    bpy.types.TOPBAR_MT_file_export.append(classic_mdl_export)
    bpy.types.TOPBAR_MT_file_export.append(reforged_mdl_export)

def unregister():
    for c in classes: 
        bpy.utils.unregister_class(c)
    bpy.types.TOPBAR_MT_file_import.remove(classic_mdl_import)
    bpy.types.TOPBAR_MT_file_import.remove(reforged_mdl_import)
    bpy.types.TOPBAR_MT_file_export.remove(classic_mdl_export)
    bpy.types.TOPBAR_MT_file_export.remove(reforged_mdl_export)

if __name__ == "__main__":
    register()
