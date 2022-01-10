ESP32 Camera Component
======================

.. seo::
    :description: Instructions for setting up the ESP32 Cameras in ESPHome
    :image: camera.svg

The ``esp32_camera`` component allows you to use ESP32-based camera boards in ESPHome that
directly integrate into Home Assistant through the native API.

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      name: My Camera
      external_clock:
        pin: GPIO27
        frequency: 20MHz
      i2c_pins:
        sda: GPIO25
        scl: GPIO23
      data_pins: [GPIO17, GPIO35, GPIO34, GPIO5, GPIO39, GPIO18, GPIO36, GPIO19]
      vsync_pin: GPIO22
      href_pin: GPIO26
      pixel_clock_pin: GPIO21
      reset_pin: GPIO15
      resolution: 640x480
      jpeg_quality: 10

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the camera.
- **icon** (*Optional*, icon): Manually set the icon to use for the camera in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Requires Home Assistant 2021.9 or newer. Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options. Requires Home Assistant 2021.11 or newer.
  Set to ``""`` to remove the default entity category.

Connection Options:

- **data_pins** (**Required**, list of pins): The data lanes of the camera, this must be a list
  of 8 GPIO pins.
- **vsync_pin** (**Required**, pin): The pin the VSYNC line of the camera is connected to.
- **href_pin** (**Required**, pin): The pin the HREF line of the camera is connected to.
- **pixel_clock_pin** (**Required**, pin): The pin the pixel clock line of the camera is connected to.
- **external_clock** (**Required**): The configuration of the external clock to drive the camera.

  - **pin** (**Required**, pin): The pin the external clock line is connected to.
  - **frequency** (*Optional*, float): The frequency of the external clock, must be either 20MHz
    or 10MHz. Defaults to ``20MHz``.

- **i2c_pins** (**Required**): The I²C control pins of the camera.

  - **sda** (**Required**, pin): The SDA pin of the I²C interface. Also called ``SIOD``.
  - **scl** (**Required**, pin): The SCL pin of the I²C interface. Also called ``SIOC``.

- **reset_pin** (*Optional*, pin): The ESP pin the reset pin of the camera is connected to.
  If set, this will reset the camera before the ESP boots.
- **power_down_pin** (*Optional*, pin): The ESP pin to power down the camera.
  If set, this will power down the camera while it is inactive.
- **test_pattern** (*Optional*, boolean): When enabled, the camera will show a test pattern
  that can be used to debug connection issues.

Frame Settings:

- **max_framerate** (*Optional*, float): The maximum framerate the camera will generate images at.
  Up to 60Hz is possible (with reduced frame sizes), but beware of overheating. Defaults to ``10 fps``.
- **idle_framerate** (*Optional*, float): The framerate to capture images at when no client
  is requesting a full stream. Defaults to ``0.1 fps``.
- **resolution** (*Optional*, enum): The resolution the camera will capture images at. Higher
  resolutions require more memory, if there's not enough memory you will see an error during startup.

    - ``160x120`` (QQVGA)
    - ``176x144`` (QCIF)
    - ``240x176`` (HQVGA)
    - ``320x240`` (QVGA)
    - ``400x296`` (CIF)
    - ``640x480`` (VGA, default)
    - ``800x600`` (SVGA)
    - ``1024x768`` (XGA)
    - ``1280x1024`` (SXGA)
    - ``1600x1200`` (UXGA)

- **jpeg_quality** (*Optional*, int): The JPEG quality that the camera should encode images with.
  From 10 (best) to 63 (worst). Defaults to ``10``.

- **contrast** (*Optional*, int): The contrast to apply to the picture, from -2 to 2. Defaults to ``0``.
- **brightness** (*Optional*, int): The brightness to apply to the picture, from -2 to 2. Defaults to ``0``.
- **saturation** (*Optional*, int): The saturation to apply to the picture, from -2 to 2. Defaults to ``0``.
- **vertical_flip** (*Optional*, boolean): Whether to flip the image vertically. Defaults to ``true``.
- **horizontal_mirror** (*Optional*, boolean): Whether to mirror the image horizontally. Defaults to ``true``.

.. note::

    Camera uses PWM timer #1. If you need PWM (via the ``ledc`` platform) you need to manually specify
    a channel there (with the ``channel: 2``  parameter)

Configuration for Ai-Thinker Camera
-----------------------------------

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO0
        frequency: 20MHz
      i2c_pins:
        sda: GPIO26
        scl: GPIO27
      data_pins: [GPIO5, GPIO18, GPIO19, GPIO21, GPIO36, GPIO39, GPIO34, GPIO35]
      vsync_pin: GPIO25
      href_pin: GPIO23
      pixel_clock_pin: GPIO22
      power_down_pin: GPIO32

      # Image settings
      name: My Camera
      # ...

Configuration for M5Stack Camera
--------------------------------

