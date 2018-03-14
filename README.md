# DJI产品流行度分析

## 目标
 
1. 编写一个爬虫，解析大疆社区中的作品展示，获得各产品流行度值，并通过图表直观给出各产品受欢迎程度
2. 不要让用你代码的人想修改你的代码！！
3. 尽量做到自动化，可扩展
 
## 解决方案
 
1. 爬取[链接:https://bbs.dji.com/forum-60-1.html](https://bbs.dji.com/forum-60-1.html)，获取帖子信息：发帖日期，发帖人，发帖人所用设备，帖子标题，链接，帖子访问次数，回复次数，最后回复时间；统计DJI产品设备名写入JSON文件，如果链接存在，设备不存在，c采用模块三`anaEachPage`更进一步获取，最后把爬取的数据写入sqlite数据库中；数据库中主表格格式如下:
    ```
    postDate, postBy, device, postTitle, postLink UNIQUE, visitTimes, commentTimes, updateTime
    ```
2. 爬取给定的链接，检测整个页面是否出现JSON中提到的的设备名称（包括别称），如果存在，则返回设备名称
    ```
    deviceList = anaEachPage(url)
    ```
3. 给定特定区间，从数据库中读取对应数据，统计设备流行度；
    ```
    接口变量：
    输入：
    period: 统计周期
    months：需要统计的起始日期（格式：201801）
    输出：
    nameList: 某个特定时间段内所有设备的名称
    valueList: 与nameList相对应的设备的流行度值
    ```
4. 将设备流行度值归一化并制成图表，发到电子邮箱中; 
5. 形成文档

## 依赖关系

    sudo pip3 install lxml
    sudo pip3 install matplotlib
    sudo apt-get install python3-tk
    sudo pip3 install beautifulsoup4
 
## 运行方法


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
5. 设计哲学：
    1. 机制与策略分离
    2. 区间不对称原则

## 开发过程中遇到的问题与解决方法

1. Q: 为了实现完全自动化，需要自动添加新的设备到程序当中。

    > A: 分析所有用户认证设备获得所有DJI设备列表。

2. Q: 分析帖子统计所用设备时，个人对设备的称呼都不尽相同，为寻找所用设备增添了难度。

    > A: 将程序自动获取的DJI设备列表保存为json文件，并在json文件中手动添加每个设备的别称，同时保证再次执行程序时不会删除掉之前添加的设备别称。
    
3. Q: 理论上应该是每人写一个模块，然后用最顶层一个python文件将各个模块粘合在一起，这样每个模块才更具有独立性，需要改改改！！！

4. Q: 绘制流行度图表时，无人机型号为中文时乱码无法显示。（图表改为横向显示，添加横纵坐标说明及图题）<br>
（参考：http://blog.csdn.net/dgatiger/article/details/50414549 ）

    > A: 方法一 
    > >     (1) 将win7中/windwos/fonts目录下SIMSUN.ttf（对应宋体字体）拷贝到ubuntu的
    > >         /usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/fonts/ttf目录中
    > >     (2) 删除~/.cache/matplotlib的缓冲目录: rm -rf ~/.matplotlib/\*.cache
    > >     (3) 第三修改修改配置文件：
    > >         1) /usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/matplotlibrc,找到如下两项:
    > >         去掉注释 #，并在font.sans-serif冒号后加上 SIMSUN, 保存退出。
    > >         font.family         : sans-serif  
    > >         font.sans-serif     : SIMSUN, ...,sans-serif
    > >         2) 找到axes.unicode_minus，将True改git为False，解决'-'显示为方块问题
    > 
    > A: 方法二
    > >     (1) 在Ubuntu终端中运行fc-list:zhang=CN,得到Ubuntu系统中的中文字库
    > >     (2) 使用matplotlib中的font_manager.FrontProperties(fname='/path/to/fonts')来设置每一处的中文字体显示
    > >         (参考：blog.csdn.net/onepiece_dn/article/details/46239581)

5. Q: 获取所有帖子信息到数据库时，为了避免重复分析帖子信息，需要判断已获取帖子与未处理过的帖子的分界线；

    > A: 获取帖子信息时按照发布时间进行排序，并按照日期的从过去到现在的顺序写入数据库，只需要检测数据库中有多少记录(页)，就可以找到已经更新的位置，从而接着进行更新写入数据库；该方法同时解决了异常导致程序停止，更新位置不可知问题；

## TODO LIST

1. 帖子里如果同时存在多个型号的设备名称，应该每个流行度都加一【目前只加了第一次出现的设备】
2. 图形绘制应该增加一个随时间变化的设备数量折线图【目前只有特定区间的设备扇形图和固定区间的设备数量柱形图】
