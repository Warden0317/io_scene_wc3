import bpy

class Version:
    def __init__(self):
        self.FormatVersion = 0
    def read(self,file):
        self.FormatVersion = file.readline().replace(",", "").split(" ")[1]
        file.readline()
    def readx(self,file):
        self.FormatVersion = file.read(4)
    def write(self,file):
        file.write("Version {\n\tFormatVersion %d,\n}\n" % self.FormatVersion)

class Model:
    def __init__(self):
        self.Name = ""
        self.Version = Version()
        self.Geosets = []
        # self.NumGeosets = 0
        # self.NumGeosetAnims = 0
        self.Bones = []
        self.PivotPoints = PivotPoints()
        # self.NumBones = 0
        # self.NumAttachments = 0
        # self.NumParticleEmittersPopcorn = 0
        # self.NumEvents = 0
        # self.NumFaceFX = 0
        # self.BlendTime = 0
        # self.MinimumExtent = []
        # self.MaximumExtent = []
    def read(self,file,name):
        self.Name = name.strip("\"")
        line = file.readline()
        while line[0:1] != '}':
            label,*parameter = line.strip().split(" ")
            if label == "NumGeosets":
                self.NumGeosets = int(parameter[0].replace(",", ""))
            elif label == "NumGeosetAnims":
                self.LevelOfDetail = int(parameter[0].replace(",", ""))
            elif label == "NumBones":
                self.NumBones = int(parameter[0].replace(",", ""))
            elif label == "NumAttachments":
                self.NumBones = int(parameter[0].replace(",", ""))
            elif label == "NumEvents":
                self.NumBones = int(parameter[0].replace(",", ""))
            elif label == "NumFaceFX":
                self.NumBones = int(parameter[0].replace(",", ""))
            else:
                pass
            line = file.readline()
    def write(self,file):
        file.write("Model \"%s\" {\n" % self.Name)
        file.write("\tNumGeosets %d,\n" % self.NumGeosets)
        file.write("\tNumBones %d,\n" % self.NumBones)
        file.write("\tBlendTime %d,\n" % self.BlendTime)
        file.write("}\n")

class Sequences:
    def __init__(self):
        self.working = 0
    def read(self,file):
        i = 0
        while file.readline()[0:1] != '}':
            i = i + 1

class Textures:
    def __init__(self):
        self.working = 0
    def read(self,file):
        i = 0
        while file.readline()[0:1] != '}':
            i = i + 1
    def write(self,file):
        file.write("Textures 1 {\n\tBitmap {\n\t\tImage \"Textures\white.blp\",\n\t}\n}\n")

class Materials:
    def __init__(self):
        self.working = 0
    def read(self,file):
        i = 0
        while file.readline()[0:1] != '}':
            i = i + 1
    def write(self,file):
        file.write("Materials 1 {\n\tMaterial {\n\t\tLayer {\n\t\t\tFilterMode None,\n\t\t\tstatic TextureID 0,\n\t\t}\n\t}\n}\n")

