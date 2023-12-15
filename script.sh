sudo apt purge raspi-firmware -y
sudo rm -rf /etc/kernel/postinst.d/z50-raspi-firmware
sudo rm -rf /etc/initramfs/post-update.d/z50-raspi-firmware
sudo apt update -y
sudo apt dist-upgrade -y
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

#add ssh key
cat id_rsa.pub >> ~/.ssh/authorized_keys

#slight cludge, ideally use venv for cleaner python install
python3.11 -m pip install -r requirements.txt
sudo apt install -y build-essential python3-venv python3-dev python3-setuptools python3-pip python3-smbus libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl libffi-dev
sudo apt install -y avahi-daemon bash-completion nano vim less tmux

#install ansible
#pip3 install ansible-core -y
sudo apt install ansible
sudo mkdir /etc/ansible
sudo mkdir /etc/ansible/hosts
sudo mkdir /etc/ansible/playbook
sudo mkdir /etc/ansible/scripts

cd /home/user/llama-cluster-upbringing-script
sudo cp inventory.yaml /etc/ansible/hosts
sudo cp playbook.yaml /etc/ansible/playbook
sudo cp run.sh /etc/ansible/scripts

#installs for talk
pip install piper-tts -y
sudo apt-get install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg -y
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
#curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - &&\
sudo apt-get update
sudo apt-get install -y nodejs

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

#see https://stackoverflow.com/questions/62503731/invalid-mit-magic-cookie-1-key-when-locally-running-mpi-application-or-starting
export HWLOC_COMPONENTS="-gl"

cd /home/user/llama-cluster-upbringing-script
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

