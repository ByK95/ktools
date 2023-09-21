# copy files from docker
docker cp 2c77742fef8d:/home/bayram/byk/ktools/files ./files

# copy files into docker
docker cp ./files 2c77742fef8d:/home/bayram/byk/ktools/files 

# zip files
zip -r output.zip output/