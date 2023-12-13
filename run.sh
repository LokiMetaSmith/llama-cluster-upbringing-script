# Start a new chat
PROMPT_CACHE_FILE=chat.prompt.bin CHAT_SAVE_DIR=./chat/default ./examples/chat-persistent.sh

# Resume that chat
PROMPT_CACHE_FILE=chat.prompt.bin CHAT_SAVE_DIR=./chat/default ./examples/chat-persistent.sh

# Start a different chat with the same prompt/model
PROMPT_CACHE_FILE=chat.prompt.bin CHAT_SAVE_DIR=./chat/another ./examples/chat-persistent.sh

# Different prompt cache for different prompt/model
PROMPT_TEMPLATE=./prompts/chat-with-bob.txt PROMPT_CACHE_FILE=bob.prompt.bin \
    CHAT_SAVE_DIR=./chat/bob ./examples/chat-persistent.sh


    1  ls
    2  ssh user@AID-E-1
    3  sftp user@AID-E-1
    4  ls
    5  cat script.sh 
    6  ./script.sh 
    7  sinfo
    8  ls
    9  cat script.sh 
   10  echo "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0" | sudo tee -a /etc/fstab
   11  sudo cat /etc/fstab
   12  sudo reboot now
   13  ls
   14  cd llama.cpp/
   15  ls
   16  cd models
   17  ls
   18  cd /etc/fstab
   19  ls
   20  sudo nano /etc/fstab
   21  ls
   22  cd ..
   23  ls
   24  cd models
   25  ls
   26  systemctl restart nfs-server.service
   27  ls
   28  cd ..
   29  hostname
   30  sview
   31  sinfo
   32  pin AID-E-1
   33  ping AID-E-1
   34  sinfo
   35  ls models/
   36  sudo apt install nfs-common -y
   37  ls
   38  cd ..
   39  ls
   40  sudo apt purge raspi-firmware
   41  ls
   42  ./script.sh 
   43  git clone git@github.com:ggerganov/whisper.cpp.git
   44  git clone https://github.com/ggerganov/whisper.cpp.git
   45  cd whisper.cpp/
   46  ls
   47  bash ./models/download-ggml-model.sh base.en
   48  make
   49  ./main -f samples/jfk.wav
   50  make WHISPER_CLBLAST=1
   51  ls
   52  sudo apt install clblast
   53  sudo apt install clblast-utils
   54  sudo rm /etc/initramfs/post-update.d/z50-raspi-firmware 
   55  sudo apt install openplas
   56  sudo apt install open
   57  ls
   58  cd whisper.cpp/
   59  make WHISPER_CLBLAST=1
   60  ls
   61  sudo apt install libclblast1
   62  sudo apt install libclblast-dev 
   63  make WHISPER_CLBLAST=1
   64  ./main -f samples/jfk.wav
   65  make WHISPER_CLBLAST=1 WHISPER_OPENBLAS=1 -j
   66  make clean
   67  make WHISPER_CLBLAST=1 WHISPER_OPENBLAS=1 -j
   68  sudo apt install libblas-dev
   69  make WHISPER_CLBLAST=1 WHISPER_OPENBLAS=1 -j
   70  sudo apt install libblas3
   71  sudo apt install libopenblas-serial-dev
   72  make WHISPER_CLBLAST=1 WHISPER_OPENBLAS=1 -j
   73  ./main -f samples/jfk.wav
   74  sudo apt install libopenblas-dev
   75  make clean
   76  make WHISPER_CLBLAST=1 WHISPER_OPENBLAS=1 -j
   77  ./main -f samples/jfk.wav
   78  sudo apt install ocl-icd-opencl-dev
   79  sudo apt install intel-opencl-icd 
   80  ./main -f samples/jfk.wav
   81  make WHISPER_CLBLAST=1 WHISPER_OPENBLAS=1 -j
   82  make clean
   83  make WHISPER_CLBLAST=1 WHISPER_OPENBLAS=1 -j
   84  ./main -f samples/jfk.wav
   85  gcc -version
   86  gcc --version
   87  cd ..
   88  ls
   89  cd llama.cpp/
   90  ls
   91  ./main -p "what color is the sky?"
   92  ls
   93  cd models/
   94  ls
   95  cd ..
   96  cat /etc/exports
   97  systemctl start nfsd
   98  srun hostname
   99  ls
  100  cd llama.cpp/
  101  ls
  102  cd models/
  103  ls
  104  cd ..
  105  cd /
  106  ls
  107  cd mnt
  108  ls
  109  cd ..
  110  ls
  111  sudo mount -t AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models
  112  sudo mount -t AID-E-1:models /home/user/llama.cpp/models
  113  sudo mount -t AID-E-1:
  114  sudo mount -t AID-E-1: /home/user/llama.cpp/models
  115  mount
  116  cd /ect/fstab
  117  sudo nano /ect/fstab
  118  sudo nano /etc/fstab
  119  sudo mount -t AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models
  120  cat /etc/fstab
  121  sudo mount -t AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0 
  122  sudo mount -t AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs 
  123  mount --help
  124  sudo mount -a
  125  sudo nano /etc/fstab
  126  sudo mount -a
  127  sudo apt ins tall nfs-common
  128  sudo apt install nfs-common
  129  sudo apt install nfs-utils
  130  sudo nano /etc/fstab
  131  sudo mount -a
  132  showmount
  133  mount -v
  134  cat /etc/fstab
  135  cat /etc/exports
  136  sudo mount -a
  137  sudo reboot now
  138  top
  139  sudo top
  140  sinfo
  141  top
  142  sudo mount -a
  143  cd /etc/nfs.conf.d/
  144  ls
  145  cd ..
  146  cat nfs.conf
  147  ls
  148  cd ~
  149  ls
  150  cd llama.cpp/
  151  ls
  152  cd models/
  153  ls
  154  cd ..
  155  nfs
  156  mount | grep nfs
  157  mount -o nfsvers=4 AID-E-1:/home/user/llama.cpp/models ./models
  158  mount -o nfsvers=4 AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models
  159  mount AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models
  160  sudo mount AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models
  161  ls
  162  cd models
  163  ls
  164  cd ..
  165  ls
  166  main
  167  ./main
  168  ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -n 128
  169  top
  170  sinfo
  171  $ mpirun   ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 64
  172  mpirun   ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 64
  173  sinfo
  174  mpirun   ./main -m ./models/ggml-model-q4_0.bin -p "I believe the meaning of life is" -n 64
  175  Invalid MIT-MAGIC-COOKIE-1 key
  176  cp ./models/ggml-model-q4_0.bin ./
  177  cp ./models/ggml-model-q4_0.bin .
  178  ls
  179  mpirun   ./main -m ./ggml-model-q4_0.bin -p "I believe the meaning of life is" -n 64
  180  make -j && ./main -m ./ggml-model-q4_0.bin -p "Building a website can be done in 10 simple steps:" -n 512
  181  Invalid MIT-MAGIC-COOKIE-1 key
  182  cd ..
  183  ls
  184  mkdir models
  185  cd models
  186  wget 
  187  wget https://huggingface.co/Pi3141/alpaca-native-7B-ggml/resolve/397e872bf4c83f4c642317a5bf65ce84a105786e/ggml-model-q4_0.bin
  188  cd ..
  189  ls
  190  cd llama
  191  cd llama.cpp/
  192  ls
  193  make clean
  194  git pull
  195  make -j
  196  ls
  197  python3
  198  python3 -m pip install -r requirements.txt 
  199  python3 -m pip3 install -r requirements.txt 
  200  pip
  201  sudo apt-get install pip3
  202  sudo apt-get install python3
  203  sudo apt-get install python3-pip
  204  python3 -m pip3 install -r requirements.txt 
  205  python3 -m pip install -r requirements.txt 
  206  python -m pip install -r requirements.txt 
  207  sudo apt-get install python3-full
  208  python3 -m pip install -r requirements.txt 
  209  python3 -m venv ~
  210  python3 -m pip3 install -r requirements.txt 
  211  python3.11 -m pip3 install -r requirements.txt 
  212  python3.11 -m pip install -r requirements.txt 
  213  ./main -m ./ggml-model-q4_0.bin -p "I believe the meaning of life is" -n 64
  214  ./scripts/verify-checksum-models.py 
  215  ls models/
  216  cd models
  217  git clone https://huggingface.co/TheBloke/Llama-2-7B-GGML
  218  cd ..
  219  ./scripts/verify-checksum-models.py 
  220  ls
  221  cd models
  222  ls
  223  cd Llama-2-7B-GGML/
  224  ls
  225  cd ..
  226  ./main -m ./models/Llama-2-7B-GGML/llama-2-7b.ggmlv3.q2_K.bin -p "I believe the meaning of life is" -n 64
  227  ./main -m ./models/Llama-2-7B-GGML/llama-2-7b.ggmlv3.q2_K.bin -p "I believe the meaning of life is" 
  228  ./main -m ./models/Llama-2-7B-GGML/llama-2-7b.ggmlv3.q4_0.bin -p "I believe the meaning of life is" 
  229  ls
  230  ./examples/chat.sh
  231  ls
  232  cd models
  233  ls
  234  mv Llama-2-7B-GGML/ 7B
  235  ls
  236  ./examples/chat.sh
  237  cd ..
  238  ./examples/chat.sh
  239  ./main -m ./models/7B/llama-2-7b.ggmlv3.q4_0.bin -p "I believe the meaning of life is" 
  240  ./main -m ./models/7B/llama-2-7b.ggmlv3.q2_K.bin -p "I believe the meaning of life is" 
  241  ./main -m ./models/7B/llama-2-7b.ggmlv3.q2_K.bin -p "I believe the meaning of life is" -n 32 -t 2 
  242  ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 2 
  243  time
  244  time ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 2 
  245  time ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 4 
  246  time ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 3
  247  time ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 1
  248  time ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 2
  249  make CC=mpicc CXX=mpicxx LLAMA_MPI=1 -j
  250  time ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 2
  251  mpirun  ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 2
  252  mpirun  ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is"  -t 2
  253  time ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 2
  254  ls
  255  time ./main -m ./models/ggml-vocab.bin -p "I believe the meaning of life is" -n 32 -t 2
  256  time ./main -m ./models/ggml-model-q4_0.bin -p "I believe the meaning of life is" -n 32 -t 2
  257  cd ..
  258  ls
  259  cd whisper.cpp/
  260  ls
  261  cd examples/
  262  ls
  263  cd stream
  264  ls
  265  cd ..
  266  cd command
  267  ls
  268  cd ..
  269  ls
  270  cd ..
  271  make stream
  272  make clean
  273  make stream
  274  sudo apt-get install libsdl2-dev 
  275  ls
  276  cd examples/
  277  ls
  278  cd stream
  279  ls
  280  cd ..
  281  make stream
  282  ls
  283  make stream
  284  ./stream -m ./models/ggml-base.en.bin -t 8 --step 500 --length 5000
  285  ls
  286  cd llama.cpp
  287  ls
  288  cd /etc/slurm/
  289  ls
  290  cat slurm.conf 
  291  export HWLOC_COMPONENTS="-gl"
  292  cd 
  293  cd llama.cpp/
  294  mpirun hostname
  295  mpirun -np 3 hostname
  296  mpirun -np 2 hostname
  297  sinfo
  298  srun --nodelist=AID-E-1 bash
  299  sudo apt install -y build-essential python-dev python-setuptools python-pip python-smbus libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl libffi-dev
  300  sudo apt install -y build-essential python3-dev python3-setuptools python3-pip python3-smbus libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl libffi-dev
  301  squeue
  302  ls
  303  cd llama.cpp/
  304  ls models/
  305  time ./main -m ./models/TinyLLama-v0.ggmlv3.q8_0.bin -p "I believe the meaning of life is" -n 32 -t 2
  306  mpirun  ./main -m ./models/TinyLLama-v0.ggmlv3.q8_0.bin -p "I believe the meaning of life is"  -t 2
  307  mpirun  ./main -m ./models/TinyLLama-v0.ggmlv3.q8_0.bin -p "I believe the meaning of life is"  -t 2 -n 2
  308  miprun hostname
  309  mpirun hostname
  310  cd ..
  311  cd whisper.cpp/
  312  ls
  313  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -p "Georgi" -t 2
  314  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -p "Georgi" 
  315  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin
  316  ./talk  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin
  317  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin
  318  ./stream -m ./models/ggml-base.en.bin -t 8 --step 500 --length 5000
  319  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -p "Georgi" -t 8
  320  cd ex
  321  ls
  322  cd examples/
  323  ls
  324  cd talk-llama/
  325  ls
  326  nano llama.cpp
  327  cd ../..
  328  make talk-llama
  329  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -p "Georgi" -t 8
  330  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -p "Georgi" -t 8 --session AID-E
  331  ./talk-llama
  332  ./talk-llama --help
  333  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -p "AIDE" -t 2 --session AID-E --speed-up true --translate true
  334  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -p "AIDE" -t 2 --session AID-E --speed-up true --translate y
  335  ./talk-llama  -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -p "AIDE" -t 2 --session AID-E 
  336  git clone https://github.com/yacineMTB/talk.git
  337  cd talk
  338  ls
  339  cat build.sh 
  340  ls
  341  cd ..
  342  ls
  343  cd models
  344  ls
  345  cd llama.cpp
  346  cd ..
  347  ls llama.cpp/models/
  348  cp -r llama.cpp/models/ models/
  349  ls
  350  ls
  351  cd talk
  352  ls
  353  ./build.sh
  354  cat build.sh 
  355  nano build.sh 
  356  ./build.sh
  357  ls
  358  ls -A
  359  cd llama.cpp/
  360  ls
  361  cd ..
  362  cd .git/
  363  ls
  364  nano config 
  365  cd ..
  366  ./build.sh
  367  npm install
  368  cd ..
  369  wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
  370  ls
  371  gunzip piper_amd64.tar.gz 
  372  ls
  373  tar -xvf piper_amd64.tar 
  374  ls
  375  cd piper
  376  ls
  377  piper
  378  ./piper
  379  sudo apt-get install piper
  380  piper --help
  381  cd ..
  382  piper -v
  383  wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/l2arctic/medium/en_US-l2arctic-medium.onnx
  384  wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/l2arctic/medium/en_US-l2arctic-medium.onnx.json
  385  echo 'hello world' | \ piper --model en_US-l2arctic-medium.onnx
  386  piper
  387  sudo apt uninstall piper
  388  sudo apt remove piper
  389  pip
  390  pip install piper-tts
  391  echo 'Welcome to the world of speech synthesis!' | piper   --model en_US-l2arctic-medium.onnx   --output_file welcome.wav
  392  piper
  393  pip install piper-tts
  394  piper-tts
  395  piper
  396  python pyper
  397  python piper
  398  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - &&sudo apt-get install -y nodejs
  399  cd talk
  400  ls
  401  ./build.sh 
  402  sudo apt install cmake
  403  ./build.sh 
  404  nano config.json
  405  npm run start
  406  sudo shutdown now
  407  piper
  408  echo 'Welcome to the world of speech synthesis!' | piper   --model en_US-lessac-medium   --output_file welcome.wav
  426  ./llama.cpp/build_server/bin/server -m models/llama/TinyLLama-v0.ggmlv3.q8_0.bin -c 2048
  427  top
  428  cd whisper.cpp/
  429  ./stream -m ./models/ggml-base.en.bin -t 8 --step 500 --length 5000
  430  make command
  431  ./command -m ./models/ggml-base.en.bin -t 8 -ac 768
  432  ./stream -m ./models/ggml-base.en.bin -t 8 --step 50 --length 500
  433  make talk
  434  ./talk -m ./models/ggml-base.en.bin -t 8 --step 50 --length 500
  435  ./stream -m ./models/ggml-base.en.bin -t 2 --step 50 --length 500
  436  ./stream
  437  ./stream -m ./models/ggml-base.en.bin -t 2 --step 50 --length 5000
  439  make talk-llama
  440  ./talk-llama
  441  ./talk-llama -m ./models/ggml-base.en.bin -t 2 --step 50 --length 5000
  442  ./talk-llama -mw ./models/ggml-base.en.bin -ml ../llama.cpp/ggml-model-q4_0.bin -t 2 -ac 768
  443  ./talk-llama -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -t 2 -ac 768
  445  ./talk-llama -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -t 2 -ac 768 --file AIDE --speak "AIDE"
  447  ./talk-llama -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -t 2 -ac 768 --file AIDE --name "AIDE"
  448  ./talk-llama -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -t 2 -ac 768 --file AIDE -p "AIDE"
  450  ./talk-llama -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -t 2  --file AIDE -p "AIDE"

