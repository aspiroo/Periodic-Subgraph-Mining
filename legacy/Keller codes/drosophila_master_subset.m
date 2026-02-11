clear;
close all;

dismat = [5,1,0.5,0.2,0.1];
cmat = 10.^[-1:0.1:0.5, -1.5, -2.0, -3.0];

fid = fopen('submit.drosophila_subset.txt', 'w');
fprintf(fid, 'user = lesong\n');
fprintf(fid, 'executable = runmatlab.sh\n');
fprintf(fid, 'universe = vanilla\n');
fprintf(fid, 'getenv = true\n');
fprintf(fid, 'arguments = drosophila_subset(''$(fname)'',$(di),$(ci),$(isreweight),$(s),$(e),''$(fidx)'',''$(suffix)'') $(output)\n\n');

fidx = '../python/transcriptional_factor.txt';
idx = load(fidx);

suffix = 'tf';

fname = '../drosophila/drosophila';    

load([fname, '.mat']);
data = data(idx,:);
[n, m] = size(data);
P = n;
smat = [1:50:P];
emat = [smat(2:end)-1,P];

for di = 3 %1:length(dismat)
for ci = 17:19 % 1:length(cmat)
for nno = 1:length(smat)

    fprintf(1, '--generating %s, %d %d\n', fname, di, ci);
    
    if (di == 1)
        isreweight = 0;
        fprintf(fid, 'fname = %s\n', fname); 
        fprintf(fid, 'di = %d\n', 1);
        fprintf(fid, 'ci = %d\n', ci);
        fprintf(fid, 'isreweight = %d\n', isreweight);
        fprintf(fid, 's = %d\n', smat(nno));
        fprintf(fid, 'e = %d\n', emat(nno));
        fprintf(fid, 'fidx = %s\n', fidx);
        fprintf(fid, 'suffix = %s\n', suffix);        
        fprintf(fid, 'output = %s_d%d_c%d_i%d_s%d_e%d_output.txt\n', fname, 1, ci, isreweight, smat(nno), emat(nno));
        fprintf(fid, 'error = %s_d%d_c%d_i%d_s%d_e%d_error.txt\n', fname, 1, ci, isreweight, smat(nno), emat(nno));
        fprintf(fid, 'log = %s_d%d_c%d_i%d_s%d_e%d_log.txt\n', fname, 1, ci, isreweight, smat(nno), emat(nno));
        fprintf(fid, 'queue\n\n');                    
    end

    isreweight = 1;
    fprintf(fid, 'fname = %s\n', fname); 
    fprintf(fid, 'di = %d\n', di);
    fprintf(fid, 'ci = %d\n', ci);
    fprintf(fid, 'isreweight = %d\n', isreweight);
    fprintf(fid, 's = %d\n', smat(nno));
    fprintf(fid, 'e = %d\n', emat(nno));   
    fprintf(fid, 'fidx = %s\n', fidx);    
    fprintf(fid, 'suffix = %s\n', suffix);            
    fprintf(fid, 'output = %s_d%d_c%d_i%d_s%d_e%d_output.txt\n', fname, di, ci, isreweight, smat(nno), emat(nno));
    fprintf(fid, 'error = %s_d%d_c%d_i%d_s%d_e%d_error.txt\n', fname, di, ci, isreweight, smat(nno), emat(nno));
    fprintf(fid, 'log = %s_d%d_c%d_i%d_s%d_e%d_log.txt\n', fname, di, ci, isreweight, smat(nno), emat(nno));
    fprintf(fid, 'queue\n\n');                            
end
end
end

fclose(fid);
