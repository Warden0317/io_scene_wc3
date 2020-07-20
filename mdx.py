from . import model
from struct import pack, unpack

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
                print(length_sub)
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
                        print('uv' + str(file.tell()))
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