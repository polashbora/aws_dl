
x=[11,12,13]
y=[21,22,23]

z = (zip(x,y))
print(z)

m=0
for n in z:
    print(m,n[0],n[1])
    m=m+1