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
% data_loc='D:/Documents_D/Rojas_lab/data/'
% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/'
% data_loc='/Users/felixbarber/Documents/Rojas_Lab/data/'

num_scenes = 1;
basename1='250515_bFB66_tun_pad';
data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% % num_scenes = 1;
% % basename1='250515_bFB66_LB_pad';
% % data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250514_bFB69_LB_pad_rep2';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250514_bFB69_LB_pad';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250512_bFB66_tun_pad';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250512_bFB66_LB_pad';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250509_bFB66_pad_LB';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250508_bFB69_pad_LB';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250508_bFB66_pad_LB';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250507_bFB66_pad_tun_v2';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250506_bFB66_pad_tun';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250505_bFB66_pad_LB';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'



% This doesn't usually change

for i0 =1:num_scenes
%     regname=['D:/Documents_D/Rojas_lab/data/' basename1 '/' basename1 '_reg_s' sprintf('%03d',i0)];
%     basename=strcat(basename1,'_s',sprintf('%03d',i0));
%     dirname={['D:/Documents_D/Rojas_lab/data/' basename1 '/' basename '_C1'];
%             ['D:/Documents_D/Rojas_lab/data/' basename1 '/' basename '_C2']};
    regname=[data_loc basename1 '/' basename1 '_reg_s' sprintf('%03d',i0)];
    basename=strcat(basename1,'_s',sprintf('%03d',i0));
    dirname={[data_loc basename1 '/' basename '_C1'];
            [data_loc basename1 '/' basename '_C2']};
   
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    workdir=pwd;
    ld=length(dirname);

    cd(regname)
    directory=dir('*.tif');
    path(regname,path)
    T=length(directory);
    tf=T*ld;

    
    count=0;
    for i=1:ld
        imagename=directory(1).name;
        RefIm=imread([regname '/' imagename]);

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
            RefIm=TestIm; % We overwrite the previous reference image
            % to compare neighboring images
            NewIm=abs(ifft2(NewImFT));

            shft(t+1,1)=output(3);
            shft(t+1,2)=output(4);

            imagename=directory2(t).name;

            I=imread([dirname{i} '/' imagename]);
            [counts,bins]=imhist(I);
            [~,maxpos]=max(counts);
            padcolor=bins(maxpos);
            
            shft_cm=cumsum(shft,1);
            I=imtranslate(I,shft_cm(t+1,:),padcolor);

            b=sprintf(['%4.4d'],t);  
            savename=[basename '_a' b '.tif'];

            imwrite(I,savename);
        end
    end

    cd(workdir);
end