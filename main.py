from psd_parse import parse_psd
from gen_vue_template import gen_template 
import argparse
if __name__ == '__main__':
  arg_parse = argparse.ArgumentParser(description='输入psd文件,输出切图')
  arg_parse.add_argument('filepath')
  arg_parse.add_argument('--output',default='./slices/',required=False)
  arg_parse.add_argument('--dw',type=int,default=375, required=False)
  args = arg_parse.parse_args()
  psd_info = parse_psd(args.filepath, args.output)
  slices =  psd_info.gen_slices_for_design()
  gen_template(args.filepath, slices, psd_width=psd_info.psd.width, design_width=args.dw)
  psd_info.cut_slices()