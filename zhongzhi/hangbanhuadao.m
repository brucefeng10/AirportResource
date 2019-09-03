%whether flight i can use huadao t
clear;
hdtype=xlsread('C:\Users\suqiang\Desktop\bianhao.xlsx','source','AC2:AC203');
summ=xlsread('C:\Users\suqiang\Desktop\bianhao.xlsx','summ','A1:GT690');
hbhd=zeros(690,27);
for i=1:690
    for k=1:202
        if summ(i,k)==1
            hbhd(i,hdtype(k))=1;
        end
    end
end
xlswrite('C:\Users\suqiang\Desktop\result.xlsx',hbhd,'hbhd');