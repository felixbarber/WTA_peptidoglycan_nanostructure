    %BacTrack.m
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

%Calls on the following m-files:
%norm16bit.m
%polefinder.m
%cellcurvature.m
%metadata.m
%extrema.m
%EffectiveLength.m
%fig2pretty.m
%movingaverage.m

clear
close all

tic
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%User Input
% % % 

basename1="/221012_bFB69_Tun_gr_HADA";
cond="120min";
date="221012";

% basename1="/220309_bFB69_Tun_gr_HADA";
% cond="60min";
% date="220309";

% basename1="/221214_bFB7_HADA_Tun";
% date="221214"
% % cond="LB";
% % cond="0min";
% % cond="5min";
% cond="10min";

% basename1="/220120_bFB7_HADA_Tun";
% date="220120"
% % cond="LB";
% % cond="5min";
% % cond="10min";
% cond="15min";

% basename1="/250616_bFB6_xylose_depletion_HADA";
% date="250616"
% % cond="0min";
% % cond="15min";
% cond="30min";
% % cond="60min";

% basename1="/250612_bFB66_EDADA_tun_full";
% date="250612"
% cond="LB";
% % cond="tun_hi";
% % cond="fos";
% % cond="untreated";
% % cond="van";

% basename1="/250613_bFB66_EDADA_tun_full";
% date="250613"
% % cond="LB";
% % cond="tun";
% % cond="fos";
% % cond="unstained";
% % cond="tun_van";
% cond="LB_van";

% basename1="/250613_bFB66_EDADA_tun_full_rep2";
% date="250613"
% cond="LB";
% cond="tun";
% cond="fos";
% cond="unstained";
% cond="tun_van";
% cond="LB_van";

% basename1="/250616_bFB66_EDADA";
% date="250616"
% cond="LB";
% cond="Tun";
% cond="fos";
% cond="tun_van";
% cond="van";
% cond="untreated";

% basename1="/250610_bFB66_tun_EDADA";
% date="250610"
% cond="tun_2_PI_day2";
% cond="tun_1_PI_day2";
% cond="LB_1_PI_day2";
% cond="LB_2_PI_day2";
% cond="LB_1";
% cond="LB_2";
% cond="tun_1";
% cond="tun_2";
% 
% basename1="/250311_width_analysis";
% % cond="bFB7";
% % cond="bFB8";
% % cond="bFB66";
% % cond="bFB87";
% % cond="bFB93";
% cond="bFB69";
% track=0;

% basename1="/241130_bFB69_GlpQ_antibody_pads";
% % cond="Buffer";
% % cond="GlpQ";
% cond="Control";

% basename1="/241129_bFB69_GlpQ_antibody_staining_pads";
% cond="Buffer";
% % cond="GlpQ";
% % cond="Control";

% basename1="/241126_bFB69_GlpQ_antibody_staining_pads";
% % cond="Buffer";
% cond="GlpQ";

% basename1="/241121_bFB69_GlpQ_antibody_staining";
% cond="Buffer";
% % cond="GlpQ";

% basename1="/241117_bFB69_LB_WGA_control";
% cond="LB";
% % cond="10min";

% basename1="/241115_bFB69_LB_Van_control";
% % cond="LB";
% cond="10min";


% basename1="/241114_bFB69_Tun_Van_pads";
% cond="Tun";
% cond="LB";
% cond="LB_v2";

% basename1="/241114_bFB66_GlpQ_Van_pads";
% cond="GlpQ";
% % cond="Buffer";

% basename1="/241113_bFB69_Tun_HADA";
% % cond="LB";
% % cond="0min";
% % cond="5min";
% cond="10min";
% date="241113";

% basename1="/241113_bFB69_Tun_Van_pads_v2";
% % cond="Tun";
% cond="LB";

% basename1="/241113_bFB69_Tun_Van_pads_v1";
% cond="Tun";
% % cond="LB";

% basename1="/241113_bFB66_GlpQ_Van_pads_v1";
% % cond="GlpQ";
% cond="Buffer";
% 
% basename1="/241112_bFB66_Tun_Van_pads";
% cond="Tun";
% % cond="LB";

% basename1="/241112_bFB66_Tun_WGA_pads";
% % cond="Tun";
% cond="LB";

