I2S Audio Media Player
======================

.. seo::
    :description: Instructions for setting up I²S based media players in ESPHome.
    :image: i2s_audio.svg

The ``i2s_audio`` media player platform allows you to play media from webservers and web streams
via the :doc:`/components/i2s_audio`. This platform only works on ESP32 based chips.

.. code-block:: yaml

    # Example configuration entry
    media_player:
      - platform: i2s_audio
        name: ESPHome I2S Media Player
        dac_type: external
        i2s_dout_pin: GPIO22
        i2s_comm_fmt: false
        mode: mono

Configuration variables:
------------------------

- **dac_type** (**Required**, enum):

  - ``external``: Use an external DAC, for example the NS4168, or UDA1334A.
  - ``internal``: Use the internal DAC

- All other options from :ref:`Media Player <config-media_player>`

External DAC
************

- **i2s_dout_pin** (**Required**, :ref:`config-pin`): The GPIO pin to use for the I²S ``DOUT/SDOUT`` *(Data Out)* signal, also referred to as ``SD/SDATA`` *(Serial Data)* or ``DACDAT`` *(Digital to Analog Converter Data)*.
- **mute_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use to mute the media player.
- **mode** (*Optional*, string): The mode of the I²S bus. Can be ``mono`` or ``stereo``. Defaults to ``mono``.
- **i2s_audio_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`I²S Audio <i2s_audio>` you wish to use for this media player.
- **i2s_comm_fmt** (*Optional*, boolean): I2S communication format. By default I2S_COMM_FORMAT_I2S_MSB (AC101, PCM5102A). Set to true if using an external DAC that uses Japanese (Least Significant Bit Justified) format (like PT8211) . Defaults to ``false``.

For best results, keep the wires as short as possible.

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
