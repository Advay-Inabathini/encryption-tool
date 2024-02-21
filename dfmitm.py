#jowein francis
p = int(input("enter prime number: "))
x,y = [int(i) for i in input("enter x and y values: ").split()]

for i in range(2, p):
	tmp, flag = [], False
	for j in range(1, p-1):
		if (i**j)%p in tmp:
			flag = True
			break
		tmp.append((i**j)%p)
	if flag:
		continue
	g = i
	break

print(g, "\n")

mitm = True if input("Is there a man in the middle: ").lower()=='y' else False

if mitm :
	x1, y1 = [int(i) for i in input("enter x and y values for the man: ").split()]
	ska = pow(pow(g, y1)%p, x)%p
	skb = pow(pow(g, x1)%p, y)%p

else:
	ska = pow(pow(g, y)%p,x)%p
	skb = pow(pow(g, x)%p,y)%p

print("secret key of a: ", ska, "\nsecret key of b: ", skb)
