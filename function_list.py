import json, re, time, os, shutil
import staff_table_dict_format


def homepage():
    """
    主页函数，提示客户输入信息及对输入的信息做初始判定
    """
    print('Home'.center(50, '-'))
    print('请输入公式进行查询 或 输入help查看公式模版 或 exit以退出')  # 用户输入提示
    user_input = input()  # 寻求用户输入

    if user_input.lower().strip().replace(' ', '') == 'help':
        # 帮助页面
        help_list()

    elif user_input.lower().strip().replace(' ', '') == 'exit':
        # 退出程序
        print("谢谢使用Roger's 员工查询系统，期待与您的再次相遇")
        exit()

    else:
        input_list = re.split(' ', user_input.replace('=', ' = '))
        input_list = list(filter(lambda i: i != '', input_list))  # 将input_list列表化并去除无效干扰元素

        def main_function(file, input_list):
            """
            判定用户输入的内容详情并调用相应函数
            :param file: 从用户输入中提取的据源文件名
            :param input_list: 从用户输入提取的信息列表
            """
            while os.path.isfile(file):
                # 因为不知道后期会否加如新的文件，所以加入文件存在性判定
                if 'find' in input_list:
                    find(file, input_list)
                elif 'add' in input_list:
                    add(file, input_list)
                elif 'del' in input_list:
                    delete(file, input_list)
                elif 'update' in input_list:
                    update(file, input_list)
                else:
                    print('wrong input! Try again!')
                    homepage()
            else:
                print('File not exist, please try again!')
                homepage()

        if all([i in input_list for i in ('from', 'where')]):
            # 判定客户具体需求并明确file位置
            file = input_list[input_list.index('from') + 1]
            main_function(file, input_list)
        elif 'add' in input_list:
            # 判定客户具体需求并明确file位置
            file = input_list[input_list.index('add') + 1]
            main_function(file, input_list)
        elif all([i in input_list for i in ('update', 'set', 'where')]):
            # 判定客户具体需求并明确file位置
            file = input_list[input_list.index('update') + 1]
            main_function(file, input_list)
        else:
            print('wrong input! Try again!')
            homepage()


def help_list():
    """
    帮助列表，提示输入方式以及注意事项
    最后寻求输入，输入'b'返回主页菜单
    """
    with open('staff_table_view', 'r') as origin_data:
        # 打开数据源文件并导入具体数据
        info_list = origin_data.readline().strip()

    print('员工信息查询系统帮助页'.center(50, '-'))
    print('员工信息包括%s六项(日期格式为"Year-Month-Day")\n' % info_list + '员工信息可根据这六项内容进行增，删，改，查四类操作')
    print("查操作（find）:\n"
          "find [具体员工信息项或*选择全部(输入两个以上的信息，需以逗号间隔)] from [文件名] where [筛选条件] 如下：\n"
          "find name,age from staff_table where age > 22\n"
          "find * from staff_table where dept = 'IT'\n"
          "find * from staff_table where enroll_date before '2013'\n"
          "find * from staff_table where enroll_date like '2013-04-01'\n"
          "注：日期的仅支持after，before，like的查找，不可用'='\n"
          "增操作（add）:\n"
          "add [文件名] name,age,phone,dept,enroll_date 如下：\n"
          "add staff_table Mosson,18,13678789527,IT,2018-12-11 \n"
          "删操作（del）:\n"
          "del from [文件名] where id = [员工id](仅可通过员工id进行删除) 如下：\n"
          "del from staff_table where id = 10\n"
          "改操作（update）:\n"
          "update [文件名] set [员工信息项] = [修改后内容] where [员工信息项] = [修改所需符合条件](where后起定位效果) 如下：\n"
          "update staff_table set dept = 'Market' where dept = 'IT'\n"
          "update staff_table set age=25 where name = 'Alex Li'"
          )

    back = input("input 'b' to the homepage\n")

    while back.lower() != 'b':
        print('wrong input! try again!')
        back = input("input 'b' to the homepage\n")
    else:
        homepage()


def time_reformat(criteria):
    """
    根据客户输入定义具体时间，以实现各种具体的查找方式（默认客户按照help提示进行输入）
    :param criteria: 客户可能输入的时间
    :return: 返回函数处理后的具体时间
    """
    input_time_reformat = criteria[2].replace("'", '"').strip('"')
    if len(input_time_reformat) == 4:
        exact_time = time.mktime(time.strptime('%s-01-01' % input_time_reformat, '%Y-%m-%d'))
    elif len(input_time_reformat) == 7:
        exact_time = time.mktime(time.strptime('%s-01' % input_time_reformat, '%Y-%m-%d'))
    elif len(input_time_reformat) == 10:
        exact_time = time.mktime(time.strptime(input_time_reformat, '%Y-%m-%d'))
    return exact_time


