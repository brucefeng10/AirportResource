%{
a=xlsread('C:\Users\Admin\Desktop\zhongzhi2\attribute.xlsx','company','A1:JN5901');
b=xlsread('C:\Users\Admin\Desktop\zhongzhi2\attribute.xlsx','task','A1:JN5901');
c=xlsread('C:\Users\Admin\Desktop\zhongzhi2\attribute.xlsx','inter','A1:JN5901');
d=xlsread('C:\Users\Admin\Desktop\zhongzhi2\attribute.xlsx','type','A1:JN5901');
m=size(a,1)
n=size(a,2)
summ=zeros(m,n);
for i=1:m
    for k=1:n
        if a(i,k)+b(i,k)+c(i,k)+d(i,k)==4
            summ(i,k)=1;
        end
    end
end

xlswrite('C:\Users\Admin\Desktop\zhongzhi2\attribute.xlsx',summ,'summ');
%}
a=xlsread('C:\Users\Admin\Desktop\zhongzhi2\result\result13.7.xlsx','nolinshi','C2:C5902');
b=ones(5901,274);
for i = 1:5901
    if a(i)>=1
        for k=206:274
            b(i,k)=0;
        end
    end
end
xlswrite('C:\Users\Admin\Desktop\solution.xlsx',b,'is_normal_137');
%{
%a=xlsread('C:\Users\Admin\Desktop\zhongzhi2\result\result13.7.xlsx','nolinshi','A2:A5902');
b=xlsread('C:\Users\Admin\Desktop\zhongzhi2\result\result13.7.xlsx','nolinshi','C2:C5902');
sol=zeros(5901,274);
for i=1:5901
    if b(i)>0
        sol(i,b(i))=1;
    end
end
xlswrite('C:\Users\Admin\Desktop\solution.xlsx',sol,'sol13.7');
%}