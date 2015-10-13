# coding=utf-8
# -*- coding: UTF-8 -*- 
import string
import math
# from math import sqrt 
# 二者都可以引入模块，后者要注意命名空间的问题，例如cmath支持复数计算
my_sqrt = math.sqrt  # from math import sqrt as my_sqrt 也是可以的
num = my_sqrt(100)
num = num // 5.0  # //表示整除，即最终结果忽略小数部分
print("res=" + str(num) + ", " + repr(num))  # Python3.0 之后print需要括号 str()是转化为字符串 repr()是转化为Python格式的字符串
s = """This could
be 'very' "" 
easy"""
str2 = r"C:\box\time\n\""  # r"" 原始字符串  u""  Unicode字符串
print(s + str2)

'''#############序列篇##############'''
# Python序列概念类似一种宽泛动态类型的数组，包括List、Tuple、String三种子类，所有序列子类都有些共性操作，当然也有彼此的特殊点。其中列表是唯一的，元素可改变的类型；元组不可被修改，基本可以被List代替，仅在：Map的Key必须用元组；很多函数的返回值是元组。
# 序列子类的共性操作：
# 索引是向量，-1表示倒数第一个元素，-len表示第一元素，[-len, 0]以外的范围会抛异常
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
num = numbers[-2]
num = numbers[0::-1]  # Slice分片，[a:b]或者[a:b:x]，表示[a, b)区间，步长为x(步长是向量)。a置空表示从0开始，b置空表示到len结束(这个很重要)。
num = num[:]  # 常用于复制一个序列
num = numbers[-3:]  # 表示最后三个元素
print(num)
# 只有一个元素，规则：从a开始，按步长计算下一个元素，达到或超过b表示的实际位置后停止。
num = numbers[-1::-1]  # 这下顺序就对了
print(num)

# 序列支持+ * in 运算符，加法只能连接两个相同类型的序列，*表示复制N次，in 返回布尔值
num = num + [9, 10]  # num = num + "abc" 抛异常
num = 'a' * 10
res = 'a' in num

# 基本函数 长度len(序列) min/max(序列 或 数字)
min(len(num), len(numbers))  # min([1,2,3,4]) both ok
# list()  tuple()  str()  用于将序列生成一个列表、元组、字符串并返回
# 注意！ python中很多重要函数名都被占用了，因此不能拿来做变量名，例如str、list、len，有意义的变量名很重要

# 列表部分（List）
# 列表的元素可变 lst[0]=1  可删   del lst[0] 
# 最重要的在于，元素更改/删除 都可以作用到分片
num = list("hello, world")
num[0:5] = "fuck"  # 分片 是对原始序列的一个引用；修改都会体现在原始序列中
del num[-3:]
print(num)
numbers.append([2, 5])  # 附加一个元素到末尾。[2,5]被作为一个整体看待
numbers.extend([2, 5])  # 将[2,5]合并到numbers的末尾，extend比 +高效,它左侧列表上进行修改，不生成临时变量
print(numbers)
num.count('o')  # 统计次数
numbers.index(7)  # 查找7出现的位置，找不到就抛异常
numbers.insert(len(numbers), 100)  # insert必须指定插入位置，可以插入到len()，即为末尾
numbers.pop(-4)  # pop()默认删除最后一个元素，它返回刚刚被删掉的元素
numbers.reverse()  # 逆序操作
numbers.remove(2)  # 删除与100匹配的第一个元素，找不到则不删
numbers.reverse()
print(numbers)
# 排序
# sort()与sorted()的区别，前者直接修改本地序列，后者在拷贝中排序并返回，不影响当前序列。
# 注意,sort()是list成员方法，sorted()是公共的内置方法
# reversed()/sorted() 都能在不改动本地数据的前提下，生成新的序列并返回。需要注意的是其返回值不一定是list，需要强转。
numbers.sort(reverse=True)  # 排序可选参数还有cmp=.. key=.. 前者用于指定比较函数，后者是个排序键值的生成函数
# 元组部分（Tuple）
tup = (1, 2, 3)  # 特殊的是单元素元组，tup = (1,)
tup = tuple(num)
print("tuple = " + str(tup[0:7]))


