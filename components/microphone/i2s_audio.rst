I²S Audio Microphone
====================

.. seo::
    :description: Instructions for setting up I²S based microphones in ESPHome.
    :image: i2s_audio.svg

The ``i2s_audio`` microphone platform allows you to receive audio via the the
:ref:`/components/i2s_audio`. This platform only works on ESP32 based chips.

.. code-block:: yaml

    # Example configuration entry
    microphone:
      - platform: i2s_audio
        i2s_din_pin: GPIO23

Configuration variables:
------------------------

- **i2s_din_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I²S DIN (Data In) signal.

- All other options from :ref:`Microphone <config-microphone>`

See also
--------

- :doc:`index`
- :ghedit:`Edit`
