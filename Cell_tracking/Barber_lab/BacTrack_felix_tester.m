% set%BacTrack.m
%Tracks bacterial growth from phase image stacks.  
%Customized for B. subtilis.
%Bactrack2.m is customized for B. subtilis filaments.


%INSTRUCTIONS FOR USE:
%Remove frames with poor contrast and save phase image stack in a directory
%by itself.  Also save the micromanager metadata file as 'basename.txt' in
%the matlab path.
%
%INPUT:
%basename: name of the image stack.
%dirname:the full pathname of the directory where you saved the image
%        stack.
%metaname(optional):full or relative pathname of micromanager metadata file from
%which to extract time points.  If it is relative path name, the
%directory in which it is saved must be on the matlab path.
%lscale: microscope calibration in microns per pixels.
%sm: width of the Gaussian filter used in edge finder equals sm*sqrt(2).
%minL: minimum length of cells;
%minW: minimum width of cells;
%maxW: maximum width of cells;
%recrunch:0 or 1.  if you've already tracked the data set and just want to
%         re-plot the data enter 1.
%
%OUTPUT:
%T: number of time points.
%time: vector of length T with time points.
%tmid: vector of length T-1 with interstitial time points.
%ncells: number of individual cells tracked.
%lcell: ncells x T matrix of cell lengths.
%wcell: ncells x T matrix of cell widths.
%acell: ncells x T matrix of cell areas
%ew: ncells x T matrix of circumferential strains.
%acell: ncells x T matrix of cell areas.
%v: ncells x T-1 matrix of cell strain rates.
%B: ncells x T cell array with cell contours.
%mlines: ncells x T cell array with cell midlines
%wav: vector of length T with average cell widths.
%wstd: vector of length T with standard deviations of cell widths.
%wste: vector of length T with standard error of cell widths.
%vav: vector of length T-1 with average cell strain rate.
%vstd: vector of length T-1 with standard deviation of strain rates.
%vste: vector of length T-1 with standard error of strain rates.
%avav: vector of length T-1 with average cell areal strain rate.
%avstd: vector of length T-1 with standard deviation of areal strain rates.
%avste: vector of length T-1 with standard error of areal strain rates.
%ndp: vecotr of lenth T-1 with number of data points averaged over.

%Calls on the following m-files:
%norm16bit.m
%polefinder.m
%cellcurvature.m
%metadata.m
%extrema.m
%EffectiveLength.m
%fig2pretty.m
%movingaverage.m

% Note that B and pixels have the same enumeration as lcell etc.

clear
close all

tic
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%User Input

maxW=2.0;%Maximum cell width, set to 2.0 for tunicamycin shock, butto

num_scenes = 5;
basename1='250612_bFB66_s750_tun_gr';
data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='250613_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'


% num_scenes = 1;
% basename1='250522_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250520_bFB66_s750_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'
% 
% num_scenes = 2;
% basename1='250519_bFB7_tun_gr';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250515_bFB66_tun_pad';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250515_bFB66_LB_pad';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250514_bFB69_LB_pad_rep2';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 1;
% basename1='250514_bFB69_LB_pad';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='250513_bFB66_s750_tun_gr_p2';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='250513_bFB66_s750_tun_gr';
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
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/';

% num_scenes = 4;
% basename1='250408_bFB291_IPTG_induction';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'
% maxW=4.0;

% num_scenes = 4;
% basename1='250402_bFB66_LB';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'
% maxW=4.0;

% num_scenes = 3;
% basename1='250326_bFB295_IPTG_induction';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'
% maxW=4.0;

% num_scenes = 4;
% basename1='250325_bFB293_IPTG_induction';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'
% maxW=4.0;

% num_scenes = 4;
% basename1='250324_bFB291_IPTG_induction';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'
% maxW=4.0;

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

% num_scenes = 5;
% basename1='241201_bFB93_40uMGlpQ_recovery';
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

% num_scenes=5;
% basename1='200916_BS_fos';

% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/'
% data_loc='/Users/felixbarber/Documents/Rojas_Lab/data/'
% 

% num_scenes=7;
% basename1='220303_bFB87_Tun_gr';    % Done with 2.0micron width 3/10 
% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/'

% num_scenes=7;
% basename1='220304_bFB93_Tun_gr';    % Done with 2.0micron width 3/10

% num_scenes=8;
% basename1='220310_bFB93_Tun_gr';    % Done with 2.0micron width 3/10 
% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/';

