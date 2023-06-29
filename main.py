from psd_parse import parse_psd
import argparse




if __name__ == '__main__':
  arg_parse = argparse.ArgumentParser(description='输入psd文件,输出切图')
  arg_parse.add_argument('filepath')
  arg_parse.add_argument('--output',default='./slices/',required=False)
  args = arg_parse.parse_args()

  psd_info = parse_psd(args.filepath, args.output)

  print(psd_info.slices)

  psd_info.cut_slices()