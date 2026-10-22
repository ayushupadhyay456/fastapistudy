def hello(a,b,**args):
    k=a+b+sum(args.values());
    print(k)


hello(1,2,x=4,y=9)


#############################

def jefe(a,b,*args):
    k=a+b+sum(args)
    print(k)

jefe(1,2,3,4,5,6,67)

#############################
def freqcount(arr):
    dict={}
    for i in arr:
        if i not in dict:
            dict[i]=1
        else:
            dict[i]+=1
    print(dict)

if __name__=='__main__':
    freqcount([1,4,2,6,6,1])


#####yield -- retrives state of the function 
#Will use generator for large data set 
##############################

# nums=[1,2,3,4,5]
# b=nums
# b.append(6)

# c=deepcopy(nums)
# #Nums will also change if b=nums
#############################

#with statement in python is used to efficiently manage resource,file database connection.


#self -- self is used to refer 

# @staticmethod
# @abstractmethod
# semaphore


# Rank,Dense Rank

def hello():
    yield 1
    yield 2
    yield 3

hello()