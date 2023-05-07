I²S Audio Microphone
====================

.. seo::
    :description: Instructions for setting up I²S based microphones in ESPHome.
    :image: i2s_audio.svg

The ``i2s_audio`` microphone platform allows you to receive audio via the the
:doc:`/components/i2s_audio`. This platform only works on ESP32 based chips.

.. code-block:: yaml

    # Example configuration entry
    microphone:
      - platform: i2s_audio
        id: external_mic
        adc_type: external
        i2s_din_pin: GPIO23

      - platform: i2s_audio
        id: adc_mic
        adc_type: internal
        adc_pin: GPIO35


Configuration variables:
------------------------

- **adc_type** (**Required**, enum):

  - ``external``: Use an external ADC connected to the I²S bus.
  - ``internal``: Use the internal ADC of the ESP32.

- All other options from :ref:`Microphone <config-microphone>`

External ADC
------------

- **i2s_din_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the I²S DIN (Data In) signal.
- **pdm** (**Required**, boolean): Set this to ``true`` if your external ADC uses PDM (Pulse Density Modulation) instead of I²S.

Internal ADC
------------

- **adc_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The GPIO pin to use for the ADC input.


Known Devices
-------------

M5Stack Atom Echo
*****************

.. code-block:: yaml

    microphone:
      - platform: i2s_audio
        adc_type: external:
        i2s_din_pin: GPIO23

RaspiAudio Muse Luxe
********************

.. code-block:: yaml

    microphone:
      - platform: i2s_audio
        i2s_din_pin: GPIO35
        adc_type: external
        pdm: false


See also
--------

- :doc:`index`
- :ghedit:`Edit`
