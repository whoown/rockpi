#coding=utf-8
# -*- coding: UTF-8 -*- 
'''#############模块##############'''
# 导入模块：1.import XXX  2. import XXX as your_new_name  3. from XXX import your_function
# 一个模块就是一个.py文件，需要将其导入到sys.path中，才能被python找到，进而被引用。有两种情况：
# 1. 运行my.py时，解释器自动将my.py所在目录加载到sys.path中
# 2. 纯粹手动加载某个目录: sys.path.append('your path')

# 所有模块在第一次调用时，被编译成.pyc字节码文件，用以提高启动速度。每次启动会比较my.py和my.pyc的时间戳，以判断是否更新。发布时可以只发布pyc文件，对源代码有一定保护作用。.pyo是优化后的字节码文件，体积更小。

# 一个包就是一个目录，这个目录中必须有一个文件：__init__.py(用以标识当前目录为包，可为空)。A目录/B目录/my.py ，引用方式为：import A.B.my

# 变量作用域：1. 全局作用域：整个.py文件范围内； 2. 局部作用域：函数内部
my_num = 100
my_list = [1,2]

def scope_test():
	global my_num # 在函数内部，可以读取全局变量，但不能直接修改。除非使用Global关键字进行声明
	my_num += 1000
	my_list.append(3) # 类似Java，这种限制对引用类型而言，不限制其中内容的改变。

scope_test()
print my_num, my_list # 1100 [1,2,3]


'''#############异常处理##############'''

try:
	a = 1 / 0
except ZeroDivisionError, value: # value为异常包含的信息
	print 'Divide Zero, msg =', value
except:  # 捕获所有异常； except (KeyError, ValueError):  捕获某类异常
	print 'Error happen'
else:                       # 不抛异常的时候才会执行
	print 'Everything OK'
finally:                    # 如同Java-finally
	print 'Always execute'

# 想要捕获异常的同时拿到异常Log数据，必须制定异常名。except (KeyError, ValueError), value: 

##自定义异常
class MyError(Exception):
	def __init__(self, data): # data是Exception内部属性
		self.data = data
	def __str__(self):
		return self.data

try:
	raise MyError,'Fuck you, world!!' # raise可以主动抛出异常
except MyError, value:
	print value


'''#############面向对象##############'''

class person:
	s_population = 0 # python中的静态属性与对象属性没有本质区别
	name = ''        # 用类名访问就是静态属性，用对象名访问就是对象属性，都可以直接读写
	__age = 0        # 两个下划线表示私有属性。类内部访问私有属性or方法需要用self.
	
	def set_age(self, new_age): #所有方法的第一个参数必须是self，表示对自身的引用。
		self.__age = new_age    
		self.__print_age()      #私有域，必须用self引用
	
	def get_age(self):
		return self.__age
		
	def __print_age(self):      #私有方法，两个下划线
		print self.__age
		
	def __init__(self, name):   #型如__abc__() 是class自有的方法。init是构造函数
		self.name = name  #非私有属性也可用self
		

rock = person('Rocky') # 实例化
person.s_population += 1 # 静态属性用类名直接访问
rock.set_age(47)

#### 静态方法 ####
# 补充静态方法，不需要self参数，但是需要@staticmethod修饰符
#
#


#### 继承 ####
# Python支持多继承，其形式为：
# class 新类名(父类1, 父类2, ..):  如果多个类中有重名方法，则按照从左到右顺序选择。

class worker(person):
	eid = 0
	job = ''
	
	def __init__(self, job, id=1): ## 可覆盖父类方法
		person.__init__(self, 'Zhangyan') #可用调用父类方法，需要传入self：父类名.func(self, 参数)
		self.job = job
		self.eid = id
		self.__age = 140  # 父类的私有属性无法继承，因此不生效
		self.set_age(140) # 必须使用继承下来的方法访问私有属性

killer = worker('Just kill peoples')
print killer.eid, killer.name, killer.job, killer.get_age()

## 注意：Python的函数重载是通过参数默认值、可变参数列表等实现的。
driver = worker('Drive people to heaven', 195618) # 算是调用了一个重载版本
print driver.eid, driver.name, driver.job, driver.get_age()

## 运算符重载：Python的class自带了所有运算符的重载方法，覆盖这些方法就完成了运算符重载
# __add__()、__sub__()、__mul__()、__div__()



