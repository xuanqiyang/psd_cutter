from psd_tools import PSDImage
from psd_tools.constants import Resource
import numpy as np
from PIL import Image
import threading

def save_layer_as_png(layer, output_path):
  # 获取图层的图像数据
  image_data = layer.composite()
  # 将图像数据转换为NumPy数组
  # image_array = np.array(image_data)
  # 提取非透明像素的边界框
  # non_transparent_pixels = image_array[..., 3] > 0  # Alpha通道大于0的像素即为非透明像素
  # min_row, max_row = np.where(non_transparent_pixels.any(axis=1))[0][[0, -1]]
  # min_col, max_col = np.where(non_transparent_pixels.any(axis=0))[0][[0, -1]]
  # 裁剪图像数据
  cropped_image_data = image_data.crop((min_col, min_row, max_col + 1, max_row + 1))
  # 保存为PNG图像文件
  cropped_image_data.save(output_path, format='PNG')

def in_slice_area(layer, slices):
  target = None
  for item in slices:
    slice = item['slice']
    if slice[0] <= layer.bbox[0] and slice[1]<=layer.bbox[1] and slice[2]>=layer.bbox[2] and slice[3]>=layer.bbox[3]:
      target = item
      break
  return target 
      
def is_top_level_layer(layer, psd):
    return layer.parent == psd 
# @return (x,y,w,h)
def get_layer_position_in_slice(layer, slice):
  return (layer.bbox[0]-slice[0],layer.bbox[1]-slice[1],layer.size[0], layer.size[1])
# 获取切片
# @return list:tuple(left,top,right,bottom)
def get_psd_slices(psd):
  slice_info = psd.image_resources.get_data(Resource.SLICES)
  bounds = []
  if slice_info:
    slices = slice_info.data['slices'] 
    for slice in slices:
      if slice['bounds']:
        bound = slice['bounds']
        coord = (int(bound['Left']),int(bound['Top ']),int(bound['Rght']),int(bound['Btom']))
        bounds.append(coord)
  return sorted(bounds, key=lambda slice: (slice[1], slice[0]))
# 迭代处理图层和分组
def process_layers(psd,slices):
  def get_area_layers(layers):
    for layer in layers:
      if layer.visible:
        area = None
        if layer.name.endswith('_area') or layer.name.endswith('_float'):
          slice = in_slice_area(layer, slices)       
          if not slice is None:
            type = ''
            if layer.name.endswith('_area'):
              type = 'area'
            else:
              type = 'float'
            area = {'type':type,'name':layer.name, 'coord':get_layer_position_in_slice(layer,slice['slice'])}
            if layer.name.endswith('_area'):
              area['text'] = get_area_layer_text_list(layer)
            if layer.name.endswith('_float'):
              area['img'] = f'./{layer.name}.png'           
        if layer.is_group():
          get_area_layers(layer)
        if layer.name.endswith('_float'):
          layers_to_png(layer)
          layer.visible = False
        if not area is None:
          slice['area_list'].append(area)
          slice['area_list'].sort(key=lambda coord: (coord['coord'][1], coord['coord'][0]))
  get_area_layers(psd._layers)
  return slices 

def get_area_layer_text_list(layer):
  text_list = []  
  if layer.is_group():
    for sub_layer in layer:
      text_list.extend(get_area_layer_text_list(sub_layer))
  elif layer.kind == 'type':
    text_content = layer.text
    text_list.append(text_content)
  return text_list


def layers_to_png(layer):
  # 保存图层为PNG图像文件
  output_path = './' + layer.name + '.png'
  save_layer_as_png(layer, output_path)
def cut_slices(psd, slices):
  image = psd.composite(layer_filter=lambda x: x.is_visible())
  for i, slice in enumerate(slices):
    # 裁剪图像
    cropped_image = image.crop(slice['slice'])
    cropped_image.save(f'./slice_{i+1}.png')
if __name__ == '__main__':
  psd = PSDImage.open('./home.psd')
  # 切图按先高后低,先左后右排序
  slices = process_layers(psd, [{'slice':slice, 'area_list':[]} for slice in get_psd_slices(psd)])
  cut_slices(psd, slices)

