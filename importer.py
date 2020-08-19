import bpy
from mathutils import (Vector,Matrix)

def ReforgedImport(model):
    armature = bpy.data.armatures.new(name="Armature")
    action = bpy.data.actions.new(name="action")

    ms2fps = bpy.context.scene.render.fps / 1000

    armatureObject = bpy.data.objects.new("Armature", armature)
    armatureObject.matrix_world = Matrix(((0.05, 0.0, 0.0, 0.0),(0.0, 0.05, 0.0, 0.0),(0.0, 0.0, 0.05, 0.0),(0.0, 0.0, 0.0, 1.0)))
    armatureObject.location = bpy.context.scene.cursor.location

    bpy.context.scene.collection.objects.link(armatureObject)
    bpy.context.scene.view_layers[0].objects.active = armatureObject
    armatureObject.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')

    editBones = []
    pivotpoints = model.PivotPoints
    for index,bone in enumerate(model.Bones):
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
                    fcurve = action.fcurves.new(datapath,index = 2,action_group = bone.Name)
                    fcurve.keyframe_points.add(count = len(bone.Translation))
                    j = 0
                    for k,v in bone.Translation.items():
                        fcurve.keyframe_points[j].co = (int(k)*ms2fps,-v[1]/20)
                        j += 1
                        
        if(bone.Rotation):
            datapath = 'pose.bones["' + bone.Name + '"].rotation_quaternion'
            for i in range(4):
                if i == 0:
                    fcurve = action.fcurves.new(datapath,index = 0,action_group = bone.Name)
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
    for index,bone in enumerate(model.Bones):
        if bone.Parent != -1 and bone.Parent != 4294967295:
            editBones[index].parent = editBones[bone.Parent]
    armatureObject.animation_data_create()
    armatureObject.animation_data.action = action

    camera = bpy.data.cameras.new(model.Camera.Name)
    camera.angle = model.Camera.FieldOfView
    camera.clip_end = model.Camera.FarClip/10
    camera.clip_start = model.Camera.NearClip/10
    cameraObject = bpy.data.objects.new(model.Camera.Name, camera)
    position = model.Camera.Position
    target = model.Camera.Target
    cameraObject.location = Vector(position)/20
    cameraObject.rotation_euler = (Vector(target)-Vector(position)).to_track_quat('-Z', 'Y').to_euler()

    bpy.context.scene.collection.objects.link(cameraObject)

    for index,geoset in enumerate(model.Geosets):
        if(geoset.LevelOfDetail == 0):
            mesh = bpy.data.meshes.new(geoset.Name)
            mesh.from_pydata(geoset.Vertices, [], geoset.Faces)
            for index2,vertex in enumerate(mesh.vertices):
                vertex.normal = geoset.Normals[index2]
                
            # uvLayer = mesh.uv_layers.new()
            # vi_uv = {i: (u, 1.0 - v) for i, (u, v) in enumerate(geoset.TVertices)}
            # per_loop_list = [0.0] * len(mesh.loops)
            # for loop in mesh.loops:
            #     per_loop_list[loop.index] = vi_uv[loop.vertex_index]
            # per_loop_list = [uv for pair in per_loop_list for uv in pair]
            # uvLayer.data.foreach_set('uv',per_loop_list)

            meshObject = bpy.data.objects.new(geoset.Name, mesh)
            meshObject.matrix_world = Matrix(((0.05, 0.0, 0.0, 0.0),(0.0, 0.05, 0.0, 0.0),(0.0, 0.0, 0.05, 0.0),(0.0, 0.0, 0.0, 1.0)))

            vertexGroups = []

            for i in range(len(model.Bones)):
                vertexGroup = meshObject.vertex_groups.new(name = model.Bones[i].Name)
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

def ClassicImport():
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