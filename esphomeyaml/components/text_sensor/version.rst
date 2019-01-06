Version Text Sensor
===================

.. seo::
    :description: Instructions for setting up version text sensors.
    :image: new-box.png

The ``version`` text sensor platform exposes the esphomelib version the firmware
was compiled against as a text sensor.

.. figure:: images/version-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: version
        name: "Esphomelib Version"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the text sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Text Sensor <config-text_sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :doc:`API Reference </api/text_sensor/version>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/text_sensor/version.rst>`__

.. disqus::
