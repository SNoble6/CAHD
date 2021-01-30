clf(figure(1));
clear;
clc;
fileID = fopen('time_value_no_rcm.txt', 'r');
formatSpec = '%f';
time = fscanf(fileID, formatSpec);
time = time.';
%fclose(fileID);
%fileID = fopen('kl_divergence_value_10_m_BMS2.txt', 'r');
%kl = fscanf(fileID, formatSpec);
%fclose(fileID);
%kl = kl.';
fileID = fopen('parameters_value_10_p.txt', 'r');
formatSpec = '%i';
parameters = fscanf(fileID, formatSpec);
fclose(fileID);
parameters = parameters.';

figure(1);
hold on;
h = plot(parameters, time, 'o', 'color', 'red');
set(h, 'MarkerFaceColor', get(h, 'Color'));
plot(parameters, time, 'color', 'red')
% axis([0 0.5 4 20]);
axis padded;
title('BMS1')
xlabel('p')
ylabel('Time')

fileID = fopen('time_value_rcm.txt', 'r');
formatSpec = '%f';
time = fscanf(fileID, formatSpec);
time = time.';
fclose(fileID);
%fileID = fopen('kl_divergence_value_20_m_BMS2.txt', 'r');
%kl = fscanf(fileID, formatSpec);
%fclose(fileID);
%kl = kl.';
fileID = fopen('parameters_value_10_p.txt', 'r');
formatSpec = '%i';
parameters = fscanf(fileID, formatSpec);
fclose(fileID);
parameters = parameters.';

h = plot(parameters, time, 'square', 'color', 'blue');
set(h, 'MarkerFaceColor', get(h, 'Color'));
plot(parameters, time, 'color', 'blue')
legend('', 'no rcm', '', 'rcm')
%axis([4 20 0 0.4]);







