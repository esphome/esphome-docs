I2S Audio Media Player
======================

.. seo::
    :description: Instructions for setting up I2S based media players in ESPHome.
    :image: i2s_audio.svg

The ``i2s_audio`` media player platform allows you to play media from webservers and web streams
via the I2S bus. This platform only works on ESP32 based chips.

.. code-block:: yaml

    # Example configuration entry
    media_player:
      - platform: i2s_audio
        name: ESPHome I2S Media Player
        dac_type: external
        i2s_lrclk_pin: GPIO33
        i2s_dout_pin: GPIO22
        i2s_bclk_pin: GPIO19
        mode: mono

Configuration variables:
------------------------

- **dac_type** (**Required**, enum)

  - ``external``: Use an external DAC, for example the NS4168, or UDA1334A.
  - ``internal``: Use the internal DAC

- All other options from :ref:`Media Player <config-media_player>`

External DAC
************

- **i2s_lrclk_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I2S LRCLK (Word Select or Left/Right Clock) signal.
- **i2s_dout_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I2S DOUT (Data Out) signal.
- **i2s_bclk_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I2S BCLK signal (Bit Clock).
- **mode** (*Optional*, string): The mode of the I2S bus. Can be ``mono`` or ``stereo``. Defaults to ``mono``.

Internal DAC
************

- **mode** (**Required**, enum): The channel mode of the internal DAC.

  - ``left``
  - ``right``
  - ``stereo``

See also
--------

- :doc:`index`
- :ghedit:`Edit`