% num_scenes=6;
% basename1='220311_bFB87_Tun_gr';
% data_loc='/Volumes/data_ssd1/Rojas_Lab/data/';


% num_scenes = 4;
% basename1='240901_bFB66_30minPBS_recovery_run2';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'

% num_scenes = 5;
% basename1='240901_bFB66_30minPBS_recovery';
% data_loc='/Volumes/data_ssd2/Rojas_Lab/data/'
% 
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
% basename1='210929_bFB2_teichoicase_recovery';

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

% num_scenes = 5;
% basename1 = '200928_BS_tun_test';

% 
% num_scenes = 4;
% basename1 = '201013_BS_tun_fos';

% num_scenes = 5;
% basename1 = '201023_BS_cerulenin';

% num_scenes = 5;
% basename1 = '201112_BS_tun_fos_delay';


% num_scenes = 5;
% basename1 = '201112_BS_tun_fos_simult';


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


% num_scenes = 5;
% basename1 = '210212_FB1_LB_Tun_response';

% 
% num_scenes = 5;
% basename1 = '210217_FB1_ER43_LB_HADA_expt1';

% 
% num_scenes = 5;
% basename1 = '210217_FB1_ER43_LB_HADA_expt2';

% 
% num_scenes = 6;
% basename1 = '210212_FB1_LB_Tun_response_HADA';
% num_channels=2;

% num_scenes = 5;
% basename1 = '210228_FB1_LB_Tun_response_HADA_0_5_ug';
% num_channels = 3;


% num_scenes = 4;
% basename1 = '210228_FB1_LB_Tun_response_HADA_0_25_ug';
% num_channels=3; 

% num_scenes = 6;
% basename1 = '210304_FB1_LB_HADA';
% num_channels=3; 

% num_scenes=4;
% basename1='191216_Paola_CRISPRi_TagO';
% 
% num_scenes=8;
% basename1='210401_BS168_LB_HADA';

% num_scenes = 6;
% basename1 = '210304_FB1_LB_Tun_response_HADA';
% 
% num_scenes = 5;
% basename1 = '210416_FB2_Tun_response';
% 
% num_scenes=5;
% basename1='210401_BS168_Tun_HADA_expt4';

% num_scenes=6;
% basename1='210429_FB6_inducer_loss';
% 
% num_scenes=6;
% basename1='210506_FB6_inducer_loss_timelapse';

% num_scenes=7;
% basename1='210507_FB1_Tun_Mg';

% num_scenes=2;
% basename1='210718_FB1_Tun_Response';
% 
% num_scenes=5;
% basename1='210718_FB7_Tun_Response';
% 
% num_scenes=5;
% basename1='210718_FB8_Tun_Response';

% num_scenes=8;
% basename1='210723_FB8_Tun_Response';   % Done with 2.0micron width 3/10

% num_scenes=7;
% basename1='210723_FB7_Tun_Response';   % Done with 2.0micron width 3/10

% num_scenes=7;
% basename1='210723_FB1_Tun_Response';

% num_scenes=8;
% basename1='210916_bFB1_PBS_recovery';

% num_scenes=6;
% basename1='210916_bFB1_PBS_teichoicase_recovery';
% 
% num_scenes=6;
% basename1='210929_bFB2_teichoicase_recovery';
% 
% num_scenes=6;
% basename1='211006_bFB2_teichoicase_recovery';
% 
% num_scenes=6;
% basename1='211006_bFB1_teichoicase_recovery';

% num_scenes=7;
% basename1='211014_bFB1_teichoicase_tunicamycin_recovery';

% num_scenes=7;
% basename1='211019_bFB1_PBS_buffer_recov';


% num_scenes=6;
% basename1='211020_bFB7_Tun';   % Done with 2.0micron width 3/10

% num_scenes=1;
% num_scenes=6;
% basename1='211020_bFB8_Tun';   % Done with 2.0micron width 3/10

% num_scenes=6;
% basename1='211215_bFB66_Tun_gr';    % Done with 2.0micron width 3/10

% num_scenes=5;
% basename1='211215_bFB7_Tun_gr';   % Done with 2.0micron width 3/10

% num_scenes=6;
% basename1='211216_bFB8_Tun_gr';   % Done with 2.0micron width 3/10

% num_scenes=6;
% basename1='211216_bFB66_Tun_gr';    % Done with 2.0micron width 3/10

