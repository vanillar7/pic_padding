# pic_padding
将任意一张图像填充到另一张图像指定的区域中，支持“拉伸填充”和“保持原比例填充”两种模式

## 使用说明
参见run.sh脚本  
参数说明：  
replaced：被替换的图像文件  
replaced_conf：被替换图像replaced指定替换区域的json文件  
new：替换的图像  
padding_mode：替换填充模式，0：拉伸填充， 1：保持原比例填充  
outfile：替换填充后图像文件存放路径  

样例：
python pad.py \
--replaced "data/1.jpg"  \
--replaced_conf "data/boxes.json" \
--new "data/2.jpg" \
--padding_mode 0 \
--outfile "data/out.jpg"
