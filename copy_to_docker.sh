# copy files from docker
docker cp 33b1502d2fa7:/home/bayram/byk/ktools/output ./output

# copy files into docker
docker cp ./bundle 33b1502d2fa7:/home/bayram/byk/ktools/output 

# 
docker exec -it 33b1502d2fa7 bash

# zip files
zip -r output.zip output/


# build docker image
docker build -t krane .
docker build --no-cache -t krane .

# run image
docker run -it --rm krane