class Geoset:
    def __init__(self):
        self.Vertices = []
        self.Normals = []
        self.TVertices = []
        self.VertexGroup = []
        self.Tangents = []
        self.SkinWeights = []
        self.Faces = []
        self.Groups = []
        self.MaterialID = 0
        self.SelectionGroup = 0
        self.LevelOfDetail = 0
        self.Name = ""
    def read(self,file):
        line = file.readline()
        while line[0:1] != '}':
            if line.strip()[-1] == "{":
                label,*parameter = line.strip().split(" ")
                if label == "Vertices":
                    for i in range(int(parameter[0])):
                        current = file.readline().strip().strip('{},;')
                        self.Vertices.append([float(n)/20 for n in current.split(', ')])
                    file.readline()
                elif label == "Normals":
                    for i in range(int(parameter[0])):
                        current = file.readline().strip().strip('{},;')
                        self.Normals.append([float(n) for n in current.split(', ')])
                    file.readline()
                elif label == "TVertices":
                    for i in range(int(parameter[0])):
                        current = file.readline().strip().strip('{},;')
                        self.TVertices.append([float(n) for n in current.split(', ')])
                    file.readline()
                elif label == "Tangents":
                    for i in range(int(parameter[0])):
                        current = file.readline().strip().strip('{},;')
                        self.Tangents.append([float(n) for n in current.split(', ')])
                    file.readline()
                elif label == "SkinWeights":
                    for i in range(int(parameter[0])):
                        current = file.readline().strip().strip(',')
                        self.SkinWeights.append([int(n) for n in current.split(', ')])
                    file.readline()
                elif label == "VertexGroup":
                    for i in range(len(self.Vertices)):
                        current = file.readline().strip().strip(',')
                        self.VertexGroup.append(int(current))
                    file.readline()
                elif label == "Groups":
                    for i in range(int(parameter[0])):
                        current = file.readline().strip()[9:].strip('{},;')
                        self.Groups.append([int(n) for n in current.split(', ')])
                elif label == "Faces":
                    file.readline()
                    data = file.readline().strip().strip('{},;').split(', ')
                    for i in range(int(int(parameter[1])/3)):
                        self.Faces.append((int(data[i*3]),int(data[i*3+1]),int(data[i*3+2])))
                else:
                    i = 0
                    while file.readline()[1:2] != '}':
                        i = i + 1
            else:
                label,*parameter = line.strip().strip(',').split(" ")
                if label == "MaterialID":
                    self.MaterialID = int(parameter[0])
                elif label == "SelectionGroup":
                    self.SelectionGroup = int(parameter[0])
                elif label == "LevelOfDetail":
                    self.LevelOfDetail = int(parameter[0])
                elif label == "Name":
                    self.Name = parameter[0].strip("\"")
                else:
                    pass
            line = file.readline()
    def write(self,file):
        file.write("Geoset {\n")
        # vertex
        file.write("\tVertices %d {\n" % len(self.Vertices))
        for vertex in self.Vertices:
            file.write("\t\t{ %.6f, %.6f, %.6f },\n" % (vertex[0],vertex[1],vertex[2]))
        file.write("\t}\n")
        # normal
        file.write("\tNormals %d {\n" % len(self.Vertices))
        for normal in self.Normals:
            file.write("\t\t{ %.6f, %.6f, %.6f },\n" % (normal[0],normal[1],normal[2]))
        file.write("\t}\n")
        # uv
        file.write("\tTVertices %d {\n" % len(self.Vertices))
        for tvertex in self.TVertices:
            file.write("\t\t{ %.6f, %.6f },\n" % (tvertex[0],tvertex[1]))
        file.write("\t}\n")
        # vertex group
        file.write("\tVertexGroup {\n")
        for vg in self.VertexGroup:
            file.write("\t\t%d,\n" % vg)
        file.write("\t}\n")
        # tangents
        if(self.Tangents):
            file.write("\tTangents %d {\n" % len(self.Vertices))
            for tangent in self.Tangents:
                file.write("\t\t{ %.6f, %.6f, %.6f, 1 },\n" % (tangent[0],tangent[1],tangent[2]))
            file.write("\t}\n")
        #skinweight
        if(self.SkinWeights):
            file.write("\tSkinWeights %d {\n" % len(self.Vertices))
            for skinweight in self.SkinWeights:
                file.write("\t\t%d, %d, %d, %d, %d, %d, %d, %d,\n" % (skinweight[0],skinweight[1],skinweight[2],skinweight[3],skinweight[4],skinweight[5],skinweight[6],skinweight[7]))
            file.write("\t}\n")
        # triangle
        file.write("\tFaces 1 %d {\n" % int(len(self.Faces)*3))
        file.write("\t\tTriangles {\n\t\t\t{")
        for Triangle in self.Faces:
            file.write(" %d, %d, %d," % Triangle)
        file.seek(file.tell()-1)
        file.write(" },\n\t\t}\n\t}\n")
        # groups
        count = 0
        for g in self.Groups:
            count += len(g)
        file.write("\tGroups %d %d {\n" % (len(self.Groups),count))
        for group in self.Groups:
            file.write("\t\tMatrices { %s },\n" % ', '.join(str(g) for g in group))
        file.write("\t}\n")

        file.write("\tMaterialID 0,\n")

        file.write("}\n")

