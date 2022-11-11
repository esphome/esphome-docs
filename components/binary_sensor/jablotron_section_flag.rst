Jablotron Section Flag
======================

.. seo::
    :description: Instructions for setting up a jablotron_section_flag binary sensor.

The `jablotron_section_flag` binary sensor platform creates a sensor that detects a specific
flag on a Jablotron section. The binary sensor requires
:doc:`Jablotron Component </components/jablotron>` to be configured.

Configuration variables:
------------------------
- **name** (*Required*, string): The name of the sensor.
- **index** (*Required*, int): Index of the section in the Jablotron control panel.
- **flag** (*Required*, enum): The flag this sensor should report.
    - ``INTERNAL_WARNING`` - internal siren active
    - ``EXTERNAL_WARNING`` - external siren active
    - ``FIRE_ALARM`` - fire alarm
    - ``INTRUDER_ALARM`` - intruder alarm
    - ``PANIC_ALARM`` - panic alarm
    - ``ENTRY`` - entry delay
    - ``EXIT`` - exit delay
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **jablotron_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :doc:`Jablotron Component </components/jablotron>` to be used.

All other options from :ref:`Binary Sensor component <config-binary_sensor>`.

Example

.. code-block:: yaml

    uart:
      # ...
    jablotron:
      # ...
    binary_sensor:
      - platform: jablotron_section_flag
        index: 1
        flag: ENTRY
        name: Main entry delay



See Also
--------
- :apiclass:`:jablotron_section_flag::SectionFlagSensor`
- :doc:`/components/jablotron`
- :doc:`/components/select/jablotron_section`
- :doc:`/components/text_sensor/jablotron_section`
- :doc:`/components/uart`
- `JA-121 RS-485 Interface <https://jablotron.com.hk/image/data/pdf/manuel/JA-121T.pdf>`__
- :ghedit:`Edit`
