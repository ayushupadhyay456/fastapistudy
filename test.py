arr="sabsssssbac"
dict={}
for i in list(arr):
    if i not in dict:
        dict[i]=1
    else:
        dict[i]+=1
for i,j in dict.items():
    if j==1:
        print(i)