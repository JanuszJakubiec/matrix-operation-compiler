a = zeros(5);
b = ones(5);
b[1,2] = 1;
b[2,4] = a[1,1] / b[2,3] + 5;
g = b[1,1];
print zeros(4)[2,2];
v = a + b;
y = [ [1,2,3,4,5],
      [1,2,3,4,4] ];
b = [ [1,2,3,4],
      [1,2,3,4],
      [1,2,3,4],
      [1,2,3,4],
      [1,2,3,4] ];
c = y * b;
print c;
j = [[1,1,1,1],
     [2,2,2,2]];
print j+c;
print (j+c)';
print c';
h = c + b;
j = b .+ 5;
h = b * j;
b += b;
b = zeros(5);
b = a';
a = zeros(4);
d = a';
