from psd_tools import PSDImage
from psd_tools.constants import Resource
# 加载PSD文件
psd = PSDImage.open('./home.psd')


layers = psd._layers
slice_info = psd.image_resources.get_data(Resource.SLICES)
slices = slice_info.data['slices'] 
for slice in slices:
  print(slice)


# def get_area_layer_text_list(layer):
#   text_list = []  # 存储文本内容的列表
#   # 检查图层是否为分组图层
#   # print(layer.kind, layer.text)
#   if layer.is_group():
#     # 遍历分组图层中的每个子图层
#     for sub_layer in layer._layers:
#       # 递归调用函数提取文本，并将结果添加到列表中
#       text_list.extend(get_area_layer_text_list(sub_layer))
#   # 检查图层是否为文本图层
#   elif layer.kind == 'type':
#     # 获取图层中的文本
#     text_content = layer.text

#     # 将文本内容添加到列表中
#     text_list.append(text_content)
#   return text_list
# def process_layers(layers):
#   png_layers = []
#   for layer in layers:
#     print(layer.kind, layer.name)
#     if layer.is_group():
#       process_layers(layer)
# process_layers(layers)