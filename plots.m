close all

% Load the data from MuboKAP output file into a matrix
% (The first rows have been removed)
data = load('GaitAnalysisModel copy.out');

% Create a time vector
t = data(:,1);

% Remove 10 frames from the end and the beginning to get one stride
t = t(11:end-10);

% Scaling the time vector
a = min(t);
b = max(t);
t = (t - a) / (b - a) * 100;

% Create a matrix containing the positions, velocities and accelerations of
% all bodies

s = data(:,2:end);


% The orientations of right thigh, shank and foot and the trunk (bodies 7,8,9 and 1)

ang1 = s(:,2);
ang1 = ang1(11:end-10);

ang7 = s(:,57);
ang7 = ang7(11:end-10);

ang8 = s(:,66);
ang8 = ang8(11:end-10);

ang9=s(:,75);
ang9 = ang9(11:end-10);


%Convert radians into degrees
ang7 = ang7*(180/pi);
ang8 = ang8*(180/pi);
ang1 =ang1*(180/pi);
ang9 = ang9*(180/pi);




% calculating the knee and hip angle
thetas_knee = ang8-ang7;

thetas_hip = ang1-(ang7-180);

% loading the data from literature
% the data is obtained by using WebPlotDigiziter

data = readmatrix('Dataset_knee.csv');
time_d = data(:,1);   % first column
angle_d = data(:,2);  % second column

% plot the knee flexion angle with respect to stride together with the
% literature plot
figure
plot(t,thetas_knee)
title('Flexion of the knee','FontSize',20)
xlabel('Stride (%)','FontSize',19)
ylabel('Angle (deg)','FontSize',19)
hold on
plot(time_d,angle_d);


data = readmatrix('Dataset_hip.csv');
time_d = data(:,1);   % first column
angle_d = data(:,2);  % second column

figure
plot(t,thetas_hip)
title('Flexion of the hip','FontSize',20)
xlabel('Stride (%)','FontSize',19)
ylabel('Angle (deg)','FontSize',20)
hold on
plot(time_d,angle_d)


% Ankle

% From the data we can see that the the foot is flat at time step t=0,66 s
% The orientation of the foot is then 204.0514° (24.0514°)
ang9(57)-180

ang13 = s(:,111);
ang13 = ang13*(180/pi);

thetas_ankle = ang8-ang9+24-90


data = readmatrix('Dataset_ankle.csv');
time_d = data(:,1);   % first column
angle_d = data(:,2);  % second column


figure
plot(t,thetas_ankle)
title('Joint angle of the ankle','FontSize',20)
xlabel('Sride (%)','FontSize',19)
ylabel('Angle (deg)','FontSize',19)
hold on
plot(time_d,angle_d)