whoami
cd whisper.cpp/
./talk-llama -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -t 2  --file AIDE -p "AIDE"
./talk-llama -mw ./models/ggml-base.en.bin -ml ../llama.cpp/models/TinyLLama-v0.ggmlv3.q8_0.bin -t 2  --file AIDE -p "AIDE"
./stream -m ./models/ggml-base.en.bin -t 2 --step 50 --length 5000
./stream -m ./models/ggml-base.en.bin -t 2 --step 5000 --length 50000
cd whisper.cpp/
./stream -m ./models/ggml-base.en.bin -t 2 --step 5000 --length 50000


    1  sftp user@AID-E-1
    2  chmod 777 script.sh
    3  ls
    4  ./script.sh 
    5  cd /etc/initramfs/post-update.d/
    6  ls
    7  sudo rm z50-raspi-firmware 
    8  ls
    9  cd ..
   10  ls
   11  cd ..
   12  ls
   13  lscd ~
   14  cd ~
   15  ls
   16  nano script.sh 
   17  ./script.sh 
   18  ls
   19  cat scrip
   20  cat script.sh 
   21  rm script.sh 
   22  sftp user@AID-E-1
   23  ls
   24  sftp user@AID-E-1
   25  ./script.sh
   26  nano script.sh 
   27  ls
   28  rm script.sh 
   29  cat munge.key 
   30  ls
   31  sftp user@AID-E-1
   32  cat script.sh 
   33  ./script.sh 
   34  sinfo -N
   35  ls
   36  cat cgroup.conf
   37  ls
   38  cat slurm.conf
   39  sinfo
   40  cd llama.cpp/
   41  ls
   42  cd models/
   43  ls
   44  sudo mount -a
   45  ls
   46  cd ..
   47  sudo mount -a
   48  ls models/
   49  ls
   50  git fetch
   51  cd ..
   52  ls
   53  cat script.sh 
   54  ./script.sh 
   55  ls
   56  ls llama.cpp/models/
   57  sudo apt install nfs-common -y
   58  cat /etc/fstab
   59  nano script.
   60  nano script.sh 
   61  sudo echo "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0"  >> /etc/fstab
   62  sudo echo "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0" sudo  >> /etc/fstab
   63  sudo -w echo "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0"  >> /etc/fstab
   64  cat /etc/fstab
   65  blkid
   66  sudo blkid
   67  cat /etc/fstab
   68  sudo blkid | sudo tee /etc/fstab
   69  cat /etc/fstab
   70  echo "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0"  | tee -a /etc/fstab
   71  echo "AID-E-1:/home/user/llama.cpp/models /home/user/llama.cpp/models nfs defaults 0 0"  |sudo tee -a /etc/fstab
   72  cat /etc/fstab
   73  sudo nano /etc/fstab
   74  cat /etc/fstab
   75  sudo reboot now
   76  ls
   77  ls llama.cpp/models/
   78  sudo apt install
   79  sudo cat /etc/fstab
   80  sudo apt install nfs-common -y
   81  sudo mount -a
   82  ls
   83  srun hostname
   84  ls
   85  cat script
   86  cat script.sh 
   87  sudo apt install
   88  sudo reboot now
   89  cd llama
   90  ls llama.cpp/models/
   91  mpirun -np 4 benchmark-matmult
   92  mpirun -np 3 benchmark-matmult
   93  mpirun -np 2 benchmark-matmult
   94  cd llama.cpp/
   95  git pull
   96  git status
   97  make CC=mpicc CXX=mpicxx LLAMA_MPI=1
   98  time ./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin -p "I believe the meaning of life is" -n 32 -t 2
   99  cd /home/user/
  100  sudo apt-get install libsdl2-dev -y
  101  git clone https://github.com/ggerganov/whisper.cpp.git
  102  cd whisper.cpp/
  103  bash ./models/download-ggml-model.sh base.en
  104  make main stream command talk talk-llama
  105  curl -fsSL https://get.docker.com -o get-docker.sh
  106  sudo sh ./get-docker.sh --dry-run
  107  docker --version
  108  sudo sh ./get-docker.sh
  109  sudo shutdown now
  110  ls
  111  cat get-docker.sh 
  112  ls
  113  cat cgroup_allowed_devices_file.conf 
  114  cat cgroup.conf 
  115  ls
  116  cd templates/
  117  ls
  118  cat script.sh 
  119  cd ..
  120  ls
  121  cd downloads/
  122  ls
  123  cd ..
  124  ls
  125  cd /
  126  ls
  127  cd etc
  128  cd munge/
  129  ls
  130  cd munge/
  131  cat munge/
  132  sudo cd munge
  133  ls munge/
  134  sudo ls munge/
  135  sudo cat munge/munge.key
  136  cd ~
  137  ls
  138  scp ./munge.key loki@pop-os:~/
  139  ls
  140  cd llama.cpp/
  141  ls
  142  cd ..
  143  ls
  144  cd  llama.cpp/
  145  sudo ls
  146  sudo ls /models
  147  sudo ls /model
  148  sudo ls /models
  149  sudo ls -A /models
  150  sudo ls -A 
  151  sudo ls -lA 
  152  exit
  153  ls
  154  cd /etc/
  155  ls
  156  cd munge/
  157  sudo sh 
  158  ls
  159  cd ~
  160  ls
  161  cat slurm.conf
