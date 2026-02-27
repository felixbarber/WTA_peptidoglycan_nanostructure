
% User Guide: Written by Felix Barber, 2/27/26

% This script is used to process "timepoint" datasets, where within a
% single experiment you acquire distinct fields of view (usually for different 
% conditions). This is NOT to be used on timelapse imaging, where you track
% the same field of view over long times. The output is saved as .mat
% files.

%The user selects ROIs (regions of interest) within the image to be blurred,
%guided by visual aides for the cell segmentation. If you click "enter"
%without making any selections, it will not overwrite a given output if one
%exists. For future development could consider dilating a binary image of
%cell masks and blurring everything else in addition to the points of
%selection.

%INPUTs:
%temp_path: Directory in which the experimental datasets are saved
% basename1: Experiment ID (the name of your folder for that experiment)
% cond: The individual experimental condition (iterate through each individual 
% subfolder within your experiment).

%Calls upon:
%norm16bit.m This cannot be run without adding the Cell_Tracking directory 
% to the path.

clear
close all

tic

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%USER INPUT

% These variables are usually "set and forget"
erase_pillars=0;  % Set this to 1 if you need to remove regularly spaced
% pillars within your image. Set to zero otherwise.
temp_path='/Users/barber.527/Documents/Rojas_Lab/data/' % Adjust this path
% to where you have saved your experiment data folders.
imscale = 100; % set this to be smaller if you are only seeing part of your 
% image


% These variables need to be changed for each new experiment
basename1="/260211_WT_pulse_chase";
cond="sample_4";
date="260211";

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
dirname=strcat(temp_path, basename1, '/', cond, '/C1');%Directory that the image stack is saved in.
out_dir=strcat(temp_path, basename1, '/', cond, '/C1_blur');


if ~exist(out_dir, 'dir')
   mkdir(out_dir)
end


curdir=cd;

cd(dirname);
directory=dir('2*.tif');
L=length(directory);
path(dirname,path)

for t=1:L
    t
    imagename=directory(t).name;
    im1=imread(imagename);
    repeat=1; % This is the variable that allows us to keep iterating until we 
    % are satisfied with our clearance (i.e. until we don't add any further
    % areas to remove

    repnum=0
    while repeat==1;
    
        
        [imM,imN]=size(im1);
        
        %%%%%%%%%%%%%%%%%%%%%%%% Doing the segmentation on this image,
        % minimally modified from Rico's segmentation code.
        
        lscale=0.065;%%Microns per pixel. Set to 0.0929 for Rojas Lab,
        % 0.065 for Barber Lab camera at 100X mag.
        tscale=20;%Frame rate.
        thresh=0;%For default, enter zero.
        IntThresh=10000;%Threshold used to enhance contrast. Default:35000
        dr=1;%Radius of dilation before watershed 
        sm=2;%Parameter used in edge detection
        minL=3;%Minimum cell length
        minW=0.2;%Minimum cell width
        maxW=2.0;%Maximum cell width, set to 2.0 for tunicamycin shock, but
        % this was previously set to 1.5 which seemed too low for Tunicamycin shock
        minA=170;%Minimum cell area. default 50
        cellLink=4;%Number of frames to ignore missing cells when tracking frame to frame
        recrunch=0;%Display data from previously crunched data? 0=No, 1=Yes.
        vis=1;%Display cell tracking? 0=No, 1=Yes.
        vis1scene=1; % display cell tracking for the first scene? 0=No, 1=Yes.
        checkhist=0;%Display image histogram? 0=No, 1=Yes.
    
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%% This is the segmentation part
    
        T=1;
        
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
    
        
        ppix=0.5;
        im2=norm16bit(im1,ppix);
    
        figure,imshow(im1,stretchlim(im1)*65000, 'InitialMagnification', imscale)
        set(gcf,'Pointer','fullcross')
        hold on
        for k=1:length(row)
           plot(boun{row(k),t}(:,1),boun{row(k),t}(:,2),'-r')
        end
        axis manual

        % Now we automatically erase the pillars since we know the grid spacing
        % is regular. First we have to help out by aligning the orientation of
        % the grid, clicking on two pillars in the same horizontal row.
        count=0;
        if and(erase_pillars,repnum==0)  % Only do this once per image
    %     point1=get(gca,'CurrentPoint');   
    %     finalRect=rbbox;                   
    %     %pause
    %     point2=get(gca,'CurrentPoint');  
    %     temp_xy=(point1(1,1:2)+point2(1,1:2))/2;
        
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
            box_size = [50,50];
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
            
        else
            k=0;
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
        end
        
        
        % Now that we've isolated the parts of interest, we make a copy, and
        % blur those regions
        temp_im2=imgaussfilt(im1,20);
        for n=1:count
            %Load image
            [imcounts,bins]=hist(double(nonzeros(im1)));
            [~,mpos]=max(imcounts);
            val=bins(mpos);
            im1(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1))=temp_im2(rp1(n,2):rp2(n,2),rp1(n,1):rp2(n,1));
        end
        curdir=cd;
        cd(out_dir);
        if or(count~=0,~isfile(imagename))  % If we either marked something 
            % in the current image, or there is nothing in the output location
            % then we save the file
            imwrite(im1,imagename);
        end
        cd(curdir);
        close all
        if count==0;
            repeat=0;
        end
        repnum=repnum+1;
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Now, we apply the same calculations to perform the actual segmentation.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dirname=strcat(temp_path, basename1, '/', cond, '/C1_blur');%Directory that the image stack is saved in.

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
    out_path = strcat(temp_path, basename1, '/', cond, '/',basename,'_segments.png');
    out_dir = strcat(temp_path, basename1, '/', cond);
    [row, col] = find(~isnan(lcell(:,t))); % Finding the objects that we don't 
    
    if vis==1
       imagename=directory(t).name;
        
       im=imread(imagename);
       t
       h=figure;
       imshow(im, 'InitialMagnification', imscale);
       hold on
       for k=1:length(row)
           plot(boun{row(k),t}(:,1),boun{row(k),t}(:,2),'-r')
       end
       F = getframe(gcf);
       [X, Map] = frame2im(F);
%        cd(out_dir);
       imwrite(X,out_path, "png")
%        cd(dirname);
      % pause
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


% cd('D:/Documents_D/Rojas_lab/data/');
cd(temp_path);
close all
clear all