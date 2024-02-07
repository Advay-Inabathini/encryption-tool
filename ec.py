#program to implement elleptical curve

print("y^2 modp = (x^3 + x + 1)modp")

p = int(input("enter p: "))

print("\nvalue\t y^2 mod p\t (x^3+x+1) mod p")
for i in range(0, p):
	print(i,"\t",(i**2)%p,"\t\t", (i**3+i+1)%p)

