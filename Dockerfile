FROM docker.paddlepaddlehub.com/paddle
MAINTAINER Supejomn Authors <yanchunwei@outlook.com>

# install CE
RUN sed -i 's#http://archive.ubuntu.com/ubuntu#http://mirrors.tuna.tsinghua.edu.cn/ubuntu/#g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y python3 python3-pip

RUN git clone https://github.com/PaddlePaddle/continuous_evaluation.git
RUN cd continuous_evaluation && bash ./build_docker.sh