% basename1="/241112_bFB66_GlpQ_Van_pads";
% cond="GlpQ";
% % cond="Buffer";


% basename1="/241108_bFB66_Tun_Van";
% % cond="Tun";
% cond="LB";

% basename1="/241108_bFB69_GlpQ_WGA_pads_azide";
% % cond="WGA";
% cond="Buffer";

% basename1="/241105_bFB69_GlpQ_WGA_pads";
% cond="GlpQ";
% % cond="Buffer";

% basename1="/241105_bFB66_Tun_Van";
% % cond="Tun";
% cond="LB";    

% basename1="/241025_bFB66_Tun_WGA_pads";
% % cond="Tun";
% % cond="Tun_v1";
% cond="LB";

% basename1="/241024_bFB69_GlpQ_WGA_pads";
% % cond="GlpQ";
% % cond="GlpQ_v1";
% cond="Buffer";

% basename1="/241024_bFB66_Tun_WGA_pads";
% cond="Tun";
% % cond="LB";

% basename1="/241023_bFB69_Tun_WGA_pads";
% % cond="Tun";
% % cond="LB";
% cond="LB_v2";

% basename1="/241022_bFB69_Tun_WGA_pads_LB";
% % cond="Tun";
% cond="LB";


% basename1="/241018_bFB69_WGA_LB_pads";
% cond="Tun";
% % cond="LB";

% basename1="/241015_bFB69_Tun_WGA";
% % cond="Tun";
% cond="LB";

% basename1="/241011_bFB69_Tun_WGA";
% cond="Tun";
% % cond="LB";

% basename1="/241008_bFB69_Tun_WGA";
% % cond="Tun";
% cond="LB";

% basename1="/241007_bFB69_GlpQ_WGA";
% cond="GlpQ";
% % cond="buffer";

% basename1="/240913_bFB66_GlpQ_FLVan";
% cond="PBS";
% % cond="GlpQ";

% basename1="/240912_bFB66_GlpQ_FLVan";
% % cond="PBS";
% cond="GlpQ";


% basename1="/240911_bFB66_Tun_FLVan";
% cond="Tun";
% % cond="LB";

% basename1="/240911_bFB66_FLVan";
% % cond="GlpQ";
% % cond="GlpQ_15min";
% % cond="PBS";
% cond="PBS_15min";

% basename1="/240202_bFB69_Tun_HADA";
% cond="LB";
% % cond="5min";
% % cond="15min";
% % cond="25min";
% date="240202";
% 
% basename1="/240202_bFB205_Tun_HADA";
% date="240202";
% % cond="LB";
% % cond="5min";
% cond="15min";

% basename1="/240131_bFB205_Tun_HADA";
% date="240131";
% cond="LB";
% % cond="0min";
% % cond="5min";
% % cond="10min";

% basename1="/240126_bFB66_Tun_HADA";
% % cond="LB";
% % cond="0min";
% % cond="5min";
% cond="10min";
% date="240126";

% basename1 = '210311_pad_HADA_staining_tunicamycin';
% % cond = '0_5ug_Tun';
% % cond = '5ug_Tun';
% cond = 'LB';


% basename1 = '210401_pad_25min';
% cond = '0_5ug';
% % cond = '5ug';
% % cond = 'LB';


% basename1 = '210401_pad_60min_Tun';
% % cond = '0_5_ug';
% cond = '5_ug';
% % cond = 'LB';

% basename1 = '210402_pad_FB1_HADA_staining_tun';
% % cond = '0_5ug';
% % cond = '5ug';
% % cond = 'LB';
% cond = 'LB_end';

% basename1 = '210402_pad_TagO_Xylose';
% % cond = '0uM_Xylose';
% cond = '10mM_Xylose';
% % cond = '30mM_Xylose';

% basename1= '210408_FB1_25min_Tun_pads';
% cond='5ug';
% % cond='0_5ug';
% % cond='LB';


% basename1= '210408_FB1_10min_Tun_pads';
% cond='0_5ug';
% % cond='LB';

% basename1= '210408_FB1_5min_Tun_pads';
% % cond='0_5ug_v1';
% % cond='0_5ug_v2';
% cond='LB';


