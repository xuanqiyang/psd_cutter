from psd_parse import parse_psd
from gen_vue_template import gen_template 
import argparse
if __name__ == '__main__':
  arg_parse = argparse.ArgumentParser(description='输入psd文件,输出切图')
  arg_parse.add_argument('filepath')
  arg_parse.add_argument('--output',default='./slices/')
  arg_parse.add_argument('--dw',type=int,default=375, required=False)
  arg_parse.add_argument('--compress', type=int, default=9)
  arg_parse.add_argument('--excel', default='./source.xlsx')
  arg_parse.add_argument('--cut', type=int, default=1)
  args = arg_parse.parse_args()
  print(args)
  psd_info = parse_psd(args.filepath, args.output)
  slices =  psd_info.gen_slices_for_design()
  gen_template(args.filepath,args.excel, slices, psd_width=psd_info.psd.width, design_width=args.dw, img_dir=psd_info.output_dir)
  if args.cut == 1:
    psd_info.cut_slices(args.compress)