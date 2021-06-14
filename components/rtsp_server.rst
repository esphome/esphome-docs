RTSP Server Component
======================

.. seo::
    :description: Instructions for setting up an RTSP Server with the ESP32 Camera in ESPHome
    :image: camera.png

The ``rtsp_server`` component allows you to stream video from ESP32-based camera boards in ESPHome to
any RTSP-compatible application (VLC Media Player; GStreamer; etc).

An ``esp32_camera`` configuration item is required to use this component.

.. code-block:: yaml
    rtsp_server:
      port: 8675
      camera: cam1

Configuration variables:
------------------------

- **port** (**Required**, number): The port number on which to listen
- **camera** (**Required**, :ref:`config-id`) The camera from which to stream video
