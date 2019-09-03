
%临时措施的三个冲突矩阵
a=xlsread('C:\Users\Admin\Desktop\zhongzhi2\attribute.xlsx','hangban','C2:C5902');
b=xlsread('C:\Users\Admin\Desktop\zhongzhi2\attribute.xlsx','hangban','D2:D5902');
n=size(a,1)
ls=ones(n,n);%临时机位时序限制情况下的冲突矩阵;i表示影响别人的航班，j表示受影响的航班
for i=1:n
    for j=1:n
        if a(j)>a(i) && a(j)<b(i)
            ls(i,j)=0;
        elseif b(j)>a(i) && b(j)<b(i)
            ls(i,j)=0;
        end
    end
end

fz=ones(n,n);%公务机坪父子机位;i表示影响别人的航班，j表示受影响的航班
for i=1:n
    for j=1:n
        if a(j)>a(i) && a(j)<b(i)
            fz(i,j)=0;
        end
    end
end



%{
b=xlsread('C:\Users\Admin\Desktop\zhongzhi2\attribute.xlsx','hangban','C2:C5902');
c=xlsread('C:\Users\Admin\Desktop\zhongzhi2\attribute.xlsx','hangban','D2:D5902');
a=b-5;
d=c+5;
n=size(b,1)
ct=zeros(n,n);
for i=1:n-1
    for j=i+1:n
        if (a(j)-b(i))*(b(j)-a(i))<0
            ct(i,j)=1;
        elseif (c(j)-b(i))*(d(j)-a(i))<0
            ct(i,j)=1;
        elseif (a(j)-d(i))*(b(j)-c(i))<0
            ct(i,j)=1;
        elseif (c(j)-d(i))*(d(j)-c(i))<0
            ct(i,j)=1;
        end
    end
end

sum(sum(ct))
%}
