
# coding: utf-8

import numpy as np
from numpy import mean
import pandas as pd
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')


my_data=[['slashdot','USA','yes',18,'None'],
['google','France','yes',23,'Premium'],
['digg','USA','yes',24,'Basic'],
['kiwitobes','France','yes',23,'Basic'],
['google','UK','no',21,'Premium'],
['(direct)','New Zealand','no',12,'None'],
['(direct)','UK','no',21,'Basic'],
['google','USA','no',24,'Premium'],
['slashdot','France','yes',19,'None'],
['digg','USA','no',18,'None'],
['google','UK','no',18,'None'],
['kiwitobes','UK','no',19,'None'],
['digg','New Zealand','yes',12,'Basic'],
['slashdot','UK','no',21,'None'],
['google','UK','yes',18,'Basic'],
['kiwitobes','France','yes',19,'Basic']]

class decision_node:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb
        self.fb=fb

# Divides a set on a specific column. Can handle numeric or nominal values
def divide_set(rows,column,value):
    # Make a function that tells us if a row is in the first group (true) or the second group (false)
    split_function=None
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value
        
    # Divide the rows into two sets and return
    set1=[row for row in rows if split_function(row)]
    set2=[row for row in rows if not split_function(row)]
    return (set1,set2)

divide_set(my_data,0,'slashdot')

my_data_df = pd.DataFrame(my_data)


# Create counts of possible results (the last column of each row is the result)
def unique_counts(rows):
    results={}                      #create a results dictionary 
    for row in rows:
        r=row[len(row)-1]
        if r not in results: 
            results[r]=0
        results[r]+=1
    return results
results = unique_counts(my_data)
print(results)

# Probability that a randomly placed item will be in the wrong category
def gini_impurity(rows):
    total=len(rows)
    counts=unique_counts(rows)
    imp=0
    for k1 in counts:
        p1=float(counts[k1])/total
        for k2 in counts:
            if k1==k2:continue
            p2=float(counts[k2])/total
            imp+=p1*p2
    return imp

gini_impurity(my_data)
set1,set2=divide_set(my_data,2,'yes')
gini_impurity(set2)

# Entropy is the sum of p(x)log(p(x)) across all the different possible results
def entropy(rows):
    from math import log
    log2=lambda x:log(x)/log(2)
    results=unique_counts(rows)
    #Calculate the entropy
    ent=0.0
    for r in results.keys():
        p=float(results[r])/len(rows)
        ent=ent-p*log2(p)
    return ent

def build_tree(rows,scoref=entropy):
    if len(rows)==0:return  decision_node()
    current_score=scoref(rows)
    
    #Set up some variables to track the best criteria
    best_gain=0.0
    best_criteria=None
    best_sets=None
    
    column_count=len(rows[0])-1
    for col in range(0,column_count):
        column_values={}
        for row in rows:
            column_values[row[col]]=1
        # Now try dividing the rows up for each value in this column
        for value in column_values.keys():
            set1,set2=divide_set(rows,col,value)
            
            #Information gain
            p=float(len(set1))/len(rows)
            q=float(len(set2))/len(rows)
            gain=current_score-p*scoref(set1)-q*scoref(set2)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain=gain
                best_criteria=(col,value)
                best_sets=(set1,set2)
    #Create the subbranches
    if best_gain>0:
        trueBranch=build_tree(best_sets[0])
        falseBranch=build_tree(best_sets[1])
        return decision_node(col=best_criteria[0],value=best_criteria[1],tb=trueBranch,fb=falseBranch)
    else:
        return decision_node(results=unique_counts(rows))

tree=build_tree(my_data)

def print_tree(tree,indent=''):
    # Is this leaf node?
    if tree.results!=None:
        print(str(tree.results))
    else:
        #Print the criteria
        print(str(tree.col)+':'+str(tree.value)+'?')
        
        #Print the branches
        print(indent+'T->')
        print_tree(tree.tb,indent+' ')
        print(indent+'F->')
        print_tree(tree.fb,indent+' ')
print_tree(tree)       

def getwidth(tree):
    if tree.tb==None and tree.fb==None: return 1
    return getwidth(tree.tb)+getwidth(tree.fb)

def getdepth(tree):
    if tree.tb==None and tree.fb==None: return 0
    return max(getdepth(tree.tb),getdepth(tree.fb))+1


from PIL import Image,ImageDraw

def drawtree(tree,jpeg='tree.jpg'):
    w=getwidth(tree)*100
    h=getdepth(tree)*100+120
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)
    drawnode(draw,tree,w/2,20)
    img.save(jpeg,'JPEG')

def drawnode(draw,tree,x,y):
    if tree.results==None:
        # Get the width of each branch
        w1=getwidth(tree.fb)*100
        w2=getwidth(tree.tb)*100
        # Determine the total space required by this node
        left=x-(w1+w2)/2
        right=x+(w1+w2)/2
        # Draw the condition string
        draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))
        # Draw links to the branches
        draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
        draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))
        # Draw the branch nodes
        drawnode(draw,tree.fb,left+w1/2,y+100)
        drawnode(draw,tree.tb,right-w2/2,y+100)
    else:
        txt=' \n'.join(['%s:%d'%v for v in tree.results.items( )])
        draw.text((x-20,y),txt,(0,0,0))

drawtree(tree,jpeg='treeview.jpg')

#Classify new observations 
def classify(observation,tree):
    if tree.results!=None:
        return tree.results
    else:
        v=observation[tree.col]
        branch=None
        if isinstance(v,int)or isinstance(v,float):
            if v>tree.value:branch=tree.tb
            else:
                branch=tree.fb
        else:
            if v==tree.value:branch=tree.tb
            else:branch=tree.fb
        return classify(observation,branch)

classify(['(direct)','USA','yes',5],tree)

#Dealing with numerical outcomes 
def variance(rows):
    if len(rows)==0:return 0
    data=[float(row[len(row)-1])for row in rows]
    mean=sum(data)/len(data)
    variance=sum([(d-mean)**2for d in data])/len(data)
    return variance

