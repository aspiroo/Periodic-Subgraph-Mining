numfiles = 66;

for k = 1:numfiles
  myfilename = sprintf('drosophila_subset_t%d.mat', k);
  load(myfilename);
  [row col v] = find(G);
  dlmwrite(sprintf('drosophila_subset_t%d.txt', k),[row col], 'delimiter', '\t','newline','pc');
end