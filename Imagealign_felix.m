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

num_scenes = 3;
basename1='250626_bFB66_tun_lysis';
data_loc='/Volumes/data_ssd2/Rojas_Lab/data/';

% num_scenes = 5;
% basename1='250612_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='250613_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='250617_bFB319_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250522_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250520_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 2;
% basename1='250519_bFB7_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='250513_bFB66_s750_tun_gr_p2';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='250513_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'


% num_scenes = 4;
% basename1='250408_bFB291_IPTG_induction';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='250402_bFB66_LB';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 2;
% basename1='250403_bFB292_IPTG_induction';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 3;
% basename1='250326_bFB295_IPTG_induction';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='250325_bFB293_IPTG_induction';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='250324_bFB291_IPTG_induction';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='250227_bFB87_Tun_PBS_long_incubation_45min';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 3;
% basename1='250226_bFB66_Tun_PBS_long_incubation_45min';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 2;
% basename1='250225_bFB66_Tun_PBS_long_incubation_30min';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='250224_bFB66_Tun_BufferA_long_incubation';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='250219_bFB66_Spp1_300ug_LB';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='250221_bFB69_Tun_PBS_long_incubation';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='250220_bFB66_Tun_PBS_long_incubation';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'


% num_scenes = 5;
% basename1='250218_bFB66_PBS_long_incubation';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='250213_bFB8_PBS_BufferA_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'


% num_scenes = 5;
% basename1='250213_bFB8_25uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'


% num_scenes = 2;
% basename1='210429_FB6_inducer_loss';
% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/'


% num_scenes = 3;
% basename1='241202_bFB7_25uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 3;
% basename1='241202_bFB7_25uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='241201_bFB93_40uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='241201_bFB93_25uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='241130_bFB93_25uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='241129_bFB87_25uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='241126_bFB69_Tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='241115_bFB87_GlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='241007_bFB69_GlpQ_LB';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240927_bFB69_Tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='240926_bFB7_Tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='240925_bFB93_40uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240925_bFB93_40uMGlpQ_recovery_v2';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240925_bFB7_Tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240920_bFB93_40uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'


% num_scenes = 4;
% basename1='240920_bFB93_PBS_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='240920_bFB93_GlpQ_Recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240918_bFB87_PBS_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'


% num_scenes = 5;
% basename1='240918_bFB87_GlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='240901_bFB66_30minPBS_recovery_run2';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240901_bFB66_30minPBS_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='240807_bF66_40uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='240729_bFB69_Tun_lysis';
% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/'

% num_scenes = 6;
% basename1='230317_bFB69_Tun_Lysis';
% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/'


% num_scenes = 4;
% basename1='240725_bFB66_40uM_GlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='240724_bFB69_25uM_GlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% % num_scenes = 5;
% % basename1='240724_bFB66_25uM_GlpQ_recovery';
% % data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240724_bFB66_29uM_GlpQ_recovery';


% num_scenes = 2;
% basename1='240612_bFB260_degron_tester_500uMIPTG002';

% num_scenes = 5;
% basename1='240528_bFB69_BufferA_500mMSorbitol';

% num_scenes = 5;
% basename1='240528_bFB69_GlpQ_500mMSorbitol';


% num_scenes = 5;
% basename1='240527_bFB66_BufferA_tester';

% num_scenes = 5;
% basename1='240527_bFB66_GlpQ_tester';

% num_scenes = 5;
% basename1='240523_bFB69_BufferA_tester';

% num_scenes = 5;
% basename1='240523_bFB69_GlpQ_tester';

% 
% num_scenes = 5;
% basename1='240503_bFB69_GlpQ_tester';

% num_scenes = 5;
% basename1='210128_FB2_Tun_response';

% num_scenes = 2;
% basename1='240311_bFB69_PBS_GlpQ_conc_recovery';

% num_scenes = 5;
% basename1='231129_bFB69_PBS_BufferA_500mMSorbitol_15min_recovery';

% num_scenes = 4;
% basename1='240111_bFB66_Tun_500mMSorbitol_test';

% num_scenes = 5;
% basename1='231119_bFB69_PBS_BufferA_500mMSorbitol_recovery_15min_ZPBS';

% num_scenes = 5;
% basename1='231117_bFB69_PBS_GlpQ_500mMSorbitol_recovery_15min_ZPBS';


% num_scenes = 5;
% basename1='231115_bFB69_PBS_BufferA_recovery_15min_ZPBS';

% num_scenes = 5;
% basename1='231110_bFB6_Xylose_depletion';

% num_scenes = 5;
% basename1='231110_bFB69_PBS_GlpQ_500mMSorbitol_recovery_15min_ZPBS';

% num_scenes = 5;
% basename1='231108_bFB69_PBS_GlpQ_recovery_15min_ZPBS';


% num_scenes = 5;
% basename1='231105_bFB69_PBS_BufferA_500mMSorbitol_recovery_15min';

% num_scenes = 5;
% basename1='231103_bFB66_PBS_denatGlpQ_recovery_15min';


% num_scenes = 5;
% basename1='231103_bFB69_PBS_GlpQ_500mMSorbitol_recovery_15min';


% num_scenes = 5;
% basename1='231030_bFB66_PBS_BufferA_recovery_30min';


% num_scenes = 5;
% basename1='231030_bFB69_PBS_BufferA_recovery_30min';


% num_scenes = 5;
% basename1='231027_bFB69_PBS_BufferA_recovery_15min';

% num_scenes = 7;
% basename1='210731_FB2_GlpQ_Response_10uM';

% num_scenes = 6;
% basename1='210916_bFB1_PBS_teichoicase_recovery';

% num_scenes = 8;
% basename1='210916_bFB1_PBS_recovery';