% basename1= '/210416_FB2_HADA_Staining';
% date="210416";
% % cond='LB';
% % cond='5min';
% % cond='10min';
% % cond='15min';
% % cond='25min';
% cond='5min_v2';
% 
% basename1= '210401_BS168_LB_HADA';
% cond='LB';

% basename1='210401_BS168_Tun_HADA_expt4';
% cond='0_5ug_Tun';

% basename1= '210429_FB1_HADA_staining_cellasic';
% cond='LB';
% % cond='15min_0_5ugTun';
% % cond='25min_0_5ugTun'; % it had some trouble segmenting this one properly

% basename1= '/210506_FB6_inducer_loss';
% cond='10min';
% % cond='25min';
% % cond='60min';
% % cond='Xylose_induced';
% date="210506";

% basename1='211012_ponA_tun_HADA';
% % cond="bFB1_0_5uM";
% % cond="bFB1_0_25uM";
% % cond="bFB1_0_125uM";
% % cond="bFB1_LB";
% % cond="bFB45_0_5uM";
% % cond="bFB45_0_25uM";
% % cond="bFB45_0_125uM";
% cond="bFB45_LB";

% basename1='211104_ConA_labeling';
% % cond="bER18_GlpQPhoD";
% % cond="bER18_PBS";
% % cond="bFB46_GlpQPhoD";
% % cond="bFB46_PBS";
% cond="bER18_unlabeled";
% 
% basename1="211111_bFB10_ConA_Tun";
% cond="0min";
% cond="0min_v2";
% cond="5min";
% cond="10min";
% cond="15min";
% cond="20min";
% cond="25min";

% basename1="211222_bFB66_ConA_Tun";
% cond="10min";
% 
% basename1="211223_bFB66_ConA_Tun";
% % cond="LB";
% % cond="20min";
% % cond="20min_v2";
% % cond="40min";
% cond="40min_v2";

% basename1="/220104_bFB66_Tun_HADA";
% % cond="LB";
% % cond="0min";
% % cond="5min";
% cond="10min";
% date="220104";
% % 
% basename1="/220104_bFB79_Tun_HADA";
% date="220104";
% cond="LB";
% cond="0min";
% cond="5min";
% cond="10min";

% basename1="220107_bFB66_ConA_primed";
% % cond="LB";
% % cond="LB_v2";
% cond="60min_Tun";
% % cond="60min_Tun_v2";
% 
% basename1="/220111_bFB79_HADA_Tun";
% date="220111";
% % cond="LB";
% % cond="0min";
% % cond="5min";
% cond="10min";

% basename1="/220113_bFB79_HADA_Tun";
% date="220113";
% % cond="LB";
% % cond="15min";
% % cond="5min";
% cond="10min";


% basename1="220120_bFB7_HADA_Tun";
% % cond="LB";
% % cond="15min";
% % cond="5min";
% cond="10min";

% basename1='220121_bFB66_ConA_pads';
% % cond='LB';
% % cond="LB_v2";
% cond="5h_Tun";
% % cond="5h_Tun_v2";


% basename1="220202_bFB8_Tun_HADA";
% cond="LB";
% % cond="15min";
% % cond="5min";
% % cond="10min";

% basename1="/220207_bFB69_Tun_HADA";
% date="220207";
% % cond="LB";
% % cond="15min";
% % cond="5min";
% cond="10min";

% basename1="221205_bFB69_Bocillin_Tun";
% % cond="LB";
% % cond="0min";
% % cond="5min";
% cond="10min";

% basename1="221212_bFB69_Bocillin_Tun";
% cond="LB";
% % cond="0min";
% % cond="5min";
% % cond="10min";
% % cond="5min_v2";

% basename1="221214_bFB7_HADA_Tun";
% % cond="LB";
% % cond="0min";
% % cond="5min";
% cond="10min";

% basename1="/230206_bFB1_HADA_Tun";
% cond="LB";
% % cond="5min";

% basename1="/230203_bFB108_HADA_Tun";
% % cond="LB";
% cond="5min";

% basename1="/230203_bFB107_HADA_Tun";
% cond="LB";
% % cond="5min";



