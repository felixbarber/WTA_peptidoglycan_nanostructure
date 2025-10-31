%Eraseimagepart.m
%Rico Rojas, updated 1/21/19
%This routine lets the user select portions of an image stack to erase (make background).   

%INSTRUCTIONS FOR USE:
%Save the image stack in a directory without any other .tif files in it.  When 
%you run the program, the final image in the image stack will open.  
%Select the regions you want to delete with the cursor and then press Enter.  
%The program writes over the original image stack, so if you want a backup stack, 
%save it in a separate location.

%INPUT:
%dirname:Directory in which the image stack is saved.

%Calls upon:
%norm16bit.m

clear
close all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%USER INPUT
% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/'
% data_loc='/Users/felixbarber/Documents/Rojas_Lab/data/'

num_scenes = 5;
basename1='250612_bFB66_s750_tun_gr';
data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='250613_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='250617_bFB319_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250522_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'
% 
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

% num_scenes = 3;
% basename1='241202_bFB7_25uMGlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 2;
% basename1='210429_FB6_inducer_loss';
% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/'

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
% basename1='240725_bFB66_40uM_GlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 4;
% basename1='240724_bFB69_25uM_GlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240724_bFB66_25uM_GlpQ_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240724_bFB66_29uM_GlpQ_recovery';

% num_scenes = 2;
% basename1='240612_bFB260_degron_tester_500uMIPTG002';

% 
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

% num_scenes = 5;
% basename1='240503_bFB69_GlpQ_tester';

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


% num_scenes = 6;
% basename1='211006_bFB1_teichoicase_recovery';

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

%num_scenes=5;
%basename1='200916_BS_fos';

%num_scenes = 5;
%basename1 = '200928_BS_tun_test';
% 
% num_scenes = 4;
% basename1 = '201013_BS_tun_fos';

% 
% num_scenes = 5;
% basename1 = '201023_BS_cerulenin';

% 
% num_scenes = 5;
% basename1 = '201112_BS_tun_fos_delay';

% 
% num_scenes = 5;
% basename1 = '201112_BS_tun_fos_simult';
% 
% num_scenes = 5;
% basename1 = '201115_BS_fos';

% num_scenes = 5;
% basename1 = '201115_BS_fos_recovery';

% num_scenes=9;
% basename1 = '201120_LM_fos';

% num_scenes = 3;
% basename1 = '210108_BS_tun';
% 
% num_scenes = 5;
% basename1 = '210128_FB2_Tun_response';

% 
% num_scenes = 5;
% basename1 = '210212_FB1_LB_Tun_response';
% 
% num_scenes=4;
% basename1='191216_Paola_CRISPRi_TagO';

% num_scenes=8;
% basename1='210401_BS168_LB_HADA';

% num_scenes = 6;
% basename1 = '210304_FB1_LB_Tun_response_HADA';

% num_scenes = 5;
% basename1 = '210416_FB2_Tun_response';
% 
% num_scenes=5;
% basename1='210401_BS168_Tun_HADA_expt4';


% num_scenes=6;
% basename1='210429_FB6_inducer_loss';

% num_scenes=6;
% basename1='210506_FB6_inducer_loss_timelapse';


% num_scenes=7;
% basename1='210507_FB1_Tun_Mg';
% 
% num_scenes=3;
% basename1='210718_FB1_Tun_Response';

% num_scenes=5;
% basename1='210718_FB7_Tun_Response';


% num_scenes=5;
% basename1='210718_FB8_Tun_Response';
% 
% num_scenes=8;
% basename1='210723_FB8_Tun_Response';

% 
% num_scenes=7;
% basename1='210723_FB7_Tun_Response';

% num_scenes=7;
% basename1='210723_FB1_Tun_Response';

% num_scenes=8;
% basename1='210916_bFB1_PBS_recovery';

% num_scenes=6;
% basename1='210916_bFB1_PBS_teichoicase_recovery';
% % 
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

% num_scenes=1;
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
% 
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
% 
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
% 
% num_scenes=4;
% basename1='221005_bFB149_Tun_gr';

