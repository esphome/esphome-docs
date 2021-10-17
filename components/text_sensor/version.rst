Version Text Sensor
===================

.. seo::
    :description: Instructions for setting up version text sensors.
    :image: new-box.png

The ``version`` text sensor platform exposes the ESPHome version the firmware
was compiled against as a text sensor.

.. figure:: images/version-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: version
        name: "ESPHome Version"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the text sensor.
- **hide_timestamp** (*Optional*, boolean): Allows you to hide the compilation timestamp from the version string. Defaults to ``False``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Text Sensor <config-text_sensor>`.

Disabling the compilation timestamp:
------------------------------------

.. code-block:: yaml    

    # Example configuration entry
    text_sensor:
      - platform: version
        name: "ESPHome Version"
        hide_timestamp: True

This will, for example, change the output of the senser from:

``1.15.0-dev (Jun 8 2020, 18:53:16)`` to ``1.15.0-dev``


See Also
--------

- :apiref:`version/version_text_sensor.h`
- :ghedit:`Edit`