'''#############字符串篇##############'''
# 字符串格式化，类似于C风格的格式化操作，基本格式如下：
# 模式串str % 值val     其中val值可能是任何类型，多值情况下，常用元组
my_str = '%d puls %s equals %s' % (1, 1, 2)  # 模式串里的%d标识，类似C风格
my_pi = "pi = %10.5f" % math.pi  # 字段宽度、小数精度控制，详细情况用到再说
print(my_pi)
# string包里有些重要常量，包括string.printable（所有可打印字符）
my_int = my_str.find('ls')  # find(sub或sub,s或sub,s,end) 查找子串第一次出现位置[s, e)，找不到返回-1.
# 类似的还有：rfind、startwith、endswith
# split()与join() 互为逆运算
"1+2+3+4+5".split('+')  # ['1','2'..] 不指定分隔符，默认将空格（包括换行）作为分隔符
print('\\'.join(['C:', 'box', 'rock']))  # C:\box\rock 待拼接的序列元素必须全都是string
# lower islower upper isupper swapcase title()首字母大写，其余小写
my_str = my_str.replace("1", "one")
# strip类似java-trim()，strip("xyz") 可以将收尾两端的x|y|z字符都删掉，默认删除空格 lstrip/rstrip类似
my_str = my_str.strip("on2")
print(my_str)
print "ABC".ljust(10) + "Z"  # ljust/rjust/center是非常常用的格式化函数，用于把ABC补足到10位长度，并且靠左对齐


'''#############字典篇##############'''
# Python中的map可以用如下形式初始化
# phonebook = {'Me':'123', 'You':'456', 'Him':'789'}
# 可以直接添加不存在的键值，但不能直接引用不存在的键值，如phonebook['She']='223'可以，但直接调用phonebook['She']抛异常，可以改用get()。
# 更可以使用dict()创建字典，这是类似list/tuple的类型，可以直接接受一些映射值对，也可以把这些值对装入一个序列，再传入dict.
my_map = dict(name='rock', age='24')  # key可以不加引号
my_item = [('name', 'rock'), ('age', '24'), ('sex', 'girl')]
my_item.append(('sex', 'boy'))  # boy 会把 gril 覆盖掉
my_map = dict(my_item)
print(my_map)

# 极为有用的是，map用作格式化字符串的值串。模式串格式为 %(键值)s|d等说明元素，如%(Rock)s
name_id = {'Rock': '195618', 'Tom': '198733', 'Zero': '000000'}  # 仅仅需要保证模式串的键值都在name_id就行了
print("Rock'id=%(Rock)s; Tom'id=%(Tom)s" % name_id)  # 如果使用了name_id中没有的键值，抛异常

# 字典的基本方法：clear()；get(Key)如果Key不存在则返回None，不抛异常；len(my_map)；del my_map[key],如果key不存在则抛异常；my_map[key]=val是个很安全的操作
res = 'name' in my_map  # 检查key是否存在，同java-containsKey
# items是dict的逆运算，将map作为列表返回；常用iteritems，返回列表迭代器，便于迭代；类似的keys/iterkeys(values/itervalues)分别返回键(值)集合、键(值)集合迭代器。


'''#############语句篇##############'''
# 合法的赋值语句：x=y=100  x+=100  y*=100   str+='abc'
# 特殊的是一种序列解包 x,y,z = 1,2,3 或(1,2,3)。必须保证变量与序列元素个数相同。
x, y, z = [1, 2, 3]  # or x,y,z = 1,2,3
print(x, y, z)
# 这种操作常用于：函数返回元组，解包元组时
my_key, my_value = my_map.popitem()
print(my_key)
my_map[my_key] = my_value
# Python不允许空的语句块，空语句可以用pass代替

# if语句
# False None 0 "" () [] {} 都会被看做False，但是()本身!=[]。False进行数字运算时为0，True为1
my_list = ['a']
my_list2 = ['a']
if my_list is my_list2:  # A is B 用来判断A、B是否为同一个对象，类似java.Object.==
    print(" is same instance ")
elif my_list == my_list2:  # == 判断A、B值是否相同，类型java.Object.equals
    print(" == compare their values. ")
else:
    if 0 < len(my_list) < 10:  ##python的特殊点，可以连续使用比较符号
        print("a")

# 比较运算符有：and or not
my_str = "ok" if not 3 > 2 else "fuck"  # 这是python版本的三元运算比较。 A if cond else B
print(my_str)
# <>的比较两端元素必须有相同类型和结构，字符串按照字典序进行比较（存在大小写时会麻烦）
my_bool = [2, [1, 4]] < [2, [2, 4]]  # [2,1,4] < [2,[2,4]] 抛异常
print(my_bool)

# 循环
x, sum = 1, 0
while True:
    sum += x
    x += 1
    if x % 7 == 0:
        continue
    if x > 100:
        break

# range(x,y,step)或(x,y)或(x)会返回:[x,y)区间，步长为step的序列，默认：x=0，step=1。
# xrange有类似功能，巨大数目列表时range会产生所有的元素，较为低效
sum = 0
for num in range(0, -101, -1):  # sum of (-101,0]
    sum += num
print(sum)

# 针对于字典，for循环可以直接遍历其键集合
for key in my_map:
    print(key, my_map[key])
for key, value in my_map.items():  # 也可以直接遍历值对集合
    print(key, value)

