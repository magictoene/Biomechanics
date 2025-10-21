close all

own_data= readmatrix('R__GlutMaxMid_lengths.csv');
time = own_data_a(:,1);   
values = own_data_a(:,2);  

figure
plot(time,values)
grid on