close all; clc;
set(groot, "DefaultFigureRenderer", "painters");
set(groot, "DefaultFigureColor", [1 1 1]);
addpath("export_fig");
%%

avg30 = mean([ 54.6, 55.42 ])
avg35 = mean([ 47.49, 48.21, 48.15, 48.10 ])
avg40 = mean([ 42.26, 43.23, 43.83, 42.75, 42.94, 43.03 ])
avg45 = mean([ 39.02, 39.06, 38.50, 38.85, 38.64, 38.97, 38.76, 39.01, 38.19 ])
avg50 = mean([ 39.02, 39.06, 38.50, 38.85, 38.64, 38.97, 38.76, 39.01, 38.19 ])
avg55 = mean([ 33.81 ])

data = readmatrix("push_can2.csv")

num_reps = [];
for n = 30:5:55
   num_reps = [num_reps ; n mean(data(data(:,1) == n, 2)) mean(data(data(:,1) == n, 3))]
end

figure("Position", [0 0 500 300])
bar(num_reps(:, 1), [num_reps(:, 2), num_reps(:, 3)])
% title("Mobile robot push can experiments")
legend(["Number of repitions before failure" "Time per repitition [s]"])
xlabel("Speed %")

export_fig("../img/push-can-data.pdf")
