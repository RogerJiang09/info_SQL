# Roger's 员工系统查询
---
## 程序文件结构
+ SQL_imitation
    + run.py --> 程序运行文件
    + funciton_list.py --> 主要运算函数存储文件
    + staff_table_dict_format.py --> 数据转化函数存储文件
    + staff_table_view --> 可视化文件（符合可是规则）
    + staff_table --> 字典文件（简化运算）
    + help.jpg --> help页面运行效果
    + add.jpg --> add程序运行效果
    + del.jpg --> del程序运行效果
    + update.jpg --> update程序运行效果
    + find.jpg --> find程序运行效果
    + flowchart.jpg --> 程序流程图
    + README.MD
---
## 程序实现功能
+ 存在可视化数据且随程序的删改查即使更新
+ help页面显示输入格式及对应帮助
+  员工信息查询
    + 通过 '=' 进行指定内容的查找
    + 通过 '<' & '>' 进行关于年龄的比较查找
    + 通过 'before' & 'after' 进行关于日期的比较查找
    + 通过 'like'进行对日期的相似查找
+ 员工信息增加
    + 通过 add + [文件名] + 具体信息进行新员工添加
    + 实现当员工离职，后入员工补位离职员工ID的功能
+ 员工信息删除
    + 同过员工id对员工进行删除并在删除前返回具体删除内容寻求确认
+ 员工信息更新
    + 通过用户的定位对相应员工的相应信息进行更改
---
## 程序的启动方式
+ 通过终端或python解释器启动run.py文件
---
## 登陆用户信息
+ 直接启动无需登陆
---
## 程序运行效果
+ help
![help](https://i.loli.net/2020/04/20/WwSonKUVbYgGCN3.jpg)
+ find
![find](https://i.loli.net/2020/04/20/hx8bvXTGdE45QW1.jpg)
+ add 
![add](https://i.loli.net/2020/04/20/EFCAyOke9J46g2G.jpg)
+  del
![del](https://i.loli.net/2020/04/20/1WO3UPYGtApnoFb.jpg)
+ update
![update.jpg](https://i.loli.net/2020/04/20/BuZzETntLJKYUvb.jpg)
---
## 程序运行流程图
+ flowchart
![flowchart.png](https://i.loli.net/2020/04/20/1udAYVUteackqEN.png)