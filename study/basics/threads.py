#coding=utf-8
# -*- coding: UTF-8 -*- 
import threading
import time

'''#############创建线程##############'''
# thread/threading模块都提供了多线程的支持；thread模块调用start_new_thread()来运行一个线程，threading模块是对thread模块的封装，使用threading就足够了。

class mythread(threading.Thread): # 可以创建自己的线程类，继承Thread
    data = 0
    
    def __init__(self, thread_name='', data=0): # 构造函数覆盖
        threading.Thread.__init__(self, name = thread_name) # 可以指定线程命，必须指明参数名
        self.data = data
    
    def run(self): # 覆盖run()，这是业务方法
        print 'Thread Name = ' + self.getName(), ', Data = ', self.data
        
        time.sleep(2)  # 休眠2s  注意单位是秒

t1 = mythread('Buddy', (1,2,3))
t1.start()
## Thread中的方法
t1.setName('Phoenix') #修改线程名
print "Thread Info: ",t1.getName(), t1.isAlive() # 判断t1是否还在执行
t1.join() # 当前线程阻塞，直到t1执行完成
print 'Now T1 executed over....'

## 直接使用Thread实例创建线程
def my_work(x, y):
    for i in range(x, y): 
        print i
# 对于简单任务不需要创建自己的类，只需要用Thread实例就足够
t2 = threading.Thread(target = my_work, args = (50, 55))
# 在默认的情况下，主线程中创建子线程，即使主线程结束，子线程仍然会执行。
t2.setDaemon(True) # 这会保证主线程结束后，t1同时被杀死。注意：必须在start()之前调用
t2.start()


'''#############线程同步和通信##############'''
# 互斥：python提供保证数据同步的互斥锁threading.Lock()或者.RLoc()。二者有微小区别，R表示reentrant。
# 如果线程T1获取了lock，毋庸置疑的是T2获取时会阻塞。但是如果代码中，T1想要再次获取lock（很少有这样的需求），这时Lock类型的锁会导致T1直接阻塞，即产生死锁；而RLock类型，则运行T1多次获取lock，当然每次acquire都有相应release。RLock会调用Lock，Lock的性能相对比RLock高。因此，如不存在很2的设计会导致T1多次调用的话，尽量使用Lock。
lock = threading.Lock() # 锁变量
lock.acquire() 
# lock.acquire()  # 连续调用acquire会导致死锁，可以改用RLock
print 'Here handle your data in security'
lock.release()


# 线程通信：Condition内部聚合了RLock，因此可以直接调用acquire/release进行互斥保护。其wait/notify/notifyAll的内涵与Java基本相同。以下是生产者-消费者，涉及多线程处理时，逻辑不够审慎很容易造成死锁。

##### Queue模块：很好的实现了生产者-消费者模式。
# 1. 互斥保护queue.put和get是线程安全的； 2. 当队列为空时queue.get()可以阻塞当前线程，也可以返回None，这都是可以通过参数控制的。见文档：http://docs.python.org/2/library/queue.html


class producer(threading.Thread):
    test_times = 5
    def run(self):
        print 'Run producer'
        while producer.test_times > 0:
            producer.test_times -= 1
            global goods_num
            if con.acquire():     # 对数据、对条件变量的操作必须用互斥锁的保护
                if goods_num > 0: # 还有商品，挂起，等待con的通知
                    con.wait()
                else:
                    goods_num = 1000 # 商品为0，生产1000商品，唤醒消费者
                    print "Producer produce 1000 goods."
                    con.notify()     # 随机找一个消费者
                con.release()
            time.sleep(1)
        
        con.acquire()
        print 'Finish producer'
        con.notifyAll() ## 生产者线程要结束了，唤醒所有消费者。 否则消费者一直处于挂起
        con.release()
        

class consumer(threading.Thread):
    def run(self):
        print 'Run consumer'
        while producer.test_times > 0:
            global goods_num
            if con.acquire():
                if goods_num <= 0: # 没有商品，挂起，等待con通知
                    con.wait()
                else:
                    goods_num = 0  # 有商品，消费完所有的，唤醒生产者
                    print self.getName() + " consumer all goods."
                    con.notifyAll() ## 这里必须使用notifyAll，确保生产者能够唤醒。如使用notify，则可能无法唤醒生产者，造成死锁
    
                con.release()
            time.sleep(1)
        print 'Finish consumer'
        

con = threading.Condition() # 条件变量

goods_num = 0

p = producer()
p.start()
for i in range(2):
    print i
    c = consumer()
    c.setName('Consumer'+str(i+1))
    c.start()
p.join()