% num_scenes=5;
% basename1='221012_bFB69_Tun_gr';

% num_scenes=4;
% basename1='221017_bFB66_Tun_hydr';

% num_scenes=5;
% basename1='221014_bFB154_Xyl_depl_gr';

% num_scenes=4;
% basename1='221021_bFB113_Tun_gr';
% 
% num_scenes=4;
% basename1='221021_bFB109_Tun_gr';

% num_scenes=5;
% basename1='221025_bFB118_Tun_gr';

% num_scenes=5;
% basename1='221025_bFB113_Tun_gr';


% num_scenes=5;
% basename1='221025_bFB109_Tun_gr';

% num_scenes=5;
% basename1='221028_bFB66_hydr_timelapse';

% num_scenes=4;
% basename1='221028_bFB66_Tun_hydr_timelapse';

% 
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

% num_scenes = 5;
% basename1='230331_bER47_Mecillinam_LB';

% num_scenes = 5;
% basename1='230331_bER47_Mecillinam_Tun_LB';

tic;
for i0=1:num_scenes
    basename=strcat(basename1,'_s',sprintf('%03d',i0));
%     dirname=['D:/Documents_D/Rojas_lab/data/' basename1 '/' basename '_1_a'];
    dirname=[data_loc basename1 '/' basename '_1_a'];
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    curdir=cd;

    cd(dirname);
    directory=dir('*.tif');
    T1=length(directory);
    path(dirname,path)

    imagename=directory(T1).name;
    im1=imread(imagename);
    [imM,imN]=size(im1);
    
    
    ppix=0.5;
    im2=norm16bit(im1,ppix);

    figure,imshow(im1,stretchlim(im1)*65000)
    % Now we automatically erase the pillars since we know the grid spacing
    % is regular. First we have to help out by aligning the orientation of
    % the grid, clicking on two pillars in the same horizontal row.
    count=0;
    
%     point1=get(gca,'CurrentPoint');   
%     finalRect=rbbox;                   
%     %pause
%     point2=get(gca,'CurrentPoint');  
%     temp_xy=(point1(1,1:2)+point2(1,1:2))/2;
    
%     temp_xy=ginput()
% %     offset_angle=acos((temp_xy(2,1)-temp_xy(1,1))/((temp_xy(2,1)-temp_xy(1,1))^2+(temp_xy(2,2)-temp_xy(1,2))^2)^0.5); % angle in radians of grid alignment. Positive is acw rotation.
% %     h_angle=acos((temp_xy(3,1)-temp_xy(1,1))/((temp_xy(3,1)-temp_xy(1,1))^2+(temp_xy(3,2)-temp_xy(1,2))^2)^0.5); % angle in radians of grid alignment. Positive is acw rotation.
%     gs_h=211; % horizontal grid spacing
%     gs_d=235.243; % angular grid spacing
%     gs_a=1.0986; % angle of grid spacing in radians
% %     gs_diag_adj=offset_angle; % adjusted diagonal angle
%     gs_diag_adj=gs_a; % adjusted diagonal angle
% %     gs_h_adj=offset_angle-gs_a; % adjusted horizontal angle.
%     gs_h_adj=0; % adjusted horizontal angle.
%     latt_v1 = [gs_h*cos(gs_h_adj),gs_h*sin(gs_h_adj)]; % lattice vector 1, xy
%     latt_v2 = [gs_d*cos(gs_diag_adj),gs_d*sin(gs_diag_adj)]; % lattice vector 2
%     box_size = [50,50];
%     init_point=temp_xy(1,1:2); % initial seed point for lattice generation

    temp_xy=ginput()% order is [[x1,y1],[x2,y2]]
    offset_angle=-acos((temp_xy(2,1)-temp_xy(1,1))/((temp_xy(2,1)-temp_xy(1,1))^2+(temp_xy(2,2)-temp_xy(1,2))^2)^0.5); % angle in radians of grid alignment. Positive is acw rotation.
