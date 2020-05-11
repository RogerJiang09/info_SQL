import json
import re


def staff_table_write():
    """
    将源文件的数据reformat写成字典存入新文件以便取值进行对应操作
    """
    with open('staff_table_view', 'r') as origin:
        phone_list = re.findall('\d{11}', origin.read())  # 提取电话号码存入一个列表，为以后进行电话号码的查重用

        origin.seek(0)  # 电话号码的摘取已经让光标走到文末，需要回到开头进行再摘取
        table_keys = origin.readline().strip().split(',')  # 分离每一列的抬头

        id_list = []  # 制作key的表格
        for line in origin:
            id_list.append(int(line.strip().split(',')[0]))

        origin.seek(0)
        origin.readline()  # 跳过第一行抬头行

        detail_info_list = []
        for line in origin:
            detail_info_list.append(dict(zip(table_keys, line.strip('\n').split(','))))  # 将抬头和文本进行结合方便提取
            # print(detail_info_list)

        staff_info_dic = dict(zip(id_list, detail_info_list))  # 将员工编号（唯一）与详细信息进行结合
        # print(staff_info_dic)

    with open('staff_table', 'w') as staff_table_dict:
        # 将整理好的字典存入新文件
        json.dump((staff_info_dic, table_keys, phone_list), staff_table_dict, indent=1)


if __name__ == '__main__':
    staff_table_write()
