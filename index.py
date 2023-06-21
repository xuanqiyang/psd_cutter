import cv2
import pytesseract
from shapely.geometry import Polygon
from scipy.spatial import ConvexHull
import math
# 以较小的图形为基准,计算图形的重合率,过滤重合太高的图块
def polygon_overlap_percentage(poly1, poly2):
    rect1 = Polygon(poly1)
    rect2 = Polygon(poly2)
    intersection_area = rect1.intersection(rect2).area
    base_area = min(rect1.area, rect2.area)
    overlap_percentage = intersection_area / base_area * 100
    return overlap_percentage
#比较图块在整图中的位置
def compare_rect(r1, r2):
    sr1=sorted(r1, key=lambda p:p[1])
    sr2=sorted(r2, key=lambda p:p[1])
    if sr1[0][1] > sr2[0][1]:
        return -1
    elif sr1[0][1] < sr2[0][1]:
        return 1 
    else:
        return 0
# 获取点与X轴的夹角
def get_polar_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    angle = math.atan2(dy, dx)
    return angle

# 按顺时针排序 
def sort_react_points(points):
    center = tuple(map(sum, zip(*points)))  # 计算所有点的中心坐标
    center = (center[0] / len(points), center[1] / len(points))  # 计算平均值
    sorted_points = sorted(points, key=lambda p: get_polar_angle(center, p))
    return sorted_points
# 排列点与点的连接方向,使其组成图形不交叉
def sort_rectangle_points(vertices):
    hull = ConvexHull(vertices)
    sorted_vertices = [vertices[i] for i in hull.vertices]
    return sorted_vertices
def convert_rect(points):
    rect=sort_rectangle_points(points)
    # 找到最小和最大的 x 坐标和 y 坐标
    min_x = min(rect, key=lambda p: p[0])[0]
    max_x = max(rect, key=lambda p: p[0])[0]
    min_y = min(rect, key=lambda p: p[1])[1]
    max_y = max(rect, key=lambda p: p[1])[1]
    # 构建矩形的四个顶点
    rectangle = sort_react_points([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])
    return rectangle

def remove_blank_lines(text):
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)
# 读取图片
img = cv2.imread('./demo.jpg')

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 进行二值化处理
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 寻找轮廓
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 遍历轮廓
rectList = []
for i in range(len(contours)):
    contour = contours[i]
    # 计算轮廓的周长
    perimeter = cv2.arcLength(contour, True)
    # 近似计算轮廓的多边形形状
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    # 如果多边形有四个点，则认为是矩形
    if len(approx) == 4 and cv2.isContourConvex(approx):
        # 绘制矩形框
        area = cv2.contourArea(contours[i])
        #设置区域大小
        if area <= 423400 and area >= 380000:
            index = 0
            rect = convert_rect([item[0] for item in approx])
            # 过滤重复轮廓
            isOverLap = False
            for i2 in range(len(rectList)):
                overlap_percentage = polygon_overlap_percentage(rect, rectList[i2])
                if overlap_percentage > 90:
                    isOverLap = True
                    break
                if rect[0][1]>rectList[i2][0][1]:
                    index = i2
            if not isOverLap:
                # cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
                rectList.insert(index, rect)
log = open('./log.txt', 'a+', encoding="utf8")
for i, item in enumerate(rectList):
    print(item)
    x = item[0][0]
    y = item[0][1]
    w = item[2][0] - x
    h = item[2][1] - y
    grayRect = cv2.cvtColor(img[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
    fileName = '{}.jpg'.format(i) 
    rectBlock = cv2.threshold(grayRect, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite(fileName, rectBlock)
    text = pytesseract.image_to_string(rectBlock, lang="chi_sim", )
    log.writelines('\n'+remove_blank_lines(text).replace(" ", ""))
    