% num_scenes=7;
% basename1='220105_bFB79_Tun_response';
% 
% num_scenes=7;
% basename1='220121_bFB66_Tun_gr';    % Done with 2.0micron width 3/10         


% num_scenes=6;
% basename1='220202_bFB66_Tun_Mg_gr';

% num_scenes=6;
% basename1='220204_bFB69_Tun_gr';    % Done with 2.0micron width 3/10 

% 
% num_scenes=6;
% basename1='220218_bFB66_Tun_gr_Mg';

% num_scenes=7;
% basename1='220223_bFB87_Tun_Mg_gr';

% num_scenes=7;
% basename1='220224_bFB69_Tun_Mg_gr';

% num_scenes=6;
% basename1='210429_FB6_inducer_loss';

% num_scenes=6; % Correct
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

% num_scenes=5;
% basename1='221012_bFB69_Tun_gr';

% num_scenes=4;
% basename1='221017_bFB66_Tun_hydr';
% 
% num_scenes=5;
% basename1='221014_bFB154_Xyl_depl_gr';

% num_scenes=4;
% basename1='221021_bFB113_Tun_gr';

% num_scenes=4;
% basename1='221021_bFB109_Tun_gr';

% num_scenes=5;
% basename1='221025_bFB118_Tun_gr';

% num_scenes=5;
% basename1='221025_bFB113_Tun_gr';

% % num_scenes=5;
% % basename1='221025_bFB109_Tun_gr';

% num_scenes=5;
% basename1='221028_bFB66_hydr_timelapse';

% num_scenes=6;
% basename1='221028_bFB79_hydr_timelapse';

% num_scenes=1;
% basename1='221028_bFB66_bleach';
% 
% num_scenes = 5;
% basename1='221110_bFB66_Tun_Amp_gr';

% num_scenes = 5;
% basename1='221110_bFB66_Amp_gr';

% num_scenes=6;
% basename1='220309_bFB69_Tun_gr';    % Done with 2.0micron width 3/10 

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

for i0=1:num_scenes % changed from num_scenes
    tracking = 1;  % This should be set to 1 if you are tracking cells,
    % but for lysis experiments you want this set to zero.
    basename=strcat(basename1,'_s',sprintf('%03d',i0));
    %     data_loc='/Users/felixbarber/Documents/Rojas_lab/data/'
    dirname=[data_loc basename1 '/' basename '_1_a'];%Directory that the image stack is saved in.
    %basename='070512_6';skp=[];%Name of the image stack, used to save file.    
    savedir=[data_loc];%Directory to save the output .mat file to.
    %metaname=['/Users/Rico/Documents/MATLAB/Matlab Ready/' basename '/metadata.txt'];%Name of metadata file.  Will only work if images were taken with micromanager.
    lscale=0.0929;%%Microns per pixel.
    tscale=20;%Frame rate.
    thresh=0;%For default, enter zero.
%     IntThresh=20000;%Threshold used to enhance contrast. Default:35000
    IntThresh=10000;%Threshold used to enhance contrast. Default:35000
%     IntThresh=5000;%Threshold used to enhance contrast. Default:35000
    dr=1;%Radius of dilation before watershed 
    sm=2;%Parameter used in edge detection
    minL=2;%Minimum cell length
    minW=0.2;%Minimum cell width

