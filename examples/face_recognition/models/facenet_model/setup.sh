apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        libsm6 libxext6 libxrender-dev \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

apt-get install libglib2.0-0

pip install numpy==1.17
pip install opencv-python==4.1.0.25
pip install scikit-learn==0.21.3
pip install tensorflow