from . import classes

def mdlreadClassic(file):
    version = model.Version()
    model = model.Model()
    sequences = model.Sequences()
    texture = model.Textures()
    material = model.Materials()
    geosets = []
    bones = []
    pivotpoints = model.PivotPoints()

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
            geoset = model.Geoset()
            geoset.read(file)
            geosets.append(geoset)
        elif label == "Bone":
            bone = model.Bone()
            bone.read(file,parameter[0])
            bones.append(bone)
        elif label == "PivotPoints":
            pivotpoints.read(file,parameter[0])
        else:
            i = 0
            while file.readline()[0:1] != '}':
                i = i + 1
        line = file.readline()