% num_scenes = 5;
% basename1='231018_bFB69_PBS_BufferA_recovery_15min';

% num_scenes = 5;
% basename1='231018_bFB69_PBS_GlpQ_recovery_15min';

% num_scenes = 5;
% basename1='231012_bFB69_PBS_GlpQ_recovery_15min';

% num_scenes = 5;
% basename1='231011_bFB66_PBS_GlpQ_recovery_15min';

% num_scenes = 5;
% basename1='231005_bFB66_PBS_GlpQconst_recovery';

% num_scenes = 5;
% basename1='231004_bFB69_PBS_BufferA_recovery_15min';

% num_scenes = 5;
% basename1='231004_bFB66_PBS_GlpQ_recovery_15min';

% num_scenes = 5;
% basename1='230926_bFB66_PBS_GlpQdenat_recovery_15min';

% num_scenes = 5;
% basename1='230926_bFB66_PBS_GlpQ_recovery_15min';

% num_scenes = 5;
% basename1='230921_bFB66_PBS_BufferA_recovery_15min';

% num_scenes = 6;
% basename1='230921_bFB66_PBS_GlpQ_recovery_15min';

% num_scenes = 6;
% basename1='230825_bFB66_PBS_recovery_15min';

% num_scenes = 6;
% basename1='230825_bFB66_PBS_recovery';

% num_scenes = 5;
% basename1='230404_bER47_Tun';

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


% num_scenes=6;
% basename1='210916_bFB1_PBS_teichoicase_recovery';


% num_scenes=6;
% basename1='210929_bFB2_teichoicase_recovery';

% num_scenes=6;
% basename1='211006_bFB2_teichoicase_recovery';

% num_scenes=6;
% basename1='211006_bFB1_teichoicase_recovery';
% 
% num_scenes=7;
% basename1='211014_bFB1_teichoicase_tunicamycin_recovery';


% num_scenes=7;
% basename1='211019_bFB1_PBS_buffer_recov';

% num_scenes=6;
% basename1='211020_bFB7_Tun';

% num_scenes=6;
% basename1='211020_bFB8_Tun';

% num_scenes=6;
% basename1='211215_bFB66_Tun_gr';

% num_scenes=5;
% basename1='211215_bFB7_Tun_gr';

% num_scenes=6;
% basename1='211216_bFB8_Tun_gr';

% num_scenes=6;
% basename1='211216_bFB66_Tun_gr';

% num_scenes=7;
% basename1='220105_bFB79_Tun_response';

% num_scenes=7;
% basename1='220121_bFB66_Tun_gr';

% num_scenes=6;
% basename1='220202_bFB66_Tun_Mg_gr';

% num_scenes=6;
% basename1='220204_bFB69_Tun_gr';

% num_scenes=6;
% basename1='220218_bFB66_Tun_gr_Mg';

% num_scenes=7;
% basename1='220223_bFB87_Tun_Mg_gr';

% num_scenes=7;
% basename1='220224_bFB69_Tun_Mg_gr';

% num_scenes=7;
% basename1='220303_bFB87_Tun_gr';

% num_scenes=7;
% basename1='220304_bFB93_Tun_gr';

% num_scenes=6;
% basename1='220309_bFB69_Tun_gr';

% num_scenes=8;
% basename1='220310_bFB93_Tun_gr';

% num_scenes=6;
% basename1='220311_bFB87_Tun_gr';

% num_scenes=6;
% basename1='210429_FB6_inducer_loss';

% num_scenes=6;
% basename1='210506_FB6_inducer_loss_timelapse';

% num_scenes=4;
% basename1='220831_bFB145_Tun_gr';

% num_scenes=4;
% basename1='220902_bFB149_Tun_gr';

% num_scenes=5;
% basename1='220909_bFB145_Tun_gr';

% num_scenes=5;
% basename1='220916_bFB145_Tun_gr';

% num_scenes=4;
% basename1='221004_bFB145_Tun_gr';

% num_scenes=4;
% basename1='221005_bFB149_Tun_gr';
% 
% num_scenes=5;
% basename1='221012_bFB69_Tun_gr';

% num_scenes=5;
% basename1='221014_bFB154_Xyl_depl_gr';

% num_scenes=4;
% basename1='221017_bFB66_Tun_hydr';

% num_scenes=4;
% basename1='221021_bFB113_Tun_gr';

% num_scenes=4;
% basename1='221021_bFB109_Tun_gr';

% num_scenes=5;
% basename1='221025_bFB118_Tun_gr';

% num_scenes=5;
% basename1='221025_bFB113_Tun_gr';


% num_scenes=5;
% basename1='221025_bFB109_Tun_gr';

% num_scenes = 5;
% basename1='221110_bFB66_Tun_Amp_gr';


% num_scenes = 5;
% basename1='221110_bFB66_Amp_gr';

% num_scenes = 6;
% basename1='230314_bFB169_Mecillinam';

% num_scenes = 6;
% basename1='230314_bFB169_Mecillinam_Tun';

% num_scenes = 7;
% basename1='230321_bFB7_Tun_lysis';

% num_scenes = 6;
% basename1='230327_bFB8_Tun_lysis';

% num_scenes = 6;
% basename1='230322_bFB69_Tun_lysis';

% num_scenes = 5;
% basename1='230331_bER47_Mecillinam_LB';

% num_scenes = 5;
% basename1='230331_bER47_Mecillinam_Tun_LB';

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
    directory=dir([basename '*.tif']);
    path(regname,path)
    T=length(directory);
    tf=T*ld;

    imagename=directory(1).name;
    RefIm=imread([regname '/' imagename]);

    count=0;
    % for i=1:ld
    for i=1:ld

        cd(dirname{i})
        path(dirname{i},path)
        directory2=dir([basename '*.tif']);
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
 