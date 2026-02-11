% run keller with development genes;

load ../data/drosophila.mat
idx = load('../data/Just_development.txt');
data = data(idx,:);

Gcell = keller(data); 