def operator_transfer(file, criteria, find_out_list):
    """
    筛选函数:对于查找功能的各种表达方式的判定以及输出内容的具体化
    :param file: 从用户输入中提取的据源文件名
    :param criteria: 客户输入的具体筛选条件
    :param find_out_list: 客户需要输出的条件列表
    """
    with open(file, 'r') as staff_table:
        # 打开数据源文件并导入具体数据
        info = json.load(staff_table)

    count = 0

    if criteria[1] == '>':
        for i in info[0].values():
            # 若筛选条件是数字相关项且存在'>'
            if int(i[criteria[0]]) > int(criteria[2]):
                output_list = []
                for k in find_out_list:
                    output_list.append(i[k])
                    count += 1
                print(str(dict(zip(find_out_list, output_list))).replace("'", '').strip('{}'))  # 将名称于内容接驳，是输出合理化
    elif criteria[1] == '<':
        # 若筛选条件是数字相关项且存在'<'
        for i in info[0].values():
            if int(i[criteria[0]]) < int(criteria[2]):
                output_list = []
                for k in find_out_list:
                    output_list.append(i[k])
                    count += 1
                print(str(dict(zip(find_out_list, output_list))).replace("'", '').strip('{}'))  # 将名称于内容接驳，是输出合理化
    elif criteria[1] == '=' and criteria[2].isdigit():
        # 若筛选条件是数字相关项且存在'='
        for i in info[0].values():
            if int(i[criteria[0]]) == int(criteria[2]):
                output_list = []
                for k in find_out_list:
                    output_list.append(i[k])
                    count += 1
                print(str(dict(zip(find_out_list, output_list))).replace("'", '').strip('{}'))  # 将名称于内容接驳，是输出合理化
    elif criteria[1] == '=':
        # 若筛选条件非数字相关项
        if len(criteria[criteria.index('=') + 1:]) > 1:
            # 因为input_list是根据空格进行split的，staff的名称存在两段字符根据空格进行拼接的状态，被split后需要重新拼接使合理化
            criteria[2] = ' '.join(criteria[criteria.index('=') + 1:]).replace("'", '').strip()

        for i in info[0].values():
            if i[criteria[0]] == criteria[2].replace("'", '"').strip('"'):
                output_list = []
                for k in find_out_list:
                    output_list.append(i[k])
                    count += 1
                print(str(dict(zip(find_out_list, output_list))).replace("'", '').strip('{}'))  # 将名称于内容接驳，是输出合理化

    elif criteria[1] == 'like':
        # 时间筛选条件存在'like'项
        for i in info[0].values():
            if re.match(criteria[2].replace("'", '"').strip('"'), i[criteria[0]]):  # 格式化筛选条件的时间
                output_list = []
                for k in find_out_list:
                    output_list.append(i[k])
                    count += 1
                print(str(dict(zip(find_out_list, output_list))).replace("'", '').strip('{}'))  # 将名称于内容接驳，是输出合理化

    elif criteria[1] == 'before':
        # 若筛选条件存在'before'项
        time_stamp = time_reformat(criteria)
        for i in info[0].values():
            if time.mktime(time.strptime(i[criteria[0]], '%Y-%m-%d')) - time_stamp < 0:  # 时间节点前后的判定
                output_list = []
                for k in find_out_list:
                    output_list.append(i[k])
                    count += 1
                print(str(dict(zip(find_out_list, output_list))).replace("'", '').strip('{}'))  # 将名称于内容接驳，是输出合理化

    elif criteria[1] == 'after':
        # 若筛选条件存在'after'项
        time_stamp = time_reformat(criteria)
        for i in info[0].values():
            if time.mktime(time.strptime(i[criteria[0]], '%Y-%m-%d')) - time_stamp > 0:  # 时间节点前后的判定
                output_list = []
                for k in find_out_list:
                    output_list.append(i[k])
                    count += 1
                print(str(dict(zip(find_out_list, output_list))).replace("'", '').strip('{}'))  # 将名称于内容接驳，是输出合理化

    print('%s data found' % int(count / len(find_out_list)))
    homepage()


def find(file, input_list):
    """
    根据用户需求就行查找输出的函数
    :param file: 从用户输入中提取的据源文件名
    :param input_list: 从用户输入提取的信息列表
    """
    find_out_list = ''.join(input_list[1:input_list.index('from')]).split(',')
    criteria = input_list[input_list.index('where') + 1:]

    with open(file, 'r') as staff_table:
        # 打开数据源文件并导入具体数据
        info = json.load(staff_table)

    if criteria[0] in info[1]:
        if find_out_list[0] == '*':
            # 定义'*'代表输出全部相应内容
            find_out_list = info[1]
            operator_transfer(file, criteria, find_out_list)  # 调用筛选函数

        elif set(find_out_list).issubset(set(info[1])):
            # 判定用户输入的需查找内容是否合理
            operator_transfer(file, criteria, find_out_list)

        else:
            print('Wrong input! Try again!')

    else:
        print('Wrong input! Try again!')

    homepage()


