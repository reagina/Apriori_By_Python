# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 16:47:49 2016

@author: Administrator
"""

class Apriori(object):
    
    def __init__(self,filename,min_support,min_confidence,item_num):
        self.filename = filename
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.line_num = 0
        self.item_num = item_num
        
        self.candidate = [[i] for i in range(item_num)]
        self.support = self.count_support(self.candidate)
        self.num = list(sorted(set([j for i in self.candidate for j in i])))
        
        self.pre_support = []
        self.pre_frequent = []
        self.pre_num = []
        
        self.support_set = [0]
        self.frequent_set = [[]]
        self.sub_support = [[]]
        
        self.item_name = []
        self.find_item_name()
        self.loop()
        self.confidence_sup_2()
        #print self.frequent_set,'frequent_set'
        #print self.support_set,'support_set'
        #Sprint self.sub_support,'sub_support'
        #print 'line_num:',self.line_num
        #print 'line_num:',self.line_num
        #print 'min_support',self.min_support
        #print '%%%%%%%%%:',self.line_num * float(self.min_support) / 100
        
    def deal_line(self,line):
        return [i.strip() for i in line.split(',') if i][1:self.item_num+1]
        
    def find_item_name(self):
        with open(self.filename,'r') as F:
            for index,line in enumerate(F.readlines()):
                if index == 0:
                    self.item_name = self.deal_line(line)
                    break
    
    def count_support(self,candidate):
        with open(self.filename,'r') as F:
            support = [0] * len(candidate)
            for index,line in enumerate(F.readlines()):
                if index == 0:
                    continue
                item_line = self.deal_line(line)
                for index_num,i in enumerate(candidate):
                    flag = 0
                    for j in i:
                        if item_line[j] != 'T':
                            flag = 1
                            break
                    if not flag:
                        support[index_num] += 1
            self.line_num = index
        return support
        
    def next_candidate(self,c):
        stack = []
        for i in self.candidate:
            for j in self.num:
                if j in i:
                    if len(i) == c:
                        stack.append(i)
                else:
                    stack.append([j] + i)   
        #print stack,'stack'
        import itertools
        s = sorted([sorted(i) for i in stack])
        candidate = list(s for s,_ in itertools.groupby(s))
        return candidate
        
    def del_candidate(self,support,candidate):
        for index,i in enumerate(support):
            if i < self.line_num * float(self.min_support) / 100:
                support[index] = 0
        for index,j in enumerate(candidate):
            sub_candidate = [j[:index_loc] + j[index_loc+1:]for index_loc in range(len(j))]
            flag = 0
            for k in sub_candidate:
                if k not in self.frequent_set:
                    flag = 1
                    break
            if flag :
                support[index] = 0
        candidate = [i for i,j in zip(candidate,support) if j != 0]
        support = [i for i in support if i != 0]
        return support,candidate
        
    def loop(self):
        s = 2
        support_set = self.support_set
        frequent_set = self.frequent_set
        sub_support = self.sub_support
        candidate = self.candidate
        support = self.count_support(candidate)
        support_set.extend(support)
        frequent_set.extend(candidate)
        while True:
            print '-'*50
            print 'The',s-1,'loop'
            print 'frequent',self.candidate
            print 'support',self.support
            print 'num',self.num
            print '-'*50
            
            candidate = self.next_candidate(s)
            support = self.count_support(candidate)
            support,candidate = self.del_candidate(support,candidate)
            print 'support_set:',support_set
            print 'frequent_set:',frequent_set
            
            support_set.extend(support)
            frequent_set.extend(candidate)
            for index_candidate,each_candidate in enumerate(self.candidate):
                del_num = [each_candidate[:index] + each_candidate[index+1:] for index in range(len(each_candidate))]
                del_num = [i for i in del_num if i in self.pre_frequent]
                del_support = [self.pre_support[self.pre_frequent.index(i)]for i in del_num if i in self.pre_frequent]
                sub_support.append(del_support)
            
            
            num = list(sorted(set([j for i in candidate for j in i])))
            s += 1
            if candidate and support and num and support_set and frequent_set:
                self.pre_num = self.num
                self.pre_frequent = self.candidate
                self.pre_support = self.support
                
                self.num = num
                self.candidate = candidate
                self.support = support
                self.support_set = support_set
                self.frequent_set = frequent_set
                self.sub_support = sub_support
            else:
                break
            
    def confidence_sup_2(self):
        from matplotlib import pyplot as plt
        if sum(self.pre_support) == 0:
            print 'min_support error'
        else:
            for index1,each_frequent in enumerate(self.frequent_set):
                if index1 == 0:
                    continue
                del_num = [each_frequent[:index] + each_frequent[index+1:] for index in range(len(each_frequent))]
                del_num = [a for a in del_num if a in self.frequent_set]
                for index_del,i in enumerate(del_num):
                    if self.support_set[index1]:
                        support = float(self.support_set[index1]) / self.line_num * 100
                        
                        sub = self.support_set[self.frequent_set.index(i)]
                        if sub != 0:
                            confidence = float(self.support_set[index1]) / sub * 100
                            if confidence > self.min_confidence:
                                s = [j for index_item,j in enumerate(self.item_name) if index_item in i]
                                s1 = [u for index_u,u in enumerate(self.item_name) if index_u in each_frequent and index_u not in i]
                                #print ','.join(s),'->>',self.item_name[each_frequent[index_del]],'support:',str(support) + '%','min_confidence:',str(confidence) + '%'
                                print ','.join(s),'->>',''.join(s1),'support:',str(support) + '%','confidence:',str(confidence) + '%'
                                
                                
                                #plt.title(title, size=14)
                                plt.figure(figsize=(6,9))
                                labels = ['confidence','not_confidence']
                                colors = ['red','yellowgreen']
                                explode = (0.05,0)
                                sizes = [confidence,100-confidence]
                                #print 'sizes:',sizes
                                patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,startangle=90,pctdistance = 0.6)
                                for t in l_text:
                                    t.set_size=(30)
                                for t in p_text:
                                    t.set_size=(20)
                                plt.axis('equal')
                                plt.legend()
                                plt.show()
                                
                                
def main():
    import os
    #while True:
    dir = 'D:\python_workspace'
    filename = raw_input('filename:')
    s = dir+'\\'+filename
    if os.path.isfile(s):
        min_support = raw_input('min_support:')
        min_confidence = raw_input('min_confidence:')
        item_num = raw_input('item_num:')
        Apriori(s,int(min_support),int(min_confidence),int(item_num))
    else:
        print filename,' dose not exist in current directory,please try again!'
        #continue
        #Apriori('simple2.txt',20,0,5)
    
if __name__ == '__main__':
    main()