%     maxW=4.0;%Maximum cell width, set to 2.0 for tunicamycin shock, but
%     % this was previously set to 1.5 which seemed too low for Tunicamycin shock
    minA=50;%Minimum cell area. default 50
    cellLink=4;%Number of frames to ignore missing cells when tracking frame to frame
    recrunch=0;%Display data from previously crunched data? 0=No, 1=Yes.
    vis=0;%Display cell tracking? 0=No, 1=Yes.
    vis1scene=1; % display cell tracking for the first scene? 0=No, 1=Yes.
    checkhist=0;%Display image histogram? 0=No, 1=Yes.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    if recrunch==1
        load([basename '_BT'])
    else

    %Determine number of frames
    curdir=cd;
    cd(dirname);
    directory=dir('*.tif');
    T=length(directory);

    cd(curdir);
    path(dirname,path)

    nc=zeros(1,T);
    allcentroids=[];
    cellnum=[];
    tstamp=[];

    %Pre-allocate matrices
    ewav=zeros(1,T);
    ewstd=zeros(1,T);
    ewste=zeros(1,T);
    ewndp=zeros(1,T);
    wav=zeros(1,T);
    wstd=zeros(1,T);
    wste=zeros(1,T);
    vav=zeros(1,T-1);
    vstd=zeros(1,T-1);
    vste=zeros(1,T-1);
    ndp=zeros(1,T-1);
    avav=zeros(1,T-1);
    avstd=zeros(1,T-1);
    avste=zeros(1,T-1);
    a=zeros(1,T);
    w=zeros(1,T);
    sa=zeros(1,T);
    l=zeros(1,T);
    DS=zeros(1,T);
    boun=cell(1,T);
    pole=zeros(1,T);
    mline=cell(1,T);
    outline1=cell(1,T);
    outline2=cell(1,T);

    %Load first image
    imagename=directory(1).name;
    im=imread(imagename);
    [imM,imN]=size(im);
    labels=zeros(imM,imN,T);
    labels2=zeros(imM,imN,T);

    %Track cells
    for t=1:T % changed from T
        display("Scene "+num2str(i0)+", Timepoint "+num2str(t))
        
        %Load image
        imagename=directory(t).name;

        im=imread(imagename);
        [imM,imN]=size(im);

        %De-speckle image
        im=medfilt2(im);

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
        imc=imadjust(imc,[thresh1/65536 1],[]);   

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
        if nc(t)~=0
            a(nc(t),t)=0;
        end
        a(1:nc(t),t)=[stats.Area]';
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

    if vis==1
       figure
       imshow(im)
       hold on
       for k=1:nc(t)
           plot(boun{k,t}(:,1),boun{k,t}(:,2),'-r')
       end
