function drosophila_subset(fname, di, ci, isreweight, Pidx1, Pidx2, fidx, suffix) 

Pidx = [Pidx1:Pidx2];

dismat = [5,1,0.5,0.2,0.1];
% cmat = 10.^[-1.0:0.1:0.5];
cmat = 10.^[-1:0.1:0.5, -1.5, -2.0, -3.0];

idx = load(fidx);

load([fname, '.mat']);
data = data(idx,:);
[n, m] = size(data);
P = n;

t = (1:m)'./m;
tdis = pdist(t).^2;
mdis = dismat(di) * median(tdis)
K = squareform(exp(-tdis./mdis)) + eye(m);

up = [1:m];
if (isreweight < 1)
    K(:) = 1;
    up = 1;
end

c = cmat(ci);       
lambda = c/(sqrt(m))
M = ones(1, m)./m;

wmatcell = {};

for j = up
    fprintf(1, '--experiement (%d, %d, %f)\n', m, j, lambda);            
    tic
    wmat = []; 

    MM = M .* K(j,:) ./ sum(K(j,:));
    tmpdata = [(0:m-1)', MM', data'];
    inputname = [fname, '_d', int2str(di), '_c', int2str(ci), '_i', int2str(isreweight), '_s', int2str(Pidx1), '_e', int2str(Pidx2), '.data'];
    outputname = [fname, '_d', int2str(di), '_c', int2str(ci), '_i', int2str(isreweight), '_s', int2str(Pidx1), '_e', int2str(Pidx2), '.wmat'];
    savematrix([P, m, m], inputname, '%d ');
    savematrix(tmpdata, inputname, '%g ', 1);
%     cmdstr = ['export LD_LIBRARY_PATH=~/Tools/Ipopt-3.5.2/build/lib/; ', ...
%         '../Release/Teslor ../src/ipopt.opt ', ...
%         inputname, ' ', outputname, ' ', num2str(lambda), ...
%         ' ', int2str(Pidx1-1), ' ', int2str(Pidx2)];
    cmdstr = ['export LD_LIBRARY_PATH=/usr1/lesong/lib/; ', ...
        '../Release/Teslor ../src/ipopt.opt ', ...
        inputname, ' ', outputname, ' ', num2str(lambda), ...
        ' ', int2str(Pidx1-1), ' ', int2str(Pidx2)];
    unix(cmdstr);
    wmat = load(outputname)';
    
    wmatcell{j} = wmat;
    toc
end

save([fname, '_d', int2str(di), '_c', int2str(ci), ...
    '_i', int2str(isreweight), ...
    '_s', int2str(Pidx1), ...
    '_e', int2str(Pidx2), ...
    '_', suffix, '.mat'], 'wmatcell');
    
