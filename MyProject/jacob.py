from itertools import islice   
import random

list = [random.randint(-10,10) for _ in xrange(10)]
dict = {x: random.randint(60,100) for x in xrange(1,26)}
print list
print dict

l1 = filter(lambda x:x>=0,list)
print l1

l2 = [x for x in list if x>=0]
print l2

for k,v in dict.iteritems():
    print k,v

d1 = {k: v for k,v in dict.iteritems() if v>=90}
print d1



