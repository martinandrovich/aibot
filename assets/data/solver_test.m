close all; clc;
set(groot, "DefaultFigureRenderer", "painters");
set(groot, "DefaultFigureColor", [1 1 1]);
addpath("export_fig");
%%

data = readmatrix("solver_stats.csv")

data_solved = data(data(:,3)~=-1.0,:);
data_unsolved = data(data(:,3)==-1.0,:);

figure("Position", [0 0 500 300])
scatter(data_solved(:, 2), data_solved(:, 3))
hold on
scatter(data_unsolved(:, 2), data_unsolved(:, 3))
legend(["Solved", "Unsolved"])
xlabel("Number of cans")
ylabel("Time [s]")

export_fig("../img/solver-scatter.pdf")