%       savename=['/Users/felixbarber/Documents/Rojas_lab/data/' basename1
%       '/' basename '_seg.png']  % Should change the directory here.
%       saveas(gcf,savename)
      pause
      close all
    end
    
    if vis1scene==1
        if t==1 % Here we do the visualization just for one scene to get
            % a clear sense of what is being tracked and what is not.
           figure
           imshow(im)
           hold on
           for k=1:nc(t)
               plot(boun{k,t}(:,1),boun{k,t}(:,2),'-r')
           end
           savename=[data_loc basename1 '/' basename '_t' sprintf('%03d',t) '_seg.png']
           saveas(gcf,savename)
           close all
        end
    end
    if vis1scene==1
        if t==T % Here we do the visualization just for the final scene 
            % to get a clear sense of what is being tracked and what is not.
           figure
           imshow(im)
           hold on
           for k=1:nc(t)
               plot(boun{k,t}(:,1),boun{k,t}(:,2),'-r')
           end
           savename=[data_loc basename1 '/' basename '_t' sprintf('%03d',t) '_seg.png']
           saveas(gcf,savename)
           close all
        end
    end


    toc

    end

    %Calculate cell length, width, etc.
    for t=1:T
        t
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
             outline1{n,t}=[xc1',yc1'];
             outline2{n,t}=[xc2',yc2'];
             dxy=diff(mline{n,t}).^2;
             dl=sqrt(dxy(:,1)+dxy(:,2));
             l(n,t)=sum(dl);
             % start from here for calculating surface area. Do this based 
             % on conical frustrums, so that the area is calculated using
             % the formula SA=pi*(r1+r2)*(h^2+(r2-r1)^2)^0.5. Note this
             % assumes the conical frustrum is formed by two parallel
             % planes but this doesn't have to be the case if the splines
             % are out of alignment.
             temp_r1 = sqrt((xc1-xc2).^2+(yc1-yc2).^2)/2; % Radius of cell
             temp_r=(temp_r1(1:end-1)+temp_r1(2:end))/2;
             temp1 = (xc1(2:end)+xc2(2:end)-xc1(1:end-1)-xc2(1:end-1)).^2;
             temp2 = (yc1(2:end)+yc2(2:end)-yc1(1:end-1)-yc2(1:end-1)).^2;
             temp_h=0.5*(temp1+temp2).^0.5; % This gives the height of
             % the conical frustrum
             sa_segments = pi*(temp_r1(1:end-1)+temp_r1(2:end))...
                 .*(temp_h.^2+(temp_r1(1:end-1)-temp_r1(2:end)).^2).^0.5;
             sa(n,t)=sum(sa_segments);
             
             %Calculate width
             ls=[0 cumsum(dl)'];
             [~,mpos1]=min(abs(ls/l(n,t)-0.25));
             [~,mpos2]=min(abs(ls/l(n,t)-0.75));

             widths=sqrt((xc1-xc2).^2+(yc1-yc2).^2);
             w(n,t)=max(widths); % Changed this to be maximum since it 
             % seems to better describe the width changes observed during 
             % loss of cell shape
%              w(n,t)=(widths(mpos1)+widths(mpos2))/2;

        end
    end


    %Extract timepoints from metadata if it exists
    if exist('metaname')==1
        if exist(metaname)==2
            %Extract timepoints from metadata
            tpoints=metadata(metaname);

            %Fix bug where micromanager screws up its timing
            dtime=diff(tpoints(1,:));
            fdt=find(dtime>2*(dtime(1)));
            if isempty(fdt)~=1
                fdt=fdt(1);
                tpoints(:,fdt+1:end)=tpoints(:,fdt+1:end)-tpoints(1,fdt+1)+tpoints(1,fdt)+(tpoints(1,fdt)-tpoints(1,fdt-1));
            end
        else
            tpoints=[0:T-1]*tscale;
        end
    else
        tpoints=[0:T-1]*tscale;
    end

    time=tpoints(1,:);
    time2=tpoints(end,:);

    %Fix bug where micromanager screws up its timing
    dtime=diff(time);
    fdt=find(dtime>2*(dtime(1)));
    if isempty(fdt)~=1
        fdt=fdt(1);
        time(fdt+1:end)=time(fdt+1:end)-dtime(fdt)+dtime(fdt-1);
        time2(fdt+1:end)=time2(fdt+1:end)-dtime(fdt)+dtime(fdt-1);
    end

    %Track cells frame to frame
    tracks=zeros(size(im));
    rcents=round(allcentroids);
    linind=sub2ind(size(im),rcents(:,2),rcents(:,1));
    tracks(linind)=1;

    nhood=[0,1,0;1,1,1;0,1,0];
    tracks=imdilate(tracks,strel('disk',cellLink));
    overlay1=imoverlay(im,tracks,[.3 1 .3]);

    [tracksL,ncells]=bwlabel(tracks,8);

    lcell=zeros(ncells,T);
    wcell=zeros(ncells,T);
    acell=zeros(ncells,T);
    pcell=zeros(ncells,T);
    sacell=zeros(ncells,T);
    B=cell(ncells,T);
    pixels=cell(ncells,T);
    mlines=cell(ncells,T);
    lcents=length(allcentroids);

    for i=1:lcents
        cellid=tracksL(linind(i));
        lcell(cellid,tstamp(i))=l(cellnum(i),tstamp(i));
        wcell(cellid,tstamp(i))=w(cellnum(i),tstamp(i));
        sacell(cellid,tstamp(i))=sa(cellnum(i),tstamp(i));
        acell(cellid,tstamp(i))=a(cellnum(i),tstamp(i));
        B{cellid,tstamp(i)}=boun{cellnum(i),tstamp(i)};
        pixels{cellid,tstamp(i)}=pxls{cellnum(i),tstamp(i)};
        mlines{cellid,tstamp(i)}=mline{cellnum(i),tstamp(i)};
        pcell(cellid,tstamp(i))=pole(cellnum(i),tstamp(i));
    end

    %Throw away cells with only one or two time points
    delind=[];
    for i=1:ncells
        if tracking==1
            if length(nonzeros(lcell(i,:)))<=2
                delind=[delind;i];
            end
        end
    end

    lcell(delind,:)=[];
    wcell(delind,:)=[];
    sacell(delind,:)=[];
    acell(delind,:)=[];
    pcell(delind,:)=[];
    B(delind,:)=[];
    pixels(delind,:)=[];
    mlines(delind,:)=[];
    [ncells,~]=size(lcell);

    lcell(lcell==0)=NaN;
    wcell(wcell==0)=NaN;
    acell(acell==0)=NaN;
    sacell(sacell==0)=NaN;
    pcell(pcell==0)=NaN;

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

    %Calculate circumferential strain
    wcell(isnan(wcell))=0;
    ew=zeros(size(lcell));
    for i=1:ncells
        ew(i,:)=wcell(i,:)/mean(wcell(i,:));
    end

    %Calculate the growth rate
    deltat=time(2:end)-time(1:end-1);
    v=(lcell(:,2:end)-lcell(:,1:end-1))./((lcell(:,1:end-1)+lcell(:,2:end))/2);
    av=(acell(:,2:end)-acell(:,1:end-1))./((acell(:,1:end-1)+acell(:,2:end))/2);
    for i=1:ncells
        v(i,:)=v(i,:)./deltat;
        av(i,:)=av(i,:)./deltat;
    end

    %Calculate total length of all cells
    lcell(isnan(lcell))=0;
    acell(isnan(acell))=0;
    for t=1:T
        ltotal(t)=sum(nonzeros(l(:,t)));
        atotal(t)=sum(nonzeros(a(:,t)));
    end
    lcell(lcell==0)=NaN;
    acell(acell==0)=NaN;

    %Throw out outliers and calculate the average width,strain and strain rate 
    %across cells
    v(isnan(v))=0;
    av(isnan(av))=0;
    ew(isnan(ew))=0;

    for t=1:T-1
        vav(t)=mean(nonzeros(v(:,t)));
        vstd(t)=std(nonzeros(v(:,t)));
    end
    vavm=ones(ncells,1)*vav;
    vstdm=ones(ncells,1)*vstd;

    inddel=abs(v-vavm)>2*vstdm&vstdm~=0;

    v(inddel)=0;
    av(inddel)=0;
    lcell(inddel)=0;
    acell(inddel)=0;
    sacell(inddel)=0;
    wcell(inddel)=0;
    ew(inddel)=0;

    for t=1:T
        wav(t)=mean(nonzeros(wcell(:,t)));
        wstd(t)=std(nonzeros(wcell(:,t)));
        wste(t)=wstd(t)./length(nonzeros(wcell(:,t)));
        ewav(t)=mean(nonzeros(ew(:,t)));
        ewstd(t)=std(nonzeros(ew(:,t)));
        ewste(t)=ewstd(t)./length(nonzeros(ew(:,t)));
    end
    for t=1:T-1
        vav(t)=mean(nonzeros(v(:,t)));
        vstd(t)=std(nonzeros(v(:,t)));
        ndp(t)=length(nonzeros(v(:,t)));
        vste(t)=vstd(t)/sqrt(ndp(t));
        avav(t)=mean(nonzeros(av(:,t)));
        avstd(t)=std(nonzeros(av(:,t)));
        avste(t)=avstd(t)/ndp(t);
    end

    v(v==0)=NaN;
    av(av==0)=NaN;
    lcell(lcell==0)=NaN;
    wcell(wcell==0)=NaN;
    sacell(sacell==0)=NaN;
    acell(acell==0)=NaN;
    ew(ew==0)=NaN;

    end

    %Plot data
    figure(1), title('Cell Length vs. Time')
    clf
    hold on
    for i=1:ncells  
        lcell(i,:)=movingaverage2(lcell(i,:),3);
        %indx=isnan(lcell(i,:))~=1;
        %indx=find(indx);
        %plot(time(indx),lcell(i,indx))
        plot(time(1:end),lcell(i,1:end)) 
    end
    xlabel('Time (s)')
    ylabel('Length (\mum)')
    fig2pretty

    figure(2), title('Cell Width vs. Time')
    hold on
    for i=1:ncells
        plot(time,wcell(i,:)) 
    end
    plot(time,wav,'-r','LineWidth',2)
    xlabel('Time (s)')
    ylabel('Width (/mum)')
    fig2pretty

%     % figure(4), title('Circumferential Strain vs. Time')
%     % hold on
%     % for i=1:ncells
%     %     plot(time,ew(i,:)) 
%     % end
%     % plot(time,ewav,'-r','LineWidth',2)
%     % xlabel('t (s)')
%     % ylabel('\epsilon_w')
%     % fig2pretty

    tmid=(time(2:end)+time(1:end-1))/2;

    figure(5), title('Elongation Rate vs. Time')
    hold on
    for i=1:ncells
        plot(tmid,v(i,:))
    end
    plot(tmid,vav,'-r')
    xlabel('Time (s)')
    ylabel('Elongation Rate (s^{-1})')
    fig2pretty

    figure(6), title('Elongation Rate vs. Time')
    hold on
    ciplot((vav-vstd)*3600,(vav+vstd)*3600,tmid,[0.75 0.75 1])
    plot(tmid,vav*3600,'-r')
    xlabel('Time (s)')
    ylabel('Elongation (hr^{-1})')
    fig2pretty

    cd(dirname);
    save([basename '_BT_felix'])
    save([basename '_BTlab_felix'],'labels','labels2','-v7.3')
end