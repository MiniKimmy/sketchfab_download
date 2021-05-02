# -*- coding: utf-8 -*-
import sys
import os 
import build_args_parser
import export_fbx # put it into .blend/scripts/

global build_args

def work():
    global build_args
    blend_fn = build_args["blend_fn"]
    output_dir = build_args["output_dir"]
    fn = os.path.basename(output_dir) + ".fbx"
    save_path = output_dir + os.sep + fn
    if os.path.exists(save_path):
        os.remove(save_path)
    export_fbx.write_ui(save_path)
    sys.exit() # 关掉当前blender窗口

if __name__ == '__main__':
    global build_args
    arg_config = {
        "blend_fn" : str,   # .blend文件的路径
        "output_dir" : str, # 生成fbx所在的文件夹目录路径, 无传则认为在.blend文件所在目录生成.fbx
    }
    build_args = build_args_parser.parse(arg_config)
    if build_args.get("blend_fn", None):
        blend_fn = build_args["blend_fn"]
        if os.path.exists(blend_fn):
            if not (build_args.get("output_dir", None)):
                build_args["output_dir"] = os.path.dirname(blend_fn)
            work()
        else:
            print(".blend file not exists %s" % blend_fn)
            os.system('pause')
    else:
        print("not send params '--blend_fn' ")
        os.system('pause')