% temp_path='/Volumes/data_ssd1/Rojas_Lab/data';
temp_path='/Volumes/data_ssd2/Rojas_Lab/data';
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% dirname=strcat('D:/Documents_D/Rojas_lab/data/', basename1, '/', cond, '/C1_blur');%Directory that the image stack is saved in.
dirname=strcat(temp_path, basename1, '/', cond, '/C1_blur');%Directory that the image stack is saved in.
dirname
% Note that the dirname has to map to the writable default mount of a mac
% HD, otherwise it kicks up a fuss later.
%basename='070512_6';skp=[];%Name of the image stack, used to save file.    
%metaname=['/Users/Rico/Documents/MATLAB/Matlab Ready/' basename '/metadata.txt'];%Name of metadata file.  Will only work if images were taken with micromanager.
lscale=0.0929;%%Microns per pixel.
tscale=20;%Frame rate.
thresh=0;%For default, enter zero.
% IntThresh=20000;%Threshold used to enhance contrast. Default:35000
IntThresh=10000;%Threshold used to enhance contrast. Default:35000
dr=1;%Radius of dilation before watershed 
sm=2;%Parameter used in edge detection
% minL=2;%Minimum cell length
minL=3;%Minimum cell length
minW=0.2;%Minimum cell width
maxW=2.0;%Maximum cell width, set to 2.0 for tunicamycin shock, but
% maxW=1.5;%Maximum cell width, set to 2.0 for tunicamycin shock, but
% minL=1.5;%Minimum cell length for tun treated cells
% minW=1;%Minimum cell width for tun treated cells
% maxW=3;%Maximum cell width for tagO delete cells or long tun treated cells.
% this was previously set to 1.5 which seemed too low for Tunicamycin shock
minA=170;%Minimum cell area. default 50
cellLink=4;%Number of frames to ignore missing cells when tracking frame to frame
recrunch=0;%Display data from previously crunched data? 0=No, 1=Yes.
vis=1;%Display cell tracking? 0=No, 1=Yes.
vis1scene=1; % display cell tracking for the first scene? 0=No, 1=Yes.
checkhist=0;%Display image histogram? 0=No, 1=Yes.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Determine number of frames
curdir=cd;
cd(dirname);
directory=dir(date+'*.tif');
T=length(directory);

path(dirname,path)

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

%Load first image
imagename=directory(1).name;
imagename
im=imread(imagename);
[imM,imN]=size(im);
labels=zeros(imM,imN,T);
labels2=zeros(imM,imN,T);

%Segment cells
for t=1:T % changed from T
    basename=strcat(basename1,'_',cond,'_s',sprintf('%03d',t),'_C1');
%     out_path = strcat('D:/Documents_D/Rojas_lab/data/', basename1, '/', cond, '/',basename,'_segments.png');
    out_path = strcat(temp_path, basename1, '/', cond, '/',basename,'_segments.png');

    display("Scene "+num2str(t))

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

for t=1:T
    wav(t)=mean(nonzeros(wcell(:,t)));
    wstd(t)=std(nonzeros(wcell(:,t)));
    wste(t)=wstd(t)./length(nonzeros(wcell(:,t)));
    basename=strcat(basename1,'_',cond,'_s',sprintf('%03d',t),'_C1');
%     out_path = strcat('D:/Documents_D/Rojas_lab/data/', basename1, '/', cond, '/',basename,'_segments.png');
    out_path = strcat(temp_path, basename1, '/', cond, '/',basename,'_segments.png');
    out_dir = strcat(temp_path, basename1, '/', cond);
    [row, col] = find(~isnan(lcell(:,t))); % Finding the objects that we don't 
    
    if vis==1
       imagename=directory(t).name;
        
       im=imread(imagename);
       t
       h=figure;
       imshow(im)
       hold on
       for k=1:length(row)
           plot(boun{row(k),t}(:,1),boun{row(k),t}(:,2),'-r')
       end
       F = getframe(gcf);
       [X, Map] = frame2im(F);
%        cd(out_dir);
       imwrite(X,out_path, "png")
%        cd(dirname);
      pause
      close all
    end
end

lcell(lcell==0)=NaN;
wcell(wcell==0)=NaN;
sacell(sacell==0)=NaN;
acell(acell==0)=NaN;

cd(dirname);
outname=strcat(basename1,'_',cond)
% fileattrib(currdir,'+w','u');
save(strcat(dirname,outname,'_BT_felix'))
save(strcat(dirname,outname, '_BTlab_felix'),'labels','labels2','-v7.3')