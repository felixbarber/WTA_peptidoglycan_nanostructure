%ImageAlign.m
%Rico Rojas, 1/21/19
%Registers image stacks using a common reference stack.  

%INSTRUCTIONS FOR USE:
%Save each image stack you want to register in separate directories.  Also
%save the reference image stack (which contains features from which it is 
%possible to track drift) in its own directory.  The program will create
%new directories for each of the image stacks to be registered in the same
%parent directory.  The reference stacks and the stacks to be registered
%should have the same number of images.

%INPUT
%basename: choose a name for the directories in which the aligned images
%          will be saved.
%dirname:  cell array containing the paths of the directories in which the
%          image stacks to be registered are.
%regname:  path of reference directory.

%CALLS ON:
%dftregistration.m
%imtranslate.m

% Modified 9/21/2020 by Felix Barber to perform manipulation on multiple
% scenes at once.

clear
close all



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%User Input
%num_scenes = 5;
%basename1='200916_BS_fos';

%num_scenes = 5;
%basename1 = '200928_BS_tun_test';

% num_scenes = 4;
% basename1 = '201013_BS_tun_fos';

% num_scenes = 5;
% basename1 = '201023_BS_cerulenin';
% 
% num_scenes = 5;
% basename1 = '201112_BS_tun_fos_simult';
% 
% num_scenes = 5;
% basename1 = '201112_BS_tun_fos_delay';
% 
% num_scenes = 5;
% basename1 = '201115_BS_fos';

% num_scenes = 5;
% basename1 = '201115_BS_fos_recovery';

% num_scenes = 9;
% basename1 = '201120_LM_fos';

% num_scenes = 10;
% basename1 = '201121_LM_tun';

% num_scenes = 3;
% basename1 = '210108_BS_tun';
% 
% num_scenes = 5;
% basename1 = '210128_FB2_Tun_response';


% num_scenes = 5;
% basename1 = '210212_FB1_LB_Tun_response';


% num_scenes = 5;
% basename1 = '210217_FB1_ER43_LB_HADA_expt1';

% num_scenes = 5;
% basename1 = '210217_FB1_ER43_LB_HADA_expt2';

% num_scenes = 6;
% basename1 = '210212_FB1_LB_Tun_response_HADA';
% 
% num_scenes = 6;
% basename1 = '210304_FB1_LB_HADA';
% num_channels=3; 

% num_scenes = 6;
% basename1 = '210304_FB1_LB_Tun_response_HADA';
% 
% num_scenes=4;
% basename1='191216_Paola_CRISPRi_TagO';

% num_scenes=8;
% basename1='210401_BS168_LB_HADA';

% num_scenes=5;
% basename1='210401_BS168_Tun_HADA_expt4';

% num_scenes = 5;
% basename1 = '210416_FB2_Tun_response';


% num_scenes=6;
% basename1='210429_FB6_inducer_loss';
% 
% num_scenes=6;
% basename1='210506_FB6_inducer_loss_timelapse';


% num_scenes=3;
% basename1='210718_FB1_Tun_Response';

% num_scenes=5;
% basename1='210718_FB8_Tun_Response';

% num_scenes=8;
% basename1='210723_FB8_Tun_Response';

% num_scenes=7;
% basename1='210723_FB7_Tun_Response';

% num_scenes=7;
% basename1='210723_FB1_Tun_Response';

% num_scenes=8;
% basename1='210916_bFB1_PBS_recovery';


num_scenes=6;
basename1='210916_bFB1_PBS_teichoicase_recovery';


% This doesn't usually change

regname=['D:/Documents_D/Rojas_lab/data/' basename1 '/' basename1 '_reg' ];
for i0 =1:num_scenes
    basename=strcat(basename1,'_s',sprintf('%03d',i0));
    dirname={['D:/Documents_D/Rojas_lab/data/' basename1 '/' basename '_C1'];
            ['D:/Documents_D/Rojas_lab/data/' basename1 '/' basename '_C2']};
   
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    workdir=pwd;
    ld=length(dirname);

    cd(regname)
    directory=dir('*.tif');
    path(regname,path)
    T=length(directory);
    tf=T*ld;

    imagename=directory(1).name;
    RefIm=imread([regname '/' imagename]);

    count=0;
    for i=1:ld

        cd(dirname{i})
        path(dirname{i},path)
        directory2=dir('*.tif');
        cd('../')

        mkdir([basename '_' num2str(i) '_a'])
        cd(['./' basename '_' num2str(i) '_a'])

        shft=zeros(T,2);

        for t=1:T
            count=count+1;
            pd=count/tf*100;
            pds=sprintf(['%4.1f'],pd);
            [pds '%']

            imagename=directory(t).name;
            TestIm=imread([regname '/' imagename]);

            [output NewImFT]=dftregistration(fft2(RefIm),fft2(TestIm),10);
            NewIm=abs(ifft2(NewImFT));

            shft(t+1,1)=output(3);
            shft(t+1,2)=output(4);

            imagename=directory2(t).name;

            I=imread([dirname{i} '/' imagename]);
            [counts,bins]=imhist(I);
            [~,maxpos]=max(counts);
            padcolor=bins(maxpos);

            I=imtranslate(I,shft(t+1,:),padcolor);

            b=sprintf(['%4.4d'],t);  
            savename=[basename '_a' b '.tif'];

            imwrite(I,savename);
        end
    end

    cd(workdir);
end
 