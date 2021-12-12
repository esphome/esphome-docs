ESP32 Camera Web Server Component
=================================

.. seo::
    :description: Instructions for setting up the ESP32 Camera Web Server in ESPHome
    :image: camera.svg

The ``esp32_camera_web_server`` component allows you to use expose web server of
ESP32-based camera boards in ESPHome that directly can be integrated into external
surveillance or PVR software.

At a given time only one stream can be served, but multiple snapshots. The stream
or snapshot can be accessed via `http://<ip>:<port>/`.

.. code-block:: yaml

    # Example configuration entry
    esp32_camera_web_server:
      - port: 8080
        mode: stream
      - port: 8081
        mode: snapshot

Configuration variables:
------------------------

- **port** (**Required**, string): The serving port.
- **mode** (**Required**, string): The operation mode.
  One of these values:

  - ``snapshot``
  - ``stream``

See Also
--------

- :apiref:`esp32_camera_web_server/esp32_camera_web_server.h`
- :ghedit:`Edit`
