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

class Employee:
    def __init__(self,age):
        self._age=age
    @property
    def age(self):
        return self._age
    @age.setter
    def age(self,age):
        if self.age>60:
            raise "Invalid value for a Corporate Employee"
        else:
            self._age=age

user1=Employee(25)

user1.age=61
print(user1.age)