%     h_angle=acos((temp_xy(3,1)-temp_xy(1,1))/((temp_xy(3,1)-temp_xy(1,1))^2+(temp_xy(3,2)-temp_xy(1,2))^2)^0.5); % angle in radians of grid alignment. Positive is acw rotation.
    gs_h=210; % horizontal grid spacing
    gs_d=235; % angular grid spacing
    gs_a=1.11; % angle of grid spacing in radians
% Initial, measured values
%     gs_h=211; % horizontal grid spacing
%     gs_d=235.243; % angular grid spacing
%     gs_a=1.0986; % angle of grid spacing in radians
    gs_diag_adj=gs_a+offset_angle; % adjusted diagonal angle
%     gs_diag_adj=gs_a; % adjusted diagonal angle
    gs_h_adj=offset_angle; % adjusted horizontal angle.
%     gs_h_adj=0; % adjusted horizontal angle.
    latt_v1 = [gs_h*cos(gs_h_adj),gs_h*sin(gs_h_adj)]; % lattice vector 1, xy
    latt_v2 = [gs_d*cos(gs_diag_adj),gs_d*sin(gs_diag_adj)]; % lattice vector 2
    box_size = [60,60];
    init_point=temp_xy(3,1:2); % initial seed point for lattice generation is the third point, taken roughly in the middle
    for tempind1=-7:7
        for tempind2=-7:7
            temp_point=round(init_point+tempind1*latt_v1+tempind2*latt_v2);
            p1=round(temp_point-box_size/2);%Calculate locations
            p2=round(temp_point+box_size/2);%Calculate locations
%             if p1(1)>=1 & p1(1)<=imN & p1(2)>=1 & p1(2)<=imM & p2(1)>=1 & p2(1)<=imN & p2(2)>=1 & p2(2)<=imM
%                 count=count+1;
%                 rp1(count,:)=p1;
%                 rp2(count,:)=p2;
%             end
            temp_v1= (p1(1)>=1 & p1(1)<=imN & p1(2)>=1 & p1(2)<=imM);
            temp_v2=(p2(1)>=1 & p2(1)<=imN & p2(2)>=1 & p2(2)<=imM);
            if  temp_v1 | temp_v2 
                if p1(2)>imM
                    p1(2)=imM;
                end
                if p1(2)<1
                    p1(2)=1;
                end
                if p1(1)>imN
                    p1(1)=imN;
                end
                if p1(1)<1
                    p1(1)=1;
                end
                if p2(2)<1
                    p2(2)=1;
                end
                if p2(2)>imM
                    p2(2)=imM;
                end
                if p2(1)<1
                    p2(1)=1;
                end
                if p2(1)>imN
                    p2(1)=imN;
                end
                p1
                p2
                count=count+1;
                rp1(count,:)=p1;
                rp2(count,:)=p2;
            end

        end
    end
    
    temp_im=imgaussfilt(im1,20);
    for n=1:count
            %Load image
            [imM,imN]=size(im1);
            [imcounts,bins]=hist(double(nonzeros(im1)));
            [~,mpos]=max(imcounts);
            val=bins(mpos);
