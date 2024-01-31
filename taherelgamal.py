import random
import time

def generators(n):
    s = set(range(1, n))
    results = []
    for a in s:
        g = set()
        for x in s:
            g.add((a**x) % n)
        if g == s:
            results.append(a)
    return results

def gcd(a,b):
	if a==0:
		return b
	return (gcd(b%a, a))

p = int(input("enter a prime number:"))
begin = time.time()
e1 = -1

for i in generators(p):
	if(gcd(i,p)==1):
		e1 = i
		break

d = random.randint(e1+1,p-2)
e2 = pow(e1,d,p)
M = int(input("enter plain text:"))

while(M>p):
	M = int(input("enter correct plain text:"))

r = int(random.random())
C1 = int(pow(e1,r,p))
C2 = M*(int(pow(e2,r)))%p

print(f"C1 is {C1} and C2 is {C2}")

P = C2*(int(pow(int(pow(C1,d)),-1,p)))
P = P%p
print("P:",P)
end = time.time()
print(f"Total time of the program is {end - begin}")
