# DJI产品流行度分析

## 目标
 
1. 编写一个爬虫，解析大疆社区中的作品展示，获得各产品流行度值，并通过图表直观给出各产品受欢迎程度
2. 不要让用你代码的人想修改你的代码！！
 
## 解决方案
 
1. 爬取[链接:https://bbs.dji.com/forum-60-1.html](https://bbs.dji.com/forum-60-1.html)，获取帖子信息：发帖日期，发帖人，发帖人所用设备，帖子标题，链接，帖子访问次数，回复次数，最后回复时间；并将这些写入sqlite数据库中；数据库中表格格式如下:
    ```
    postDate, postBy, device, postTitle, postLink UNIQUE, visitTimes, commentTimes, updateTime
    ```
2. 统计DJI产品设备名写入JSON文件，并判断发帖人设备是否存在，如果存在，该设备流行度加一；如果不存在，保存该链接；
    ```
    接口变量：
    djiDevicePopularity: DJI设备对应的流行度值
    linkListUnident: 不好判断的链接列表
    djiDevice: DJI存在的设备列表
    ||
    至少要有前面数据的导入接口，后面获取新数据的接口
    ```
3. 爬取步骤二中的链接，检测整个页面是否出现步骤一中的设备名称（包括别称），如果存在，该设备流行度加一，否则跳过该链接
    ```
    接口变量：
    djiDevicePopularity: DJI设备对应的流行度值（包含不好判断的链接）
    ||
    至少要有前面数据的导入接口，后面获取新数据的接口
    ```
4. 将步骤2/3中统计的流行度值归一化并制成图表，发到电子邮箱中; 
5. 形成文档

## 依赖关系

    sudo pip3 install lxml
    sudo pip3 install matplotlib
    sudo apt-get install python3-tk
    sudo pip3 install beautifulsoup4
 
## 运行方法

    vi sendResultMail.py修改邮箱地址
    python3 sendResultMail.py

## 运行结果

分析2页，解决中文乱码问题后运行<br>
![five](https://github.com/labrick/Spider4DJIDrone/blob/master/image/result_2page_CN.png)<br>
分析10页，图表改为横向显示，同时添加坐标信息及图题<br>
![five](https://github.com/labrick/Spider4DJIDrone/blob/master/image/result_10page_CN.png)<br>
合并同系列，分析4页，相应的柱状图
![bar4](https://github.com/labrick/Spider4DJIDrone/blob/master/image/bar_4page_CN.png)<br>
合并同系列，分析4页，相应的饼状图
![bar4](https://github.com/labrick/Spider4DJIDrone/blob/master/image/pie_4page_CN.png)<br>



## 分工
 
YANAN: 步骤3 
 
FUAN：步骤2/4 
 
YINBIAO：步骤1 

## 合作说明
 
1. 命名方式统一采用小驼峰式命名法
2. 统一采用python3
3. 统一`tab`为四个`space`
4. 统一注释格式：`#`+空格+注释内容
5. 统一加入单元测试组件
    ```
    def main():
        ...
    if __name__ == '__main__':
        main()
    ```

## 所用到的知识点

1. python语法
2. 对HTML页面的解析
3. 爬虫库（urllib, beautifulsoup）的使用
4. 基本绘图库（matplotlib）的使用

## 开发过程中遇到的问题与解决方法

1. Q: 为了实现完全自动化，需要自动添加新的设备到程序当中。

    A: 分析所有用户认证设备获得所有DJI设备列表。

2. Q: 分析帖子统计所用设备时，个人对设备的称呼都不尽相同，为寻找所用设备增添了难度。

    A: 将程序自动获取的DJI设备列表保存为json文件，并在json文件中手动添加每个设备的别称，同时保证再次执行程序时不会删除掉之前添加的设备别称。

3. Q: 理论上应该是个人写一个模块，然后用最底层一个python文件将各个模块粘合在一起，这样每个模块才更具有独立性，需要改改改！！！

4. Q: 绘制流行度图表时，无人机型号为中文时乱码无法显示。（图表改为横向显示，添加横纵坐标说明及图题）<br>（参考：http://blog.csdn.net/dgatiger/article/details/50414549 ）


    A:方法一： (1) 将win7中/windwos/fonts目录下SIMSUN.ttf（对应宋体字体）拷贝到ubuntu /usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/fonts/ttf目录中
	
    (2) 删除~/.cache/matplotlib的缓冲目录: rm -rf ~/.matplotlib/\*.cache
	
    (3) 第三修改修改配置文件：<br>
	    1) /usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/matplotlibrc,找到如下两项:<br>
         去掉注释 #，并在font.sans-serif冒号后加上 SIMSUN, 保存退出。<br>
         font.family         : sans-serif  
         font.sans-serif     : SIMSUN, ...,sans-serif <br>
        2) 找到axes.unicode_minus，将True改git为False，解决'-'显示为方块问题<br>
    方法二：(1) 在Ubuntu终端中运行fc-list:zhang=CN,得到Ubuntu系统中的中文字库

    (2)使用matplotlib中的font_manager.FrontProperties(fname='/path/to/fonts')来设置每一处的中文字体显示(参考：blog.csdn.net/onepiece_dn/article/details/46239581)

5. Q: 获取所有帖子信息到数据库时，为了避免重复分析帖子信息，需要判断已获取帖子与未处理过的帖子的分界线；

    A: 最后评论时间新于数据中最新时间的帖子为本次需要分析的帖子；在需要分析的帖子里，有些是已经更新在数据库中的，这些需要在数据库中找到，更新最后评论时间；其他的直接写入数据库
