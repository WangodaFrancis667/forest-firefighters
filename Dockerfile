FROM ubuntu:20.04

ARG USER_ID=1000
ARG GROUP_ID=1000
ARG USERNAME=webotsuser

ENV DEBIAN_FRONTEND=noninteractive
ENV WEBOTS_HOME=/usr/local/webots
ENV PATH="${WEBOTS_HOME}:${PATH}"
ENV QT_X11_NO_MITSHM=1
ENV XDG_RUNTIME_DIR=/tmp/runtime-webots
ENV ALSOFT_DRIVERS=null
ENV QTWEBENGINE_DISABLE_SANDBOX=1
ENV QTWEBENGINE_CHROMIUM_FLAGS=--no-sandbox

RUN apt update && apt install -y \
    wget \
    git \
    ca-certificates \
    nano \
    python3 \
    python3-pip \
    python3-numpy \
    python3-opencv \
    mesa-utils \
    libglvnd0 \
    libgl1 \
    libegl1 \
    libgles2 \
    libglu1-mesa \
    libxrender1 \
    libxi6 \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb1 \
    libx11-xcb1 \
    libfontconfig1 \
    libfreetype6 \
    libnss3 \
    libasound2 \
    libopenal1 \
    libpulse0 \
    libdbus-1-3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxtst6 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O /tmp/webots_2021b_amd64.deb \
    https://github.com/cyberbotics/webots/releases/download/R2021b/webots_2021b_amd64.deb \
    && apt update \
    && apt install -y /tmp/webots_2021b_amd64.deb \
    && rm /tmp/webots_2021b_amd64.deb

RUN groupadd -g ${GROUP_ID} ${USERNAME} \
    && useradd -m -u ${USER_ID} -g ${GROUP_ID} -s /bin/bash ${USERNAME} \
    && mkdir -p /workspace /tmp/runtime-webots \
    && chown -R ${USERNAME}:${USERNAME} /workspace /tmp/runtime-webots \
    && chmod 700 /tmp/runtime-webots

USER ${USERNAME}
WORKDIR /workspace

CMD ["/bin/bash"]
