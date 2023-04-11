I2S Audio Component
===================

.. seo::
    :description: Instructions for setting up I2S based devices in ESPHome.
    :image: i2s_audio.svg

The ``i2s_audio`` component allows for sending and receiving audio via I2S.
This component only works on ESP32 based chips.

.. code-block:: yaml

    # Example configuration entry
    i2s_audio:
      i2s_lrclk_pin: GPIO33
      i2s_bclk_pin: GPIO19

Configuration variables:
------------------------

- **i2s_lrclk_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I2S LRCLK (Word Select or Left/Right Clock) signal.
- **i2s_bclk_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I2S BCLK (Bit Clock) signal.

See also
--------

- :doc:`microphone/index`
- :doc:`media_player/index`
- :ghedit:`Edit`