# zip()用于将两个同构的列表，打包成一个。 这样会方便并行遍历两个列表的情况
my_list = [1, 2, 3, 4]  # zip打包的两个列表长度可以不同，按照最短的计算
my_list2 = ['a', 'bb', 'ccc']
print(list(zip(my_list, my_list2)))  # 注意zip返回的不是list，需要强转

# enumerate(List)用于返回<Index,Value>形式的List，这就类似Java-C风格的for循环
for i, val in enumerate(my_list):
    if i == len(my_list) - 1:
        print("Final element :", i, val)

# 列表推导式，用于生成一个列表的表达式。
print([(x, y * y) for x in range(5) for y in range(2, 3)])

# python的动态性还体现在，它可以运行时生成新的代码，并直接执行。
# exec("python代码") 可以直接执行python代码
my_scope = {}  # 创建一个命名空间
exec ("print('hello world')") in my_scope  # 将执行代码放在新的命名空间，以不影响当前空间的代码执行

# eval("python代码") 可以计算python表达式，这就简化了逆波兰计算的过程。而exec是没有返回值的
print(eval("2+3+5"))


'''#############函数篇##############'''
# python函数可以方便返回多个值，使用元组。直接return，其实返回的是None。
# 传参：不可变量是按值传入，如String、Tuple；可变量是按引用传入，如List
def my_func(arg0, arg1="rock"):  # 可以指定默认参数，没有默认值的参数，必须传入
    print(arg0, arg1)

# 调用时可通过形参名，为指定参数赋值。但这种方式不能与默认顺序参数混用。
my_func(arg1=100, arg0=250)  # (arg1=100, 250) (arg1==100) 均抛异常

# *号的意思是收集剩余位置的参数，形成元组
# 可以给函数传入不定量的参数，arg1作为元组接收不定数量的参数
def my_func(arg0, *arg1):  # 重复定义my_func，自动覆盖之前的定义
    print(arg0, arg1)
my_func("MutipleArgs = ")  # arg1为空
my_func("MutipleArgs = ", 1, 'a', 'fuck')

# **号用于传入不定数量的值对，即字典元素
def my_func(arg0, **arg1):
    print(arg0, arg1)
my_func("MutipleArgs = ", age=24, job='rogue', sex='female')

# */**还可以用于拆解序列/字典，拆分为单个元素，传入函数
def my_func(arg0, arg1, arg2):
    print(arg0, arg1, arg2)
my_list = [1, 2]
my_func('Unzip=', *my_list)  # 将my_list拆成了1与2，传入了函数

# 字典的拆分有问题，待研究

def my_func(*arg0, **arg1):  # 这种调用方法很常用
    print(arg0, arg1)
my_func(0, 1, 2, me='rock', she='lucy')

#按引用传入的技巧
def change_num(a):
    a[0] = a[0] ** 2  # a = a ** 2  这二者有本质不同



'''############# 函数装饰器Decorator#############'''
'''
可以给函数加上装饰器（e.g @check）,语法角度类似Java的方法注释。Python装饰器本质用于修改、甚至替换其修饰的函数。所以，装饰器的返回值必须是一个函数。
同时装饰器也必须有至少一个入参，代表其修饰的函数。装饰器有两种类型：有参数、和无参数（这里的参数指自定义的参数），二者语法有些区别。
'''


def deco_check(func):  # 无参数装饰器
    print ""
    def new_func(argA, argB):
        print "New func content replace the eld one"
        func(argA, argB) # 可以在新函数内部调用被修饰函数（Wrapper效果） 也可以不调用
    return new_func # new_func将会替换掉被修饰的函数。这里也可以直接返回 func，即仍然使用原函数。


@deco_check # func1的定义将被替换为 deco_check(func1)
def func1(a, b):
    print "Func1 called. ", a, b
func1('hello', 'world')


def deco_check2(*args):  # 带有参数的装饰器
    print args
    def new_func(func): #被修饰方法无参数
        print "new_func content replace the eld one"

    def new_func2(func):
        print "new_func2 content replace the eld one"
        def handle_args(argA, argB):
            print "new_func2 handle args", argA, argB
            # func(argA, argB) 按需求调用
        return handle_args

    #return new_func  # 处理被修饰方法无参数
    return new_func2 # 处理被修饰方法有参数的情况


@deco_check2("Decorator", "Arguments")  # 可以加入给装饰器的参数
def func2(a, b):
    print "Func2 called. ", a, b
func2('hello', 'world')

'''
装饰器顺序问题：
@A
@B
@C
def f()...
f = A(B(C(f)))
'''


'''Python内置的装饰器：staticmethod, classmethod, property'''
'''
其中@staticmethod用于将一个函数标记为静态方法，可以使用类名直接引用访问
@classmethod用于将一个函数标记为类方法，函数声明时需要加上class参数
@property用于声明类的属性，其作用本质是实现Python下的getter/setter/deleter
'''

input("Press Enter to exit~~~~")
