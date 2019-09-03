


%considering all the three objectives
%we consider the third objective with some weights in the objective function
tic
tic
clear;

%time match
alpha=xlsread('C:\Users\suqiang\Desktop\bianhao.xlsx','timematch','A1:ZN690');

summ=xlsread('C:\Users\suqiang\Desktop\bianhao.xlsx','summ','A1:GT690');
hbhd=xlsread('C:\Users\suqiang\Desktop\bianhao.xlsx','hbhd','A1:AA690');%航班能否停在此滑道
s_near=xlsread('C:\Users\suqiang\Desktop\bianhao.xlsx','source','X2:X203');
hdtime=xlsread('C:\Users\suqiang\Desktop\bianhao.xlsx','hdmatch','A1:ZN690');
hdtype=xlsread('C:\Users\suqiang\Desktop\bianhao.xlsx','source','AC2:AC203');
%xlswrite('C:\Users\Admin\Desktop\result3.xlsx',solution,'solution80');

m=20;
n=202;
r=27;

M=10;
e=0.1;
t0=toc

tic

f=[];
x=binvar(m,n);
y=binvar(m,r);
z=binvar(m,m,r,'full');
s=binvar(m,1);

dia=diag(ones(1,m));
dib=1-dia;

%objective

ob1=0;
ob2=0;
ob3=m;
ob1=sum(sum(x));
ob2=sum(x*s_near);
ob3=m-sum(s);
obj=-(3*ob1+2*ob2+ob3)/m;
%ao=0
to=toc

tic
sum0=zeros(m,m);
for t=2:r
    sum0=sum0+hdtime(1:m,1:m).*z(:,:,t);
end
for j=1:m
    f=f+[s>=sum0(:,j)];
    f=f+[s'>=sum0(j,:)];
end
t1=toc

tic
A=zeros(m,m);
B=zeros(m,m);
for t=1:r
    A=repmat(y(:,t),1,m);
    B=repmat(y(:,t)',m,1);
    for i=1:m
        f=f+[M*(z(i,:,t)+dia(i,:))-e>=A(i,:)+B(i,:)-2];
        f=f+[M*(z(i,:,t).*dib(i,:)-1)<=A(i,:)+B(i,:)-2];
    end
end
t2=toc

tic
for i=1:m
    sum11=0;
    sum12=0;
    for t=1:r
        sum11=sum11+y(i,t)*t;
    end
    for k=1:n
        sum12=sum12+x(i,k)*hdtype(k);
    end
    f=f+[sum11==sum12];
end
%ac=3
t3=toc

tic
f=f+[x<=summ(1:m,:)];
f=f+[sum(x,2)<=1];
f=f+[sum(y,2)<=1];
%ac=4
t4=toc


tic
C=zeros(m,m);
D=zeros(m,m);
for k=1:n
    C=repmat(x(:,k),1,m);
    D=repmat(x(:,k)',m,1);
    for i=1:m
        f=f+[C(i,:)+D(i,:)<=1+alpha(i,1:m)];
    end
end
%ac=6
t6=toc




options = sdpsettings('solver', 'cplex', 'cplex.timelimit', 17200);
%options=sdpsettings('verbose',1,'solver','cplex','cplex.qpmethod',1);
sol=optimize(f,obj,options);
if sol.problem == 0
    % Extract and display value
    %xlswrite('C:\Users\Flash\Desktop\ncovering.xlsx',y,'y');
    objective=-value(obj)
    object12=value(ob1+ob2)
    solution=value(x);
    
else
    display('Hmm, something went wrong!');
    sol.info
    yalmiperror(sol.problem)
end


t=toc