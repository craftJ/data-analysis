# -*- coding: utf-8 -*-
import random
import string

# 随机生成人物关系
def rand_relations(roles=None):
    if roles == None:
        return
    def connect_random(exceptName):
        #使用sample保证随机的元素不重复
        connectlist = random.sample(roles, random.randint(0,len(roles)-1))
        #去除指定元素，保证没有自关联的关系
        if exceptName != "":
            connectlist = [x for x in connectlist if x != exceptName]
        return connectlist
    relationships = {role:connect_random(role) for role in roles}
    print("\n","relation map:",relationships,"\n")
    return relationships

def main():
    rand_relations(['Alice','Bob', 'Charlie','David','Eve','Fiona','Gary'])
    return


if __name__ == '__main__':
    main()


