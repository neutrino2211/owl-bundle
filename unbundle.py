import zlib
import FQL
import sys

def byteify(s):
    arr = []
    for c in s:
        arr.append(ord(c))
    return bytearray(arr)

def frombits(bits):
    chars = ""
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars += chr(int(byte,2))
    return chars

def unpackAssets(assets):
    a = str(assets)[2:-1]
    assets_dict = {}
    # print(a)
    a = a.replace("\\\\","\\")
    assets = a.split("*")
    for asset in assets:
        cva = asset.split("?")
        assets_dict[cva[1]] = frombits(FQL.FUnassign(FQL.FUnassign2(cva[0])))
    return assets_dict

def main(args):

    bundle = zlib.decompress(args[0])
    bundle = str(bundle)[2:-1]
    bundle_parts = bundle.split("*")

    # HEADER
    bundle_header = bundle_parts[0]
    bundle_header_content = frombits(FQL.FUnassign(FQL.FUnassign2(bundle_header.split("?")[0])))

    # Assets
    bundle_assets = bundle_parts[1]
    bundle_assets_content = frombits(FQL.FUnassign(FQL.FUnassign2(bundle_assets.split("?")[0])))
    try:
        assets = unpackAssets(zlib.decompress(byteify(bundle_assets_content)))
    except Exception as e:
        bundle_header = bundle_parts[1]
        bundle_header_content = frombits(FQL.FUnassign(FQL.FUnassign2(bundle_header.split("?")[0])))

        # Assets
        bundle_assets = bundle_parts[0]
        bundle_assets_content = frombits(FQL.FUnassign(FQL.FUnassign2(bundle_assets.split("?")[0])))
        assets = unpackAssets(zlib.decompress(byteify(bundle_assets_content)))
    # print(assets)
    if bundle_header_content[:4] == "xOWL":
        print("Valid application")
        app_entry = zlib.decompress(byteify(bundle_header_content[0xf4:]))
        app_header = bundle_header_content[:0xf4]
        app_name,app_package = (app_header[124:].replace("\x00",""),app_header[4:124].replace("\x00",""))
        # print(app_name,app_package)
        return (app_name,app_package,app_entry,assets)
    else:
        print("Error: '{}' is not an owl app".format(args[0]))
        exit(0)

if __name__ == "__main__":
    args = sys.argv[1:]
    content = open(args[0],"rb").read()
    (app_name,app_package,app_entry,assets) = main([content])

    if args[1] == 'info':
        print('''
Application: %s
Package Name: %s,
Assets: %s
        '''%(app_name, app_package, ','.join(assets.keys())))
    else:
        print(app_name,app_package,app_entry,assets)