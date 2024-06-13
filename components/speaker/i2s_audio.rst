I²S Audio Speaker
=================

.. seo::
    :description: Instructions for setting up I²S based speakers in ESPHome.
    :image: i2s_audio.svg

The ``i2s_audio`` speaker platform allows you to receive audio via the the :doc:`/components/i2s_audio`.

This platform only works on ESP32 based chips.

.. warning::

    Audio and voice components consume a significant amount of resources (RAM, CPU) on the device.

    **Crashes are likely to occur** if you include too many additional components in your device's
    configuration. In particular, Bluetooth/BLE components are known to cause issues when used in
    combination with Voice Assistant and/or other audio components.

.. code-block:: yaml

    # Example configuration entry
    speaker:
      - platform: i2s_audio
        dac_type: external
        i2s_dout_pin: GPIOXX
        mode: mono

Configuration variables:
------------------------

- **dac_type** (**Required**, enum):

  - ``external``: Use an external DAC, for example the NS4168, or UDA1334A.
  - ``internal``: Use the internal DAC

External DAC
************

- **i2s_dout_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I²S DOUT (Data Out) signal.
- **mode** (*Optional*, string): The mode of the I²S bus. Can be ``mono`` or ``stereo``. Defaults to ``mono``.
- **i2s_audio_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`I²S Audio <i2s_audio>` you wish to use for this speaker.

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
