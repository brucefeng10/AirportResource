


%considering all the three objectives
%we consider the third objective with some weights in the objective function

tic
clear;

%time match
alpha=xlsread('C:\Users\Admin\Desktop\zhongzhi\bianhao.xlsx','timematch','A1:ZN690');

summ=xlsread('C:\Users\Admin\Desktop\zhongzhi\bianhao.xlsx','summ','A1:GT690');
hbhd=xlsread('C:\Users\Admin\Desktop\zhongzhi\bianhao.xlsx','hbhd','A1:AA690');%航班能否停在此滑道
s_near=xlsread('C:\Users\Admin\Desktop\zhongzhi\bianhao.xlsx','source','X2:X203');
hdtime=xlsread('C:\Users\Admin\Desktop\zhongzhi\bianhao.xlsx','hdmatch','A1:ZN690');
hdtype=xlsread('C:\Users\Admin\Desktop\zhongzhi\bianhao.xlsx','source','AC2:AC203');
%xlswrite('C:\Users\Admin\Desktop\result3.xlsx',solution,'solution80');

m=690;
n=202;
r=27;

M=10;
e=0.1;



f=[];
x=binvar(m,n);
y=binvar(m,r);
z=binvar(m,m,r,'full');
s=binvar(m,1);
%objective

ob1=0;
ob2=0;
ob3=m;
for i=1:m
    for k=1:n
        if summ(i,k)==1
            ob1=ob1+x(i,k)*3;
            ob2=ob2+x(i,k)*s_near(k)*2;
        end
    end
    ob3=ob3-s(i);
end
obj=-(ob1+ob2+ob3)/m;
ao=0

for i=1:m-1
    for j=1+i:m
        if hdtime(i,j)==1
            sum0=0;
            for t=2:r
                if hbhd(i,t)==1 && hbhd(j,t)==1
                    sum0=sum0+z(i,j,t);
                end
            end
            f=f+[s(i)>=sum0];
            f=f+[s(j)>=sum0];
        end
    end
end
ac=1

for i=1:m-1
    for t=1:r
        if hbhd(i,t)==1
            for j=1+i:m
                if hbhd(j,t)==1 && hdtime(i,j)==1
                    f=f+[M*z(i,j,t)-e>=y(i,t)+y(j,t)-2];
                    f=f+[M*(z(i,j,t)-1)<=y(i,t)+y(j,t)-2];
                end
            end
        end
    end
end
ac=2

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
ac=3

for i=1:m
    sum1=0;
    for k=1:n
        sum1=sum1+x(i,k);
        if summ(i,k)==0
            f=f+[x(i,k)<=0];
        end
    end
    f=f+[sum1<=1];
end
ac=4

for i=1:m
    sum3=0;
    for t=1:r
        sum3=sum3+y(i,t);
    end
    f=f+[sum3<=1];
end
ac=5

for i=1:m-1
    for k=1:n
        if summ(i,k)==1
            for j=i+1:m
                if summ(j,k)==1 && alpha(i,j)==0%alpha为0表示两航班存在时间冲突
                    f=f+[x(i,k)+x(j,k)<=1];
                end
            end
        end
    end
end
%}
ac=6




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