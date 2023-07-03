import re
from jinja2 import Environment, PackageLoader, Template
loader = PackageLoader("temp", "templates")
env = Environment(loader=loader)
template = env.get_template("template.html")  # 加载某个文件，会从：./temp/templates/ 路径下自动查找这个 test.html
def get_filename_from_path(file_path):
    pattern = r'[^\\/]+(?=\.[^\\/]+$)'
    match = re.search(pattern, file_path)
    if match:
        return match.group(0)
    else:
        return None

def gen_template(file_path, slices, psd_width, design_width):
    # make_source_data(slices, img_dir)
    htmlString = template.render(slices = slices,psd_width=psd_width, design_width=design_width)
    file_name = get_filename_from_path(file_path)
    vueTemplate = open(f'{file_name}.vue', "w",encoding="utf-8")
    vueTemplate.write(htmlString)

# def make_source_data(slices, img_dir):

