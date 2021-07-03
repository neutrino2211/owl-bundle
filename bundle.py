import zlib
import sys
from os import path
import os, shutil
import json
import FQL
import onetimepad

args = sys.argv[1:]

def delete(folder):
    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        os.unlink(folder)

def byteify(s):
    arr = []
    for c in s:
        arr.append(ord(c))
    return bytearray(arr)

def makeBundle(dir):
    # arg = args[1]
    fz = FQL.FlameZipArchive()
    
    s = fz.archiveDir("build")
    a = "*".join(s)
    # a = ""

    # for z in s:
    #     a+=z+"*"
    print("Packaging",dir)
    comp = zlib.compress(byteify(a))
    dest = open(dir,"wb")
    dest.write(comp)
    dest.close()
    delete('build/'+dir[:-3]+'header')
    delete('build/assets.fz')

        

def buildBundle(name="App"):
    if not os.path.isdir(os.path.join(os.path.curdir,"build")):
        sys.stderr.write("Error : {} is not a directory.\n".format("build"))
        sys.exit()
    makeBundle(name)

def archiveAssets(arg):
    # arg = args[1]
    if not os.path.isdir(os.path.join(os.path.curdir,arg)):
        sys.stderr.write("Error : {} is not a directory.\n".format(arg))
        sys.exit()
    fz = FQL.FlameZipArchive()
    
    s = fz.archiveDir(arg)
    assets = os.listdir(arg)
    for i,l in enumerate(s):
        # print(l.split("?")[1],i)
        print("Adding asset:",assets[i])
        s[i] = s[i].replace(path.relpath(arg),"")
    # s[1] = s[1].replace("")
    a = "*".join(s)
    # a = ""
    # print(path.relpath(arg))
    # for z in s:
    #     a+=z+"*"

    comp = zlib.compress(byteify(a))
    dest = open("build/assets.fz","wb")
    dest.write(comp)
    dest.close()

def confirm_required_fields(obj):
    keys = obj.keys()
    if not "entries" in keys:
        raise Exception("Field: 'entries' is required in .app.json")
    
    if not "bundle" in keys:
        raise Exception("Field: 'bundle' is required in .app.json")

    if not "name" in keys:
        raise Exception("Field: 'name' is required in .app.json")

def bundle(args):
    # Application bundle header
    bundle_header = "xOWL" + ("\x00"*0xf0)

    # App config path
    app_json = path.join(args[0],".app.json")

    # App config object
    app_config = json.load(open(app_json))

    print(app_config['name'])

    # Self explanatory
    confirm_required_fields(app_config)

    # Application entry point
    app_main = path.join(args[0],app_config["entries"]["main"])

    # Add app name to bundle header
    bundle_header_bytes = list(bundle_header)
    bundle_header_bytes[4:4+len(app_config["name"])] = list(app_config["name"])
    bundle_header_bytes[124:124+len(app_config["bundle"])] = list(app_config["bundle"])

    # print(bundle_header_bytes)

    final_app_header = []
    final_app_header.extend(bundle_header_bytes)
    # Confirm build path
    if not os.path.exists("build"):
        os.makedirs("build")

    entry_code_zlib = zlib.compress(open(app_main,"rb").read())
    # print(byteify(open(app_main).read()))
    print("Adding entry file:",app_main)
    xx = []
    for x in list(entry_code_zlib):
        xx.append(chr(x))
    # print(xx)
    final_app_header.extend(xx)
    # print(final_app_header)
    header_string = []
    for s in final_app_header:
        header_string.append(ord(s))
    # print(bytes(header_string,"ISO-8859-5"))

    # Write app header 
    with open("./build/"+app_config["name"]+".header", "wb") as f:
        f.write(bytearray(header_string))

    archiveAssets(args[0]+"/"+app_config["assets"])
    buildBundle(app_config["name"]+".app")

if __name__ == "__main__":
    bundle(args)