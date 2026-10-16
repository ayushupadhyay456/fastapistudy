l=[10,10,20,40,20,30,30]
#10^0=10
#10^10=0
k=0
for i in l:
    k=k^i
print(k)
###########################

s="abcfabc"
k=0
for i in list(s):
    k=k^ord(i)
print(chr(k))