.. warning::

    This camera board has insufficient cooling and will overheat over time,
    ESPHome does only activate the camera when Home Assistant requests an image, but
    the camera unit can still heat up considerably for some boards.

    If the camera is not recognized after a reboot and the unit feels warm, try waiting for
    it to cool down and check again - if that still doesn't work try enabling the test pattern.

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO27
        frequency: 20MHz
      i2c_pins:
        sda: GPIO25
        scl: GPIO23
      data_pins: [GPIO17, GPIO35, GPIO34, GPIO5, GPIO39, GPIO18, GPIO36, GPIO19]
      vsync_pin: GPIO22
      href_pin: GPIO26
      pixel_clock_pin: GPIO21
      reset_pin: GPIO15

      # Image settings
      name: My Camera
      # ...

Configuration for M5Stack Timer Camera X/F
------------------------------------------

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO27
        frequency: 20MHz
      i2c_pins:
        sda: GPIO25
        scl: GPIO23
      data_pins: [GPIO32, GPIO35, GPIO34, GPIO5, GPIO39, GPIO18, GPIO36, GPIO19]
      vsync_pin: GPIO22
      href_pin: GPIO26
      pixel_clock_pin: GPIO21
      reset_pin: GPIO15

      # Image settings
      name: My Camera
      # ...

Configuration for Wrover Kit Boards
-----------------------------------

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO21
        frequency: 20MHz
      i2c_pins:
        sda: GPIO26
        scl: GPIO27
      data_pins: [GPIO4, GPIO5, GPIO18, GPIO19, GPIO36, GPIO39, GPIO34, GPIO35]
      vsync_pin: GPIO25
      href_pin: GPIO23
      pixel_clock_pin: GPIO22

      # Image settings
      name: My Camera
      # ...

Configuration for TTGO T-Camera V05
-----------------------------------

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO32
        frequency: 20MHz
      i2c_pins:
        sda: GPIO13
        scl: GPIO12
      data_pins: [GPIO5, GPIO14, GPIO4, GPIO15, GPIO18, GPIO23, GPIO36, GPIO39]
      vsync_pin: GPIO27
      href_pin: GPIO25
      pixel_clock_pin: GPIO19
      power_down_pin: GPIO26

      # Image settings
      name: My Camera
      # ...

Configuration for TTGO T-Camera V162
------------------------------------

.. code-block:: yaml

    esp32_camera:
      external_clock:
        pin: GPIO4
        frequency: 20MHz
      i2c_pins:
        sda: GPIO18
        scl: GPIO23
      data_pins: [GPIO34, GPIO13, GPIO14, GPIO35, GPIO39, GPIO38, GPIO37, GPIO36]
      vsync_pin: GPIO5
      href_pin: GPIO27
      pixel_clock_pin: GPIO25
      jpeg_quality: 10
      vertical_flip: true
      horizontal_mirror: false

      # Image settings
      name: My Camera
      # ...

Configuration for TTGO T-Camera V17
-----------------------------------

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO32
        frequency: 20MHz
      i2c_pins:
        sda: GPIO13
        scl: GPIO12
      data_pins: [GPIO5, GPIO14, GPIO4, GPIO15, GPIO18, GPIO23, GPIO36, GPIO39]
      vsync_pin: GPIO27
      href_pin: GPIO25
      pixel_clock_pin: GPIO19
      # power_down_pin: GPIO26
      vertical_flip: true
      horizontal_mirror: true

      # Image settings
      name: My Camera
      # ...

Configuration for TTGO T-Journal
--------------------------------

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO27
        frequency: 20MHz
      i2c_pins:
        sda: GPIO25
        scl: GPIO23
      data_pins: [GPIO17, GPIO35, GPIO34, GPIO5, GPIO39, GPIO18, GPIO36, GPIO19]
      vsync_pin: GPIO22
      href_pin: GPIO26
      pixel_clock_pin: GPIO21

      # Image settings
      name: My Camera
      # ...


Configuration for TTGO-Camera Plus
----------------------------------

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO4
        frequency: 20MHz
      i2c_pins:
        sda: GPIO18
        scl: GPIO23
      data_pins: [GPIO34, GPIO13, GPIO26, GPIO35, GPIO39, GPIO38, GPIO37, GPIO36]
      vsync_pin: GPIO5
      href_pin: GPIO27
      pixel_clock_pin: GPIO25
      vertical_flip: false
      horizontal_mirror: false

      # Image settings
      name: My Camera
      # ...

Configuration for TTGO-Camera Mini
----------------------------------

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO32
        frequency: 20MHz
      i2c_pins:
        sda: GPIO13
        scl: GPIO12
      data_pins: [GPIO5, GPIO14, GPIO4, GPIO15, GPIO37, GPIO38, GPIO36, GPIO39]
      vsync_pin: GPIO27
      href_pin: GPIO25
      pixel_clock_pin: GPIO19

      # Image settings
      name: My Camera
      # ...

Configuration for ESP-EYE
----------------------------------

.. code-block:: yaml

    # Example configuration entry
    esp32_camera:
      external_clock:
        pin: GPIO4
        frequency: 20MHz
      i2c_pins:
        sda: GPIO18
        scl: GPIO23
      data_pins: [GPIO34, GPIO13, GPIO14, GPIO35, GPIO39, GPIO38, GPIO37, GPIO36]
      vsync_pin: GPIO5
      href_pin: GPIO27
      pixel_clock_pin: GPIO25

      # Image settings
      name: My Camera
      # ...


See Also
--------

- :apiref:`esp32_camera/esp32_camera.h`
- :ghedit:`Edit`
