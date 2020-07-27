
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
            version.FormatVersion = file.read(length)
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
                geoset = Model.Geoset()
                start_sub = file.tell()
                length_sub = readint(file,4)
                while file.tell()-start_sub < length_sub:
                    label_g = file.read(4).decode()
                    if label_g == "VRTX":
                        par = readint(file,4)
                        for i in range(par):
                            file.read(12)
                    elif label_g == "NRMS":
                        par = readint(file,4)
                        for i in range(par):
                            file.read(12)
                    elif label_g == "PTYP":
                        file.read(24)
                        par = readint(file,4)
                        for i in range(par):
                            file.read(2)
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
                        file.read(128)
                    elif label_g == "TANG":
                        par = readint(file,4)
                        for i in range(par):
                            file.read(16)
                    elif label_g == "SKIN":
                        par = readint(file,4)
                        for i in range(par):
                            file.read(1)
                    elif label_g == "UVAS":
                        file.read(8)
                        par = readint(file,4)
                        for i in range(par):
                            file.read(8)
        # elif label == "BONE":
        #     start = file.tell()
        #     while file.tell()-start<length:
        #         bone = model.Bone()
        #         length_sub = readint(file,4)
        #         name = file.read(80)
        #         obid = file.read(4)
        #         parent = file.read(4)
        #         file.read(4)
        #         if file.read(4) == "KGTR":
        #             par1 = readint(file,4)
        #             file.read(8)
        #             for i in range(par1):
        #                 file.read(16)
        #         elif file.read(4) == "KGRT":
        #             par1 = readint(file,4)
        #             file.read(8)
        #             for i in range(par1):
        #                 file.read(20)
        #         file.read(8)

        elif label == "PIVT":
            num = int(length/12)
            for i in range(num):
                file.read(12)
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