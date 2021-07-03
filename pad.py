# -*- coding: utf-8 -*-

import os

import cv2

def replace(replaced_pic_file, replaced_pic_rect, replacement_pic_file, padding_mode, outfile):
    '''
    用其他图像填充图像指定方框区域中的部分
    参数：
    replaced_pic_file：
        str, 被替换的图像
    replaced_pic_rect：
        dict， replaced_pic图像的矩形方框信息
        样例：{"left_top": [100, 100], "right_bottom": [200, 300]}
    replacement_pic_file：
        str, 替换的图像
    padding_mode：替换图像填充模式，0：拉伸填充，1：保持原比例填充
    outfile：替换后图像文件保存路径
    '''
    replaced_img = cv2.imread(replaced_pic_file)
    replacement_img = cv2.imread(replacement_pic_file)

    # 获取矩形宽、高
    rect_left_top_x = replaced_pic_rect['left_top'][0]
    rect_left_top_y = replaced_pic_rect['left_top'][1]
    width = replaced_pic_rect['right_bottom'][0] - replaced_pic_rect['left_top'][0]
    height = replaced_pic_rect['right_bottom'][1] - replaced_pic_rect['left_top'][1]
    if replaced_img.shape[1] < replaced_pic_rect['right_bottom'][0] or \
            replaced_img.shape[0] < replaced_pic_rect['right_bottom'][1]:
        print("被替换的图像尺寸小于配置文件中矩形大小")
        return

    # 替换模式
    if padding_mode == 0:  # 拉伸填充
        replacement = cv2.resize(replacement_img, (width, height))
    else:
        # 保持原比例填充，若替换图像超出了被替换图像的大小，截断
        replacement = replacement_img[:height,:width,:]
        width = replacement.shape[1]
        if rect_left_top_x + width > replaced_img.shape[1]:
            width = replaced_img.shape[1]-rect_left_top_x
        height = replacement.shape[0]
        if rect_left_top_y + height > replaced_img.shape[0]:
            height = replaced_img.shape[0] - rect_left_top_y

    for c in range(replacement.shape[2]):
        replaced_img[rect_left_top_y:rect_left_top_y + height,
                        rect_left_top_x:rect_left_top_x + width, c] = replacement[:height, :width, c]
        # replaced_img[rect_left_top_x:rect_left_top_x + width,
        #         rect_left_top_y:rect_left_top_y + height, c] = replacement[:width, :height, c]

    cv2.imwrite(outfile, replaced_img)


if __name__ == "__main__":
    import argparse
    import json

    # 参数配置解析
    parser = argparse.ArgumentParser(description="arguments of padding tool")
    parser.add_argument('--replaced', help='to be replaced pic', type=str, default=None)
    parser.add_argument("--replaced_conf", help="models folder", type=str, default=None)
    parser.add_argument('--new', help='replacement pic', type=str, default=None)
    parser.add_argument("--padding_mode", help='padding mode, 0:拉伸填充, 1:保持原比例填充', type=int, default=0)
    parser.add_argument("--outfile", help='outfile', type=str, default=None)
    args = parser.parse_args()
    # print(args)
    if not args.replaced or not args.replaced_conf or not args.new or not args.outfile:
        print("参数错误")
        exit(-1)

    # 获取被替换图像的box_b
    box_b_rectangle = None
    conf_boxes_name = 'boxes'
    conf_box_name = 'name'
    conf_box_value = 'box_b'
    conf_box_rectangle_name = 'rectangle'
    with open(args.replaced_conf, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)
        if conf_boxes_name not in json_data:
            print("被替换图像配置文件内容有误，无法获取%s字段" % conf_boxes_name)
            exit(-1)
        if type(json_data[conf_boxes_name]) != list:
            print("被替换图像配置文件内容有误，%s字段内容不是数组形式" % conf_boxes_name)
            exit(-1)
        for one_box in json_data[conf_boxes_name]:
            if one_box.get(conf_box_name, "").strip() == conf_box_value:
                if conf_box_rectangle_name not in one_box:
                    print("被替换图像配置文件内容有误，%s没有%s字段" % (conf_box_value, conf_box_rectangle_name))
                    exit(-1)
                box_b_rectangle = one_box.get(conf_box_rectangle_name, {})
                break

        if not box_b_rectangle:
            print("被替换图像配置文件内容有误，获取不到%s的rectangle信息" % conf_box_value)
            exit(-1)
        print("rectangle: ", box_b_rectangle)

    replace(args.replaced, box_b_rectangle, args.new, args.padding_mode, args.outfile)


