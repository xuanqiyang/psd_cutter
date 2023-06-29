from psd_parse import parse_psd
from jinja2 import Environment, PackageLoader, Template

# 声明一个 package 加载器，会自动去 temp 这个 python包下的 templates 文件夹找所有的文件，即：./temp/templates/*.*
loader = PackageLoader("temp", "templates")
env = Environment(loader=loader)  # 生成环境

template = env.get_template("template.html")  # 加载某个文件，会从：./temp/templates/ 路径下自动查找这个 test.html
psd_info = parse_psd('./home.psd', './slices/')
slices =  psd_info.gen_slices_for_design()
print(slices)

print(template.render(slices = slices,psd_width=psd_info.psd.width, design_width=375))

# def make_template(slices):
    


# if __name__ == '__main__':

    