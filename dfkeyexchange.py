# Diffie-Hellman Code


P = int(input("enter prime number: "))
G = int(input("enter generator: "))
# Private Keys
x1, x2 = int(input("Enter The Private Key Of User 1 : ")), int(
	input("Enter The Private Key Of User 2 : "))
while 1:
	if x1 >= P or x2 >= P:
		print(f"Private Key Of Both The Users Should Be Less Than {P}!")
		continue
	break

# Calculate Public Keys
y1 = (G**x1)%P
y2 = (G**x2)%P

# Generate Secret Keys
k1 = (y2**x1)%P
k2 = (y1**x2)%P

print(f"\nSecret Key For User 1 Is {k1}\nSecret Key For User 2 Is {k2}\n")

if k1 == k2:
	print("Keys Have Been Exchanged Successfully")
else:
	print("Keys Have Not Been Exchanged Successfully")

