close all
clear all

own_data_a1= readmatrix('ankle_moment_test1.csv');
time_own = own_data_a1(:,1);   
values_own_a1 = own_data_a1(:,2);  


own_data_k= readmatrix('knee_moment_test.csv');
values_own_k = own_data_k(:,2);  

own_data_h= readmatrix('hip_moment_test.csv'); 
values_own_h = own_data_h(:,2);  

lit_data_a= readmatrix('Ankle_moment_winter.csv');
time_lit_a = lit_data_a(:,1);   
values_lit_a = lit_data_a(:,2);  

lit_data_k = readmatrix('knee_moment_winter.csv')
time_lit_k = lit_data_k(:,1);   
values_lit_k = lit_data_k(:,2); 

lit_data_h = readmatrix('hip_moment_winter.csv')
time_lit_h = lit_data_h(:,1);   
values_lit_h = lit_data_h(:,2); 


% Red: from the literature
% Blue: own data
figure
plot(time_own,values_own_a1,'b')
hold on
plot(time_lit_a,values_lit_a,'r')
grid on
hold off



figure
plot(time_lit_k,values_lit_k,'r')
grid on
ylim([-0.7 0.5])
xlim([0,100])
hold on
plot(time_own,values_own_k,'b')
hold off

figure
plot(time_lit_h,values_lit_h,'r')
grid on
hold on
plot(time_own,values_own_h,'b')