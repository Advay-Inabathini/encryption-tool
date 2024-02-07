#program to implement point doubling of elleptical curve cryptography
import time
def mod_Inv(x,y):
    for i in range(y):
        if (x*i)%y==1:
            return i
start = time.time()
p = int(input("enter p of finite field: "))
a = int(input("enter coefficient of curve equation(a): "))
print("\n")
x1 = int(input("enter x coordinate of given point: "))
y1 = int(input("enter y coordinate of given point: "))

lnum = (3*(x1**2)+a)%p
ldenom = mod_Inv(2*y1,p)

l = (lnum*ldenom)%p

x3 = ((l**2)-(2*x1))%p
y3 = (l*(x1-x3)-y1)%p
end = time.time()

print("point doubling: ")
print("lambda:", l)
print(x3,",", y3) 
print("execution time:", end-start)
