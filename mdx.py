
from struct import pack, unpack
from .classes import (Model,Bone,Geoset)
def readint(file,length):
    return int.from_bytes(file.read(length),'little')

def readfloat(file):
    return 1

def mdxReadClassic(file):
    magic = file.read(4)
    label = file.read(4).decode()
    while label:
        length = int.from_bytes(file.read(4),'little')
        if label == "VERS":
            version = model.Version()
            version.FormatVersion = file.read(length)
        elif label == "MODL":
            file.read(length)
        elif label == "SEQS":
            file.read(length)
        elif label == "MTLS":
            file.read(length)
        elif label == "TEXS":
            num = int(length/268)
            for i in range(num):
                par1 = file.read(4)
                print(file.read(264).decode().strip().strip(b'\x00'.decode()))
        elif label == "GEOS":
            geoset = model.Geoset()
            start = file.tell()
            while file.tell()-start<length:
                length_sub = int.from_bytes(file.read(4),'little')
                start_sub = file.tell()
                while file.tell()-start_sub < length_sub-4:
                    label_g = file.read(4).decode()
                    if label_g == "VRTX":
                        par = int.from_bytes(file.read(4),'little')
                        for i in range(par):
                            file.read(12)
                            # print(unpack('f'*3,file.read(12)))
                    elif label_g == "NRMS":
                        par = int.from_bytes(file.read(4),'little')
                        for i in range(par):
                            file.read(12)
                    elif label_g == "PTYP":
                        file.read(24)
                        par = int.from_bytes(file.read(4),'little')
                        for i in range(par):
                            file.read(2)
                    elif label_g == "GNDX":
                        par = int.from_bytes(file.read(4),'little')
                        for i in range(par):
                            file.read(1)
                    elif label_g == "MTGC":
                        par = int.from_bytes(file.read(4),'little')
                        for i in range(par):
                            file.read(4)
                    elif label_g == "MATS":
                        par = int.from_bytes(file.read(4),'little')
                        for i in range(par):
                            file.read(4)
                        file.read(520)
                    elif label_g == "UVAS":
                        file.read(8)
                        par = int.from_bytes(file.read(4),'little')
                        for i in range(par):
                            file.read(8)
        elif label == "BONE":
            start = file.tell()
            while file.tell()-start<length:
                length_sub = int.from_bytes(file.read(4),'little')
                name = file.read(80)
                obid = file.read(4)
                parent = file.read(4)
                file.read(4)
                a = file.read(4)
                if(a == "KGTR"):
                    length_b = file.read(4)
                    file.read(4)
                    file.read(4)
                    file.read(4)
                geoid = file.read(4)
                geoAnid = file.read(4)
                start_sub = file.tell()
                while file.tell()-start_sub < length_sub-4:
                    label_b == ""
        elif label == "PIVT":
            num = int(length/268)
            for i in range(num):
                par1 = file.read(12)
        else:
            file.read(length)
        label = file.read(4).decode()


        #help
        #atch
        #pivt
        #evts
        #clid


def mdxReadReforged(file,model):
    magic = file.read(4)
    label = file.read(4).decode()
    while label:
        length = int.from_bytes(file.read(4),'little')
        if label == "VERS":
            version = model.Version
            version.FormatVersion = readint(file,length)
        elif label == "MODL":
            file.read(length)
        elif label == "SEQS":
            file.read(length)
        elif label == "MTLS":
            file.read(length)
        elif label == "TEXS":
            file.read(length)
        elif label == "GEOS":
            start = file.tell()
            while file.tell()-start<length:
                geoset = Geoset()
                start_sub = file.tell()
                length_sub = readint(file,4)
                while file.tell()-start_sub < length_sub:
                    label_g = file.read(4).decode()
                    if label_g == "VRTX":
                        par = readint(file,4)
                        for i in range(par):
                            geoset.Vertices.append(list(unpack('f'*3,file.read(12))))
                    elif label_g == "NRMS":
                        par = readint(file,4)
                        for i in range(par):
                            geoset.Normals.append(list(unpack('f'*3,file.read(12))))
                    elif label_g == "PTYP":
                        file.read(24)
                        par = readint(file,4)
                        for i in range(int(par/3)):
                            geoset.Faces.append(list(unpack('H'*3,file.read(6))))
                    elif label_g == "GNDX":
                        file.read(4)
                    elif label_g == "MTGC":
                        par = readint(file,4)
                        for i in range(par):
                            file.read(4)
                    elif label_g == "MATS":
                        par = readint(file,4)
                        for i in range(par):
                            file.read(4)
                        file.read(12)
                        geoset.LevelOfDetail = readint(file,4)
                        geoset.Name = file.read(112).decode().strip().strip(b'\x00'.decode())
                    elif label_g == "TANG":
                        par = readint(file,4)
                        for i in range(par):
                            file.read(16)
                    elif label_g == "SKIN":
                        par = readint(file,4)
                        for i in range(int(par/8)):
                            geoset.SkinWeights.append(list(unpack('B'*8,file.read(8))))
                    elif label_g == "UVAS":
                        file.read(8)
                        par = readint(file,4)
                        for i in range(par):
                            file.read(8)
                # print(geoset.LevelOfDetail)
                model.Geosets.append(geoset)
        elif label == "BONE":
            start = file.tell()
            while file.tell()-start<length:
                bone = Bone()
                start_sub = file.tell()
                length_sub = readint(file,4)
                bone.Name = file.read(80).decode().strip().strip(b'\x00'.decode())
                bone.ObjectId = readint(file,4)
                bone.Parent = readint(file,4)
                file.read(4)
                while file.tell()-start_sub < length_sub-8:
                    label_b = file.read(4).decode()
                    if label_b == "KGTR":             #Translation
                        par1 = readint(file,4)
                        file.read(8)
                        for i in range(par1):
                            bone.Translation.update({readint(file,4):list(unpack('f'*3,file.read(12)))})
                    elif label_b == "KGRT":           #Rotation
                        par1 = readint(file,4)
                        file.read(8)
                        for i in range(par1):
                            bone.Rotation.update({readint(file,4):list(unpack('f'*4,file.read(16)))})
                    elif label_b == "KGSC":
                        par1 = readint(file,4)
                        file.read(8)
                        for i in range(par1):
                            bone.Scaling.update({readint(file,4):list(unpack('f'*3,file.read(12)))})
                file.read(8)
                model.Bones.append(bone)

        elif label == "PIVT":
            num = int(length/12)
            for i in range(num):
                model.PivotPoints.Location.append(list(unpack('f'*3,file.read(12))))
        elif label == "CAMS":
            length_sub = readint(file,4)
            model.Camera.Name = file.read(80).decode().strip().strip(b'\x00'.decode())
            model.Camera.Position = list(unpack('f'*3,file.read(12)))
            model.Camera.FieldOfView = unpack('f',file.read(4))[0]
            model.Camera.FarClip = unpack('f',file.read(4))[0]
            model.Camera.NearClip = unpack('f',file.read(4))[0]
            model.Camera.Target = list(unpack('f'*3,file.read(12)))
        else:
            file.read(length)
        label = file.read(4).decode()

#GEOA
#ATCH
#CAMS
#EVTS
#CLID
#FAFX
#BPOS