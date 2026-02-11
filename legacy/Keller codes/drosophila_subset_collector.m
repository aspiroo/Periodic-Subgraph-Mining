clear;
close all;

% dismat = [1,2,0.5,0.2,5]; %[0.2,0.5,1,2,5];
% cmat = 10.^[-1.0:0.1:0.5];
% cmat = 10.^[-1.5:0.1:0.5];

fname = '../drosophila/drosophila';    

% fidx = '../python/Just_development.txt';
fidx = '../python/transcriptional_factor.txt';
idx = load(fidx);

suffix = 'tf';

load([fname, '.mat']);
data = data(idx,:);
[n, m] = size(data);
% n = 4028; m = 66;
P = n;
clear data;
smat = [1:50:P];
emat = [smat(2:end)-1,P];

G = [];
for di = 3 % 1:length(dismat)
for ci = 18 % 1:length(cmat)    
        for nno = 1:length(smat)
            isreweight = 1;
            curname = [fname, '_d', int2str(di), '_c', int2str(ci), ...
                '_i', int2str(isreweight), ...
                '_s', int2str(smat(nno)), ...
                '_e', int2str(emat(nno)), ...
                '_', suffix, '.mat'];
            load(curname);
                        
            for t = 1:m         
                fprintf(1, '--processing time %d, node: %d\n', t, smat(nno));
                curname = [fname, '_', suffix, '_t', int2str(t)];                

                if (nno == 1)
                    G = zeros(P, P);
                    G = sparse(G);
                else
                    load(curname);
                end
                
                G(:, [smat(nno):emat(nno)]) = (abs(wmatcell{t}) > 1e-3);
                
                if (nno == length(smat))
                    G = (G | G');
                end
                                
                save(curname, 'G');
            end
            
            clear wmatcell;                 
        end
end
end
