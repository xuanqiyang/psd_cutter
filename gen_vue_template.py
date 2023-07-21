import re
from jinja2 import Environment, PackageLoader, Template
import openpyxl
import json
import Levenshtein

loader = PackageLoader("temp", "templates")
env = Environment(loader=loader)
template = env.get_template("template.html")  # 加载某个文件，会从：./temp/templates/ 路径下自动查找这个 template.html
def get_filename_from_path(file_path):
    pattern = r'[^\\/]+(?=\.[^\\/]+$)'
    match = re.search(pattern, file_path)
    if match:
        return match.group(0)
    else:
        return None
# 计算文本相似度
def calc_text_similarity(text1, text2):
    text1 = re.sub("\s+", "", text1)
    text2 = re.sub("\s+", "", text2) 
    # set1 = set(text1.split())
    # set2 = set(text2.split())
    # intersection = len(set1.intersection(set2))
    # union = len(set1.union(set2))
    # print(text1, text2, intersection / union)
    # return intersection / union
    distance = Levenshtein.distance(text1, text2)
    similarity = 1 - (distance / max(len(text1), len(text2)))
    return similarity

def gen_template(file_path, excel_path, slices, psd_width, design_width, img_dir):
    htmlString = template.render(slices = slices,psd_width=psd_width, design_width=design_width, img_dir=img_dir)
    file_name = get_filename_from_path(file_path)
    vueTemplate = open(f'{file_name}.vue', "w",encoding="utf-8")
    vueTemplate.write(htmlString)
    sourceData =open(f'{file_name}.json', "w", encoding="utf-8")
    sourceData.write(make_source_data(slices, excel_path, img_dir))

def make_source_data(slices,excel_path, img_dir):
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook['Sheet1']
    products = []
    for row in sheet.iter_rows(values_only=True):
        products.append({
            'name': row[0],
            'id': row[1]
        })
    workbook.close()
    source_data = [] 
    for i, slice in enumerate(slices):
        productIds = []
        for area in slice['area_list']:
            if not area['primary_text'] is None:
                primary_text =  area['primary_text']
                similarity = 0
                productId = ''
                for i, row in enumerate(products):
                    _similarity = calc_text_similarity(row['name'], primary_text)
                    if _similarity > similarity:
                        similarity = _similarity
                        productId = f"{row['id']}"
                productIds.append(productId)
        source_data.append({
            'img':f'{img_dir}slice_{i+1}.png',
            'productIds':productIds
        })
    json_text = json.dumps(source_data)
    return json_text