class Bone:
    def __init__(self):
        self.ObjectId = 0
        self.Parent = -1
        self.ParentName = ""
        self.GeosetId = -1
        self.GeosetAnimId = ""
        self.Translation = {}
        self.Rotation = {}
        self.Scaling = {}
        self.Name = ""
    def read(self,file,name):
        self.Name = name.strip("\"")
        line = file.readline()
        while line[0:1] != '}':
            if line.strip()[-1] == "{":
                label,*parameter = line.strip().split(" ")
                if label == "Translation":
                    file.readline()
                    for i in range(int(parameter[0])):
                        num,data = file.readline().strip().split(":")
                        data = data.strip().strip('{},;')
                        self.Translation.update({num:[float(n) for n in data.split(', ')]})
                    file.readline()
                elif label == "Rotation":
                    file.readline()
                    for i in range(int(parameter[0])):
                        num,data = file.readline().strip().split(":")
                        data = data.strip().strip('{},;')
                        self.Rotation.update({num:[float(n) for n in data.split(', ')]})
                    file.readline()
                elif label == "Scaling":
                    file.readline()
                    for i in range(int(parameter[0])):
                        num,data = file.readline().strip().split(":")
                        data = data.strip().strip('{},;')
                        self.Scaling.update({num:[float(n) for n in data.split(', ')]})
                    file.readline()
                else:
                    i = 0
                    while file.readline()[1:2] != '}':
                        i = i + 1
            else:
                label,*parameter = line.strip().strip(',').split(" ")
                if label == "ObjectId":
                    self.ObjectId = int(parameter[0])
                if label == "Parent":
                    self.Parent = int(parameter[0])
                if label == "GeosetId":
                    self.GeosetId = parameter[0]
                if label == "GeosetAnimId":
                    self.GeosetAnimId = parameter[0]
                else:
                    pass
            line = file.readline()
    def write(self,file):
        file.write("Bone \"%s\" {\n" % self.Name[-3:])
        file.write("\tObjectId %d,\n" % self.ObjectId)
        if self.Parent != -1:
            file.write("\tParent %d,\n" % self.Parent)
        if self.GeosetId == -1:
            file.write("\tGeosetId Multiple,\n")
        else:
            file.write("\tGeosetId %d,\n" % self.GeosetId)
        file.write("\tGeosetAnimId None,\n")
        # Translation
        if len(self.Translation):
            file.write("\tTranslation %d {\n\t\tLinear,\n" % len(self.Translation))
            file.write("\t\t0: { 0, 0, 0 },\n")
            for k,v in self.Translation.items():
                file.write("\t\t%s: { %.6f, %.6f, %.6f },\n" % (k,v[0],v[1],v[2]))
            file.write("\t}\n")
        # Rotation
        if len(self.Rotation):
            file.write("\tRotation %d {\n\t\tLinear,\n" % len(self.Rotation))
            for k,v in self.Rotation.items():
                file.write("\t\t%s: { %.6f, %.6f, %.6f, %.6f },\n" % (k,v[0],v[1],v[2],v[3]))
            file.write("\t}\n")
        # Scaling
        if len(self.Scaling):
            file.write("\tScaling %d {\n\t\tLinear,\n" % len(self.Scaling))
            for k,v in self.Scaling.items():
                file.write("\t\t%s: { %.6f, %.6f, %.6f },\n" % (k,v[0],v[1],v[2]))
            file.write("\t}\n")
        file.write("}\n")

class PivotPoints:
    def __init__(self):
        self.Location = []
    def read(self,file,count):
        for i in range(int(count)):
            current = file.readline().strip().strip('{},;')
            self.Location.append([float(n)/20 for n in current.split(', ')])
        file.readline()
    def write(self,file):
        file.write("PivotPoints %d {\n" % len(self.Location))
        for loc in self.Location:
            file.write("\t{ %.6f, %.6f, %.6f },\n" % (loc[0]*20,loc[1]*20,loc[2]*20))
        file.write("}\n")