function Gcell = keller(data, di, ci, isreweight, Pidx1, Pidx2) 

addpath minFunc;

[n, m] = size(data);

if (nargin < 2)
    di = 3; 
    ci = 18;
    isreweight = 1;
    Pidx1 = 1;
    Pidx2 = n;
end

% select kernel bandwidth;
dismat = [5,1,0.5,0.2,0.1];
% select regularization parameter;
cmat = 10.^[-1:0.1:0.5, -1.5, -2.0, -3.0, -4.0, -5.0, -6.0];
% select the genes to run;
Pidx = [Pidx1:Pidx2];

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
fprintf(1, '--regularization parameter = %g, bandwidth = %g median distance\n', c, dismat(di));
c = c/(sqrt(m));
M = ones(1, m)./m;

w_init = zeros(n,1);
Gcell = {};
for j = up
    wmat = zeros(n,length(Pidx)); 

    kw = M .* K(j,:) ./ sum(K(j,:));
    kw = kw';
    
    for i = Pidx
        fprintf(1, '--time point %d, gene %d\n', j, i);
        lambda = c*ones(n,1);
        lambda(i) = 0; % Do not penalize bias variable
        y = data(i,:)';
        X = data';
        X(:,i) = 1;
        funObj = @(w)wLogisticLoss(w,X,y,kw);
        options.order = -1; % Turn on using L-BFGS
        w = L1GeneralProjection(funObj,w_init,lambda,options);        
        wmat(:,i-Pidx(1)+1) = w;
    end

    G = sparse(n, n);    
    G(:,Pidx) = (abs(wmat) > 1e-3);
    G = (G | G');    
    G = G - diag(diag(G));
    Gcell{j} = G;
end

save('result.mat', 'Gcell');

