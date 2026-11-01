# arr="sabsssssbac"
# dict={}
# for i in list(arr):
#     if i not in dict:
#         dict[i]=1
#     else:
#         dict[i]+=1
# for i,j in dict.items():
#     if j==1:
#         print(i)

#####################################

# class Employee:
#     Company="Google"
#     def __init__(self,name):
#         self.name=name
#         return self.name
#     @classmethod
#     def newnew(cls):
#         return cls.Company
#     @staticmethod
#     def is_valid(name):
#         if len(name)>3:
#             return True
#         else:
#             return False

# print(Employee.newnew())
# print(Employee.is_valid("Ayushshs"))
# e1=Employee("Ayush")
# print(e1.name())

# class Employee:
#     def __init__(self,age):
#         self._age=age
#     @property
#     def age(self):
#         return self._age
#     @age.setter
#     def age(self,value):
#         if value>60:
#             raise ValueError("Invalid value for a Corporate Employee")
#         else:
#             self._age=value

# user1=Employee(25)

# user1.age=59
# print(user1.age)

# def is_palindrome(line):
#     s="".join(i.lower() for i in line if i.isalnum())
#     return s==s[::-1]
# if __name__=='__main__':
#     print(is_palindrome('Mada     m'))

# def check_secondlar(limp):
#     s=set()
#     k=float('-inf')
#     x=[s.add(i) for i in limp]
#     l=-1
#     sl=-1
#     for i in range(len(s)):
#         if limp[i]>l:
#             l=s[i]

#     for i in range(len(s)):
#         if s[i]>sl and s[i]!=l:
#             sl=s[i]
#     return sl
              

# if __name__=='__main__':
#     print(check_secondlar([5,9,9,6,4]))

def count_letters(s):
    d={}
    for i in list(s):
        if i in d:
            d[i]+=1
        else:
            d[i]=1
    return d

if __name__=='__main__':
    print(count_letters('hello'))
        