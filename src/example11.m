a = zeros(5);
b = ones(5);
b[1,2] = 1;
b[2,4] = a[1,1] / b[2,3] + 5;
g = b[1,1];
print zeros(4)[2,2];
v = a + b;
y = [ [1,2,3,4,5],
      [1,2,3,4,5] ];
b = [ [1,2,3,4],
      [1,2,3,4],
      [1,2,3,4],
      [1,2,3,4],
      [1,2,3,4] ];
c = y * b;
h = c + b;
j = b .+ 5;
h = b * j;
b += b;
a = 5;
b = a';
a = zeros(4);
c = -a;
d = a';
a = "aaaaa";
b = -a;
