sudo apt purge raspi-firmware -y
sudo rm -rf /etc/kernel/postinst.d/z50-raspi-firmware
sudo rm -rf /etc/initramfs/post-update.d/z50-raspi-firmware
sudo apt update -yq
sudo apt dist-upgrade -fyq

sudo apt install openssh-server ntpdate git cmake -y

#sudo mkdir /clusterfs
#sudo chown nobody.nogroup -R /clusterfs
#sudo chmod 777 -R /clusterfs
sudo apt install nfs-kernel-server nfs-common python3-full python3-pip -y

# pull llama.cpp and compile, build everything
cd /home/user/
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp/
git fetch
git pull

cmake -B build -DGGML_RPC=ON -DLLAMA_SERVER_SSL=ON
cmake --build build --config Release  -j

# Copy compiled tools
#COPY --from=builder /app/llama.cpp/build/src/*.so /usr/lib/x86_64-linux-gnu
#COPY --from=builder /app/llama.cpp/build/ggml/src/*.so /usr/lib/x86_64-linux-gnu
#COPY --from=builder /app/llama.cpp/build/ggml/src/ggml-rpc/*.so /usr/lib/x86_64-linux-gnu
#COPY --from=builder /app/llama.cpp/build/bin/rpc-server .
#COPY --from=builder /app/llama.cpp/build/bin/llama-cli .
#COPY --from=builder /app/llama.cpp/build/bin/llama-embedding .
#COPY --from=builder /app/llama.cpp/build/bin/llama-server .


#if [[  strcmp( $ ( tail -n 1 /etc/fstab ) , "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0" ) ]]; then
#echo "nfs already added"
#else
#echo "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0" | sudo tee -a /etc/fstab
#fi


#adding lolbanner.sh aliaces
echo lolbanner.sh >> .bash_aliases

git lfs install 
git clone https://huggingface.co/rhasspy/piper-voices ~/models/voices

#install visuals
cd ~
sudo apt install lolcat figlet
mkdir ~/.local/share/fonts/
git clone https://github.com/xero/figlet-fonts.git ~/.local/share/fonts/
sudo apt install hollywood
sudo apt install sl 
sudo apt install fortune 
sudo apt install cowsay 
sudo apt install toilet
sudo apt install cmatrix

#install sillytavern or koboltcpp or similar frontend


git clone https://github.com/bartobri/no-more-secrets.git 
cd ./no-more-secrets
make nms
make sneakers             ## Optional
sudo make install

#add ssh key
cd /home/user/.ssh
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
python3 -m venv ~/.local --system-site-packages
~/.local/bin/pip install piper-tts -y 
~/.local/bin/pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
#probably need to add this bit to startup
source ~/.local/bin/activate

sudo apt-get install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg -y
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
#curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - &&\
sudo apt-get update
sudo apt-get install -y nodejs


#install Whipsper.cpp
cd /home/user/
sudo apt-get install libsdl2-dev -y
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp/
bash ./models/download-ggml-model.sh base.en
make main stream command talk talk-llama

#see https://stackoverflow.com/questions/62503731/invalid-mit-magic-cookie-1-key-when-locally-running-mpi-application-or-starting
export HWLOC_COMPONENTS="-gl"

# Install Paddler
echo "Installing Paddler..."
# Define Paddler version - check https://github.com/distantmagic/paddler/releases for the latest version
PADDLER_VERSION="v1.2.0"
PADDLER_ARCHIVE="paddler-${PADDLER_VERSION}-linux-amd64.tar.gz"
PADDLER_URL="https://github.com/distantmagic/paddler/releases/download/${PADDLER_VERSION}/${PADDLER_ARCHIVE}"

# Download Paddler
cd /tmp # Work in a temporary directory
echo "Downloading Paddler from ${PADDLER_URL}"
if ! wget -q "${PADDLER_URL}"; then
    echo "Error: Failed to download Paddler. Please check the URL or network connection."
    # Optionally, try with curl as a fallback or instruct user
    # if ! curl -sLO "${PADDLER_URL}"; then
    #    echo "Error: Failed to download Paddler with curl as well."
    # fi
else
    echo "Paddler downloaded successfully."

    # Extract Paddler
    echo "Extracting Paddler..."
    if ! tar -xzf "${PADDLER_ARCHIVE}"; then
        echo "Error: Failed to extract Paddler archive."
    else
        echo "Paddler extracted successfully."

        # Make executable and move to PATH
        if [ -f "./paddler" ]; then
            echo "Making Paddler executable..."
            chmod +x ./paddler
            echo "Moving Paddler to /usr/local/bin..."
            if sudo mv ./paddler /usr/local/bin/; then
                echo "Paddler installed successfully to /usr/local/bin/paddler"
                echo "You can verify by running: paddler --version"
            else
                echo "Error: Failed to move Paddler to /usr/local/bin. sudo permissions might be required or /usr/local/bin not writable."
            fi
        else
            echo "Error: paddler executable not found after extraction."
        fi
    fi

    # Clean up downloaded archive
    echo "Cleaning up downloaded archive..."
    rm -f "${PADDLER_ARCHIVE}"
fi
# End of Paddler Installation

cd /home/user/llama-cluster-upbringing-script



