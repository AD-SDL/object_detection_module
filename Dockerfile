FROM ghcr.io/ad-sdl/wei

LABEL org.opencontainers.image.source=https://github.com/AD-SDL/object_detection_module
LABEL org.opencontainers.image.description="A module that allows you to take a picture via webcam and run YOLO object detection through darknet"
LABEL org.opencontainers.image.licenses=MIT

#########################################
# Module specific logic goes below here #
#########################################

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git \
    libopencv-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /root/src

RUN cd /root/src && ls -lrth

RUN mkdir -p /root/src/darknet_install

RUN cd /root/src && ls -lrth

WORKDIR /root/src

# Clone the Darknet repository
# RUN git clone https://github.com/hank-ai/darknet /root/src/darknet
RUN git clone https://github.com/hank-ai/darknet darknet_install/

# Build Darknet
WORKDIR /root/src/darknet_install/darknet

RUN pwd

RUN ls -lrth

RUN mkdir build && cd build

RUN cmake -DCMAKE_BUILD_TYPE=Release ..

RUN make -j4 package

# Install Darknet package
RUN dpkg -i build/darknet-*.deb

WORKDIR /home/app

RUN mkdir -p /home/app/trained

COPY trainingImages /home/app/trained

RUN mkdir -p /home/app/object_detection_module

COPY ./src object_detection_module/src
RUN chmod +x object_detection_module/src/photoAndPosition.sh
COPY ./README.md object_detection_module/README.md
COPY ./pyproject.toml object_detection_module/pyproject.toml

RUN --mount=type=cache,target=/root/.cache \
    pip install -e ./object_detection_module

# CMD ["python", "-m", "object_detection_rest_node"]

# Add user to video group to access camera
RUN usermod -a -G video app

#########################################
