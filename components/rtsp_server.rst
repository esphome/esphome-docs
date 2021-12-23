RTSP Server Component
======================

.. seo::
    :description: Instructions for setting up an RTSP Server with the ESP32 Camera in ESPHome
    :image: camera.png

The ``rtsp_server`` component allows you to stream video from ESP32-based camera boards in ESPHome to
any RTSP-compatible application (VLC Media Player; GStreamer; etc).

Currently, only UDP transport is supported; therefore, ensure that you have the appropriate firewall / routing 
configurations to support UDP transport.  Many application permit explicit definition of the UDP port ranges
to use.

Sample FFMPEG RTSP capture, using a defined UDP port range:
`ffmpeg -loglevel debug -rtsp_transport udp -min_port 12160 -max_port 12165 -i rtsp://camera.local:8675 -vcodec copy out.mkv`

An :ref:`esp32_camera <esp32_camera>` configuration item is required to use this component.

.. code-block:: yaml
    rtsp_server:
      port: 8675
      camera: cam1

Configuration variables:
------------------------

- **port** (**Required**, number): The port number on which to listen
- **camera** (**Required**, :ref:`config-id`) The camera from which to stream video
