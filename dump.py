import math
import os
import random
import re
import sys

#task2
if __name__ == '__main__':
    n = int(input("").strip())


    if n>=1 and n<=100:
         
            if n%2==0 and ((n>=2 and n<=5) or (n>20)):
                print ("Not Weird")
            elif n%2==0 and (n>=6 and n<=20):
                print("Weird")
            elif n%2!=0:
                    print ("Weird")
                        
    else: 
        if  n<1 or n>100:
            print("Invalid number.")
    
#task3

    a= int(input())
    b= int(input())
    add= a+b
    sub= a-b
    prod= a*b
    if (a>=1 and a<= (10**10) ) and (b>=1 and b<= (10**10) ):
         print(add)
         print(sub)
         print(prod)

#task4
    a= float(input())
    b= float(input())
    div_int= int(a/b)
    div_float= float(a/b)

    print(int(div_int))
    print(float(div_float))


#task5

n= int(input())
if n>=1 and n<=20:
    i=list(range(n))

    square= [m ** 2 for m in i]

    print(*square, sep='\n')
#to print a list element each in a seperate line you write it
#like print(*listname, seperate= '\n)
#            (each element, then go to new line ) tuple helps you do this


#task6

def is_leap(year):  
    if year%400==0:
        return True
    elif year%100==0:
        return False
    elif year%4==0:
        return True
    else:
        return False
year = int(input())
print(is_leap(year))


#test7
n= int(input())
i = range(1,n+1)
print(*i,sep='')

#test 10

x = int(input())
y = int(input())
z = int(input())
n = int(input())
    

range_of_x= range(x+1)
range_of_y= range(y+1)
range_of_z= range(z+1)

# result=[]

# for x in range_of_x:
#     for y in range_of_y:
#         for z in range_of_z:
#           if x+y+z!=n:
#             result.append([x,y,z])
        
# print(result)

print([[x,y,z] for x in range_of_x for y in range_of_y for z in range_of_z if x+y+z!=n] )