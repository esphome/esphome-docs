ESP-ADF
=======

.. seo::
    :description: Instructions for including ESP-ADF in ESPHome.
    :image: esp-adf.svg

`ESP-ADF <https://github.com/espressif/esp-adf>`__ is Espressif's Audio Development Framework.

ESPHome can leverage this framework to provide a number of features:

- VAD (Voice Activity Detection) for the :doc:`voice_assistant`
- :doc:`Microphone </components/microphone/esp_adf>` for certain boards.
- :doc:`Speaker </components/speaker/esp_adf>` for certain boards.


.. code-block:: yaml

    esp_adf:

Configuration variables:
------------------------

- **board** (Optional, string): Manually specify the esp-adf board to use.
  Defaults to the ``board`` from the :doc:`/components/esp32`.

.. _esp_adf-boards:

  For the ``microphone`` and ``speaker``, the following boards are supported:

    - ``esp32s3box`` - ESP32 S3 Box
    - ``esp32s3boxlite`` - ESP32 S3 Box Lite


See Also
--------

- :doc:`/components/esp32`
- :doc:`/components/microphone/esp_adf`
- :doc:`/components/speaker/esp_adf`
- :doc:`/components/voice_assistant`
- :ghedit:`Edit`
