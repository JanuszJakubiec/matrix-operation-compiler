a = 5;
b = 7;
c = a + b;
print a;
d = zeros(5 - 4 + 3);
h = ones(4);
h = h .* 10;
d = d .+ 1;
d[1,1] = 200;
j = d + h;
print j;
g = d * j;
print g;
print b;
while(c < 100)
{
    a = a + 1;
    print a;
    if(a == 12)
        print "TEST";
    else
        print "XYZXYYZ";
    if(a == 13)
        break;
    c = c + 10;
    print c;
}
return c;