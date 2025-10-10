close all

% Load the data from MuboKAP output file into a matrix
% (The first rows have been removed)
data = load('PlankAnalysisModel.out');

% Create a time vector
t = data(:,1);

% Create a matrix containing the positions, velocities and accelerations of
% all bodies

s = data(:,2:end);

% Get the orientations of the trunk, left thigh and left shank (bodies 1, 11 and 12):

ang1 = s(:,2);
ang11 = s(:,93);
ang12 = s(:,102)


%Convert into degrees

ang1 = ang1*(180/pi);
ang11 = ang11*(180/pi);
ang12 = ang12*(180/pi);

%Calculate the hip angle:
thetas_hip = ang11-ang1-180;

%Calculate the knee angle:
thetas_knee = ang11-ang12

% getting the maximum and minimum angles of the hip hyper extension
min(thetas_hip)
max(thetas_hip)

% plot the knee and hip angles
figure
plot(t,thetas_hip)
title('Flexion of the hip','FontSize',20)
xlabel('time (s)','FontSize',19)
ylabel('Angle (deg)','FontSize',19)

figure
plot(t,thetas_knee)
title('Flexion of the knee','FontSize',20)
xlabel('time (s)','FontSize',19)
ylabel('Angle (deg)','FontSize',19)




