%             im(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1))=val*ones(rp2(n,2)-rp1(n,2)+1,rp2(n,1)-rp1(n,1)+1);
            im1(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1))=temp_im(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1));
    end
    figure,imshow(im1,stretchlim(im1)*65000)
    

    %%%%%%%%%%%%%%%%%%%%%%%% Doing the segmentation on this image,
    % minimally modified from Rico's segmentation code.
    
    lscale=0.0929;%%Microns per pixel.
    tscale=20;%Frame rate.
    thresh=0;%For default, enter zero.
    IntThresh=20000;%Threshold used to enhance contrast. Default:35000
    dr=1;%Radius of dilation before watershed 
    sm=2;%Parameter used in edge detection
    minL=2;%Minimum cell length
    minW=0.2;%Minimum cell width
    maxW=2.0;%Maximum cell width, set to 2.0 for tunicamycin shock, but
    % this was previously set to 1.5 which seemed too low for Tunicamycin shock
    minA=50;%Minimum cell area. default 50
    cellLink=4;%Number of frames to ignore missing cells when tracking frame to frame
    recrunch=0;%Display data from previously crunched data? 0=No, 1=Yes.
    vis=1;%Display cell tracking? 0=No, 1=Yes.
    vis1scene=1; % display cell tracking for the first scene? 0=No, 1=Yes.
    checkhist=0;%Display image histogram? 0=No, 1=Yes.

    
    T=1;
    t=1;
    
    nc=zeros(1,T);
    allcentroids=[];
    cellnum=[];
    tstamp=[];

    
    %Pre-allocate matrices
    wav=zeros(1,T);
    wstd=zeros(1,T);
    wste=zeros(1,T);
    acell=zeros(1,T);
    wcell=zeros(1,T);
    sacell=zeros(1,T);
    lcell=zeros(1,T);
    DS=zeros(1,T);
    boun=cell(1,T);
    pole=zeros(1,T);
    mline=cell(1,T);
    
    
    %De-speckle image
    im=medfilt2(im1);

    %Normalize images
    ppix=0.5;
    im=norm16bit(im,ppix);

    %Enhance contrast
    imc=imcomplement(im);
    if checkhist==1;
        figure,imhist(imc),pause;
    end

    if thresh==0;
        [imcounts,bins]=imhist(imc);
        [imcounts,idx]=sort(imcounts);
        bins=bins(idx);
        thresh1=bins(end-1);
    else
        thresh1=thresh;
    end
    imc=imadjust(imc,[thresh1/65535 1],[]);   

    %Find edges
    [ed2,thresh2]=edge(imc,'canny',[],sm*sqrt(2));

    %Clean image
    cc=bwconncomp(ed2,8);
    stats=regionprops(cc,imc,'Area','MeanIntensity');
    idx=find([stats.Area]>minA&[stats.Area]<1e5&[stats.MeanIntensity]>IntThresh);
    ed2=ismember(labelmatrix(cc),idx);

    %Close gaps in edges by extending spurs and bridging adjacent
    %ones.
    despurred=bwmorph(ed2,'spur');
    spurs=ed2-despurred;
    [spy,spx]=find(spurs);
    for k=1:length(spx)
        ed2(spy(k)-1:spy(k)+1,spx(k)-1:spx(k)+1)=ed2(spy(k)-1:spy(k)+1,spx(k)-1:spx(k)+1)+rot90(ed2(spy(k)-1:spy(k)+1,spx(k)-1:spx(k)+1),2);
        ed2(spy(k),spx(k))=1;
    end
    ed2=bwmorph(ed2,'bridge'); 

    se=strel('disk',dr);
    ed2=imdilate(ed2,se);
    ed2=bwmorph(ed2,'thin',2);

    %Identify cells based on size and intensity
    ed3=~ed2;
    ed3(1,:)=ones(1,imN);
    ed3(end,:)=ones(1,imN);
    ed3(:,1)=ones(imM,1);
    ed3(:,end)=ones(imM,1);

    cc=bwconncomp(ed3,4);
    stats=regionprops(cc,imc,'Area','MeanIntensity');
    idx=find([stats.Area]>minA&[stats.Area]<1e5&[stats.MeanIntensity]>3e4);
    ed4=ismember(labelmatrix(cc),idx);

    %Find cell areas and centroids
    bw=bwmorph(ed4,'thicken');
    [P,bw]=bwboundaries(bw,4,'noholes');
    stats=regionprops(bw,'Area','Centroid','PixelIdxList');

    L=bwlabel(bw);    
    labels(:,:,t)=L;
    labels2(:,:,t)=bw;

    nc(t)=length(P);
    areas=[stats.Area];
    cents=cat(1,stats.Centroid);
    acell(nc(t),t)=0;
    acell(1:nc(t),t)=[stats.Area]';
    centroids=cents;
    %Calculate smooth cell contours
    for n=1:nc(t)

        rP=[P{n}(:,2),P{n}(:,1)];
        px=[rP(1:end-1,1);rP(1:end-1,1);rP(:,1)];
        py=[rP(1:end-1,2);rP(1:end-1,2);rP(:,2)];
        sp=length(rP);
        dS=sqrt(diff(px).^2+diff(py).^2);
        S=[0 cumsum(dS)'];

        px=csaps(S,px,0.05,S);
        py=csaps(S,py,0.05,S);

        px=px(sp+1:2*sp);
        py=py(sp+1:2*sp);

        px(end)=px(1);
        py(end)=py(1);

        dS=sqrt(diff(px).^2+diff(py).^2);
        S=[0 cumsum(dS)];
        ls=length(S);
        DS(n,t)=S(end)/(ls-1);
        Sn=(0:DS(n,t):S(end));
        nx=spline(S,px,Sn);
        ny=spline(S,py,Sn);

        boun{n,t}=[nx',ny'];
        pxls{n,t}=stats(n).PixelIdxList;

    end
    allcentroids=[allcentroids;centroids];
    tstamp=[tstamp;ones(nc(t),1)*t];
    cellnum=[cellnum;(1:nc(t))'];

    toc

    for n=1:nc(t)    
         X=boun{n,t}(:,1);
         Y=boun{n,t}(:,2);   
         [sX,~]=size(X);

         %Find poles
         [X,Y,pole(n,t)]=polefinder(X,Y);

         %Create mesh
         npts=min(pole(n,t),sX-pole(n,t)+1);
         S=(0:DS(n,t):(sX-1)*DS(n,t));

         s1=(0:S(pole(n,t))/(npts-1):S(pole(n,t)));
         s2=(S(pole(n,t)):(S(end)-S(pole(n,t)))/(npts-1):S(end));
         xc1=spline(S(1:pole(n,t)),X(1:pole(n,t)),s1);
         xc2=spline(S(pole(n,t):end),X(pole(n,t):end),s2);
         yc1=spline(S(1:pole(n,t)),Y(1:pole(n,t)),s1);
         yc2=spline(S(pole(n,t):end),Y(pole(n,t):end),s2);
         xc2=fliplr(xc2);
         yc2=fliplr(yc2);

         %Calculate midline
         mline{n,t}=[(xc1+xc2)'/2,(yc1+yc2)'/2];
         dxy=diff(mline{n,t}).^2;
         dl=sqrt(dxy(:,1)+dxy(:,2));
         lcell(n,t)=sum(dl);
         % start from here for calculating surface area. Do this based 
         % on conical sections, so that the area is calculated using
         % the formula SA=pi*(r1+r2)*(h^2+(r2-r1)^2)^0.5
         temp_r1 = sqrt((xc1-xc2).^2+(yc1-yc2).^2)/2;
         temp_r=(temp_r1(1:end-1)+temp_r1(2:end))/2;
         temp1 = (xc1(2:end)+xc2(2:end)-xc1(1:end-1)-xc2(1:end-1)).^2;
         temp2 = (yc1(2:end)+yc2(2:end)-yc1(1:end-1)-yc2(1:end-1)).^2;
         temp_h=0.5*(temp1+temp2).^0.5;
         sa_segments = pi*(temp_r1(1:end-1)+temp_r1(2:end))...
             .*(temp_h.^2+(temp_r1(1:end-1)-temp_r1(2:end)).^2).^0.5;
         sacell(n,t)=sum(sa_segments);

         %Calculate width
         ls=[0 cumsum(dl)'];
         [~,mpos1]=min(abs(ls/lcell(n,t)-0.25));
         [~,mpos2]=min(abs(ls/lcell(n,t)-0.75));

         widths=sqrt((xc1-xc2).^2+(yc1-yc2).^2);
         %w(n,t)=max(widths);
         wcell(n,t)=(widths(mpos1)+widths(mpos2))/2;

    end

    %Dimsionalize the variables
    lcell=lcell*lscale;
    wcell=wcell*lscale;
    acell=acell*lscale^2;
    sacell=sacell*lscale^2;

    %Throw away cells that are too short or too fat or too skinny
    lcell(lcell<minL|wcell>maxW|wcell<minW)=NaN;
    wcell(lcell<minL|wcell>maxW|wcell<minW)=NaN;
    acell(lcell<minL|wcell>maxW|wcell<minW)=NaN;
    sacell(lcell<minL|wcell>maxW|wcell<minW)=NaN;

    [row, col] = find(~isnan(lcell)); % Finding the objects that we don't 
    % filter out
    %%%%%%%%%%%%%%%%%%%%%%%%%%%% Finished segmentation


%     set(gcf,'Pointer','fullcross')
    hold on
    for k=1:length(row)
       plot(boun{row(k),t}(:,1),boun{row(k),t}(:,2),'-r')
    end
    axis manual

    k=0;
    w=0;
    while w~=1  % This allows us to go back and edit more if the output 
        set(gcf,'Pointer','fullcross')
        hold on
        axis manual
        % doesn't look good
        k=waitforbuttonpress;
        while k~=1
            count=count+1;
            k=waitforbuttonpress;
            point1=get(gca,'CurrentPoint');   
            finalRect=rbbox;                   
            %pause
            point2=get(gca,'CurrentPoint');    
            point1=point1(1,1:2);              
            point2=point2(1,1:2);
            point1(point1<1)=1;
            point2(point2<1)=1;
            if point1(2)>imM
                point1(2)=imM;
            end
            if point1(1)>imN
                point1(1)=imN;
            end
            if point2(2)>imM
                point2(2)=imM;
            end
            if point2(1)>imN
                point2(1)=imN;
            end
            p1=min(point1,point2);%Calculate locations
            p2=max(point1,point2);
            offset = abs(point1-point2);%And dimensions
            x = [p1(1) p1(1)+offset(1) p1(1)+offset(1) p1(1) p1(1)];
            y = [p1(2) p1(2) p1(2)+offset(2) p1(2)+offset(2) p1(2)];
            plot(x,y)
    
            rp1(count,:)=round(p1);
            rp2(count,:)=round(p2);
        end
        save('outline.mat','rp1','rp2','count')
        vars = {'rp1','rp2'};
        clear(vars{:})
        
        load('outline.mat')
%         temp_im=imgaussfilt(im1,20);
        for n=1:count
                %Load image
                [imM,imN]=size(im1);
                [imcounts,bins]=hist(double(nonzeros(im1)));
                [~,mpos]=max(imcounts);
                val=bins(mpos);
    %             im(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1))=val*ones(rp2(n,2)-rp1(n,2)+1,rp2(n,1)-rp1(n,1)+1);
                im1(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1))=temp_im(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1));
        end
        figure,imshow(im1,stretchlim(im1)*65000)
        w=waitforbuttonpress;     
        % Note, here we should click if we want to return to editing, and press
        % enter if you instead want to move on
    end

    cd(data_loc);
    close all
    vars = {'rp1','rp2'};
    clear(vars{:})
    
end

for i0=1:num_scenes
    basename=strcat(basename1,'_s',sprintf('%03d',i0));
    dirname=[data_loc basename1 '/' basename '_1_a'];
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    curdir=cd;

    cd(dirname);
    directory=dir('*.tif');
    T1=length(directory)-1;
    path(dirname,path)

    imagename=directory(T1).name;
    im1=imread(imagename);
    [imM,imN]=size(im1);
    load('outline.mat')
    for t=1:T1+1
        t
        for n=1:count
            %Load image
            imagename=directory(t).name;
            
            im=imread(imagename);
            temp_im=imgaussfilt(im,20);
            [imM,imN]=size(im);

            [imcounts,bins]=hist(double(nonzeros(im1)));
            [~,mpos]=max(imcounts);
            val=bins(mpos);
%             im(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1))=val*ones(rp2(n,2)-rp1(n,2)+1,rp2(n,1)-rp1(n,1)+1);
            im(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1))=temp_im(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1));
            delete(imagename);
            imwrite(im,imagename);
        end
    end
    cd(data_loc);
    close all
end