sudo apt purge raspi-firmware
sudo rm -rf /etc/kernel/postinst.d/z50-raspi-firmware
sudo rm -rf /etc/initramfs/post-update.d/z50-raspi-firmware
sudo apt install openssh-server ntpdate slurm-wlm git -y
#sudo mkdir /clusterfs
#sudo chown nobody.nogroup -R /clusterfs
#sudo chmod 777 -R /clusterfs
sudo apt install nfs-kernel-server nfs-common python3-full python3-pip -y
sudo apt install openmpi-bin openmpi-common libopenmpi-dev libopenmpi3 -y
cd /home/user/
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp/
git fetch
git pull
#slight cludge, ideally use venv for cleaner python install
python3.11 -m pip install -r requirements.txt
make CC=mpicc CXX=mpicxx LLAMA_MPI=1 -j
#if [[  strcmp( $ ( tail -n 1 /etc/fstab ) , "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0" ) ]]; then
#echo "nfs already added"
#else
#echo "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0" | sudo tee -a /etc/fstab
#fi
#sudo -u munge ${sbindir}/mungekey --verbose

cd /home/user/
sudo apt-get install libsdl2-dev -y
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp/
bash ./models/download-ggml-model.sh base.en
make main stream command talk talk-llama

cd /home/user/
sudo cp cgroup.conf cgroup_allowed_devices_file.conf slurm.conf /etc/slurm
sudo cp munge.key /etc/munge/munge.key
sudo chown munge /etc/munge/munge.key
sudo systemctl enable munge
sudo systemctl start munge
systemctl status munge -l
sudo systemctl enable slurmd
sudo systemctl start slurmd
systemctl status slurmd -l
sudo systemctl enable slurmctld
sudo systemctl start slurmctld
systemctl status slurmctld -l
sudo cat /var/log/slurm/slurmctld.log

