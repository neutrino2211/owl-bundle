import os
import json
import argparse
from bundle import bundle

def initialize(args):
    if not os.path.exists(args.directory):
        os.mkdir(args.directory)
    
    proj_dir = os.path.join(args.directory, args.id)

    dist = os.path.join(proj_dir, 'dist')
    src = os.path.join(proj_dir, 'src')

    if not os.path.exists(src):
        os.mkdir(src)
    if not os.path.exists(dist):
        os.mkdir(dist)
    if not os.path.exists(proj_dir):
        os.mkdir(proj_dir)

    index = os.path.join(src, 'index.html')

    pkg_conf = os.path.join(proj_dir, 'package.json')
    app_json = os.path.join(proj_dir, '.app.json')

    with open(app_json, 'w') as f:
        f.write(json.dumps({
            "bundle": args.id,
            "name": args.name,
            "entries": {
                "main": 'dist/index.html'
            },
            "assets": 'dist'
        }))

    with open(pkg_conf, 'w') as f:
        f.write(json.dumps({
            "name": args.id,
            "version": "0.0.0",
            "description": "",
            "main": "index.js",
            "keywords": [],
            "author": "",
            "license": "ISC"
        }))

    with open(index, 'w') as f:
        f.writelines('\n'.join([
            '<html>',
            '\t<head>',
            '\t</head>',
            '\t<body>',
            '\t</body>',
            '</html>'
        ]))

def build_project(args):
    bundle([args.directory])
parser = argparse.ArgumentParser(description='OWL-OS sdk command line tool')

subparsers = parser.add_subparsers(help='Commands')
parser_1 = subparsers.add_parser('build', help='Build an OWL-OS project')
parser_1.add_argument('directory', type=str, help='directory to build')
parser_1.set_defaults(build=True, func=build_project)

# parser_2 = subparsers.add_parser('init', help='...')
# parser_2.set_defaults(parser2=True)

parser_3 = subparsers.add_parser('init', help='Create an OWL-OS project')
parser_3.add_argument('directory', type=str, help='directory to keep project files')
parser_3.set_defaults(init=True, func=initialize)
parser_3.add_argument('id', type=str, help='Application ID e.g (com.dev.app)')
parser_3.add_argument('name', type=str, help='Application name')

args = parser.parse_args()
if args.func:
    args.func(args)