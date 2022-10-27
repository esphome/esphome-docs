Jablotron Section
====================

.. seo::
    :description: Instructions for setting up a jablotron_section text sensor.

The `jablotron_section` text sensor platform creates a sensor for a section
configured in the Jablotron control panel. The text sensor requires
:doc:`Jablotron Component </components/jablotron>` to be configured.

The sensor reports these section states from the JA-121T protocol:

- ``READY``: Normal mode
- ``ARMED_PART``: Partially set
- ``ARMED``: Set
- ``SERVICE``: Service mode
- ``BLOCKED``: Blocked after an alarm
- ``OFF``: Section disabled

To expose section flags, create appropriate :doc:`jablotron_section_flag` sensors for
the section.

Configuration variables:
------------------------
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (*Required*, string): The name of the sensor.
- **index** (*Required*, int): Index of the section in the Jablotron control panel.

All other options from :ref:`Text Sensor component <config-text_sensor>`.

Example

.. code-block:: yaml

    uart:
      # ...
    jablotron:
      # ...
    text_sensor:
      - platform: jablotron_section
        index: 1
        name: Main


See Also
--------
- :apiclass:`:jablotron_section::SectionSensor`
- :doc:`/components/jablotron`
- :doc:`/components/jablotron_section_flag`
- :doc:`/components/uart`
- `JA-121 RS-485 Interface <https://jablotron.com.hk/image/data/pdf/manuel/JA-121T.pdf>`__
- :ghedit:`Edit`