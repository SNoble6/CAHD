clf(figure(1));
clear;
clc;
fileID = fopen('final_kl_fake.txt', 'r');
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
h = plot(parameters, time, 'o', 'color', 'black');
set(h, 'MarkerFaceColor', get(h, 'Color'));
plot(parameters, time, 'color', 'black')
% axis([0 0.5 4 20]);
axis padded;
title('BMS1')
xlabel('p')
ylabel('KL-Divergence')

fileID = fopen('final_kl_true.txt', 'r');
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
plot(parameters, time, 'color', 'blue');
legend('', 'fake items', '', 'no fake items');
%axis([4 20 0 1000]);