def add(file, input_list):
    """
    添加相应内容进入数据源文件中
    :param file: 从用户输入中提取的据源文件名
    :param input_list: 从用户输入提取的信息列表
    """
    adding_str = ''.join(input_list[2:])  # 需要添加的信息
    adding_list = adding_str.split(',')

    with open(file, 'r') as staff_table:
        # 打开数据源文件并导入具体数据，用来进行判定
        info = json.load(staff_table)

    if re.search('1\d{10}', adding_str) and re.search('\d{4}-\d{2}-\d{2}', adding_str) and len(
            adding_list) == 5:
        # 判定输入内容是否符合要求
        if re.search('\d{11}', adding_str).group() in info[2]:
            # 因为手机号要求唯一，所以判定是否重复输入了手机号
            print('phone number is already exist, please check and try again!')
        else:
            id_set = set(map(int, info[0].keys()))
            new_id = set(range(1, len(id_set) + 2)) - id_set  # 若之前删除过中间的id，进行补位操作，不仅仅追加
            adding_str = '%s,%s\n' % (str(new_id).strip('{}'), adding_str)

            with open('staff_table_view', 'a') as origin_data:
                # 追加内容仅源文件
                origin_data.write(adding_str)

            staff_table_dict_format.staff_table_write()  # 将改后数据写入字典文件方便取用
            print('Staff successfully added!')
    else:
        print('wrong input! Try again!')

    homepage()


def delete(file, input_list):
    """
    根据客户输入的id删除数据源文件中的对应数据
    :param file: 从用户输入中提取的据源文件名
    :param input_list: 从用户输入提取的信息列表
    """
    delete_id = input_list[input_list.index('=') + 1]  # 提取用户需要删除的内容id，即key

    with open(file) as staff_table:
        # 打开数据源文件并导入具体数据，用来进行判定以及提示确认信息
        info = json.load(staff_table)

    if input_list[input_list.index('where') + 1].strip(',') == 'id' and delete_id in info[0].keys():
        # 判定输入内容的正确性并打印信息寻求客户确认
        print(str(info[0][delete_id]).replace("'", '').strip('{}'))
        confirmation = input('Are you sure you want the delete this staff from the list?(please enter yes or no)\n')

        if confirmation.lower() == 'yes':
            lines = (i for i in open('staff_table_view') if i.startswith(delete_id) is False)  # 删除相应id行的数据
            with open('origin_data_new', 'w') as replacing_file:
                replacing_file.writelines(lines)
            shutil.move('origin_data_new', 'staff_table_view')
            staff_table_dict_format.staff_table_write()  # 将改后数据写入字典文件方便取用
            print('Successfully delete!')
        else:
            # 若客户认为信息错误不输入'yes'，返回主页
            pass
    else:
        print('Wrong input! Try again!')

    homepage()


def update(file, input_list):
    """
    根据用户输入的需求，更改源文件的相应内容
    :param file: 从用户输入中提取的据源文件名
    :param input_list: 从用户输入提取的信息列表
    """
    condition = input_list[input_list.index('where') + 1:]
    overwrite_info = input_list[input_list.index('set') + 1:input_list.index('where')]

    with open(file) as staff_table:
        info = json.load(staff_table)

    if all([i in info[1] for i in (overwrite_info[0], condition[0])]):
        # 验证改变项和条件项的正确性
        overwrite_section = info[1].index(overwrite_info[0])

        if len(condition[condition.index('=') + 1:]) > 1:
            # 因为input_list是根据空格进行split的，staff的名称存在两段字符根据空格进行拼接的状态，被split后需要重新拼接使合理化
            locate_condition = ' '.join(condition[condition.index('=') + 1:]).replace("'", '').strip()
        else:
            locate_condition = condition[-1].replace("'", '').strip()

        with open('origin_data_rewrite', 'w') as data_rewrite:
            with open('staff_table_view') as data:
                count = 0  # 记录改变条目的数量
                for line in data:
                    line_info = re.split(',', line)  # 分解字符串以方便判定
                    if locate_condition in line_info:
                        line = line.replace(line_info[overwrite_section], overwrite_info[-1].strip("'"))
                        count += 1
                        print('%s: successfully Updated!' % line_info[1])
                    data_rewrite.write(line)
        shutil.move('origin_data_rewrite', 'staff_table_view')
        print('%s data changed' % count)
        staff_table_dict_format.staff_table_write()  # 将改后数据写入字典文件方便取用

    else:
        print('Wrong input! Try again!')

    homepage()
