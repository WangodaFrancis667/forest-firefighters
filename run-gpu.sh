#!/usr/bin/env bash
set -e

xhost +local:docker >/dev/null

docker rm -f webots_r2021b_gpu 2>/dev/null || true

docker run -it --rm \
  --name webots_r2021b_gpu \
  --network host \
  --ipc=host \
  --shm-size=4g \
  --gpus all \
  --device=/dev/dri:/dev/dri \
  -e DISPLAY="$DISPLAY" \
  -e QT_X11_NO_MITSHM=1 \
  -e XDG_RUNTIME_DIR=/tmp/runtime-webots \
  -e ALSOFT_DRIVERS=null \
  -e QTWEBENGINE_DISABLE_SANDBOX=1 \
  -e QTWEBENGINE_CHROMIUM_FLAGS=--no-sandbox \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e __NV_PRIME_RENDER_OFFLOAD=1 \
  -e __GLX_VENDOR_LIBRARY_NAME=nvidia \
  -e __VK_LAYER_NV_optimus=NVIDIA_only \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$PWD/workspace:/workspace" \
  webots-r2021b-gpu
