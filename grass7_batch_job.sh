g.proj -c proj4="+proj=utm +zone=43 +datum=WGS84 +units=m +no_defs"
v.in.ogr min_area=0.0001 snap=-1 input="/media/office/New Volume/Research/Sukhjit/ExperimentalDataThesis/Heremap/merged/utm43" layer=Here_mereged_3_UTM43 output=tmp1501946422113 --overwrite -o
g.region n=3595353.05356 s=3268595.87758 e=686792.182365 w=392866.383828 res=100
v.clean  input="tmp1501946422113" tool=rmline threshold="0" output=output4137db4e5ccf426d8e6469989f0d5704 error=error4137db4e5ccf426d8e6469989f0d5704 --overwrite
v.out.ogr -s -e input=output4137db4e5ccf426d8e6469989f0d5704 type=auto output="/tmp/processing91416a2ad8c6405e830467de79ce39f8/9e67a316331c467eb364c02c3c3baaa9" format=ESRI_Shapefile output_layer=output --overwrite
v.out.ogr -s -e input=error4137db4e5ccf426d8e6469989f0d5704 type=auto output="/tmp/processing91416a2ad8c6405e830467de79ce39f8/4a17e739dade420e9f0e554a265ef773" format=ESRI_Shapefile output_layer=error --overwrite
exit