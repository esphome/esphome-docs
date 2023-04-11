I²S Audio Component
===================

.. seo::
    :description: Instructions for setting up I²S based devices in ESPHome.
    :image: i2s_audio.svg

The ``i2s_audio`` component allows for sending and receiving audio via I²S.
This component only works on ESP32 based chips.

.. code-block:: yaml

    # Example configuration entry
    i2s_audio:
      i2s_lrclk_pin: GPIO33
      i2s_bclk_pin: GPIO19

Configuration variables:
------------------------

- **i2s_lrclk_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I²S LRCLK (Word Select or Left/Right Clock) signal.
- **i2s_bclk_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I²S BCLK (Bit Clock) signal.

See also
--------

- :doc:`microphone/i2s_audio`
- :doc:`media_player/i2s_audio`
- :ghedit:`Edit`
