# syntax=docker/dockerfile:1

FROM ghcr.io/ggerganov/llama.cpp:full

RUN apt-get install -y mpich curl

RUN curl -O /app/models/ggml-vocab.bin https://github.com/ggerganov/llama.cpp/tree/f514d1b306e1114c2884fcb25dd9bd48ae64ba32/models/ggml-vocab.bin

COPY hostfile /app

RUN make CC=mpicc CXX=mpicxx LLAMA_MPI=1

ENTRYPOINT ["tail", "-f", "/dev/null"]

#ENTRYPOINT ["mpirun", "-hostfile", "hostfile", "-n", "2", "./main", "-m", "./models/ggml-vocal.bin", "-n", "128" ] 