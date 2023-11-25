using latest distro from https://www.crunchbangplusplus.org/#download

Username is user, password is a standard password

Bookworm 12.0 MD5 71d02a8e55627ce43e217724dc6de6c5

sudo -u munge ${sbindir}/mungekey --verbose creates the munge.key that will authenticate the cluster

copy the files to the home directory and run ./script.sh

This assumes the name of every computer is AID-E-# where # is a number 0-20, change the hostname to your expected cluster configuration name.


For the docker config image
//Create the Image
docker buildx build . -t gpt-mpi:latest
//Run the image to create a container
docker run -itd gpt-mpi
//Get Container ID or Name
docker ps -a
//Execute a command
docker container exec container_name-or-ID mpirun -hostfile hostfile -n 3 ./main -m ./models/ggml-vocal.bin -p "Whats the meaning of life?" -n 512
