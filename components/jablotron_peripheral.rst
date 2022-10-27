Jablotron Peripheral
====================

.. seo::
    :description: Instructions for setting up a jablotron_peripheral binary sensor.

The `jablotron_peripheral` binary sensor platform creates a sensor for a peripheral
connected to the Jablotron control panel. The binary sensor requires
:doc:`Jablotron Component </components/jablotron>` to be configured.

Configuration variables:
------------------------
- **name** (*Required*, string): The name of the sensor.
- **index** (*Required*, int): Index of the peripheral in the Jablotron control panel.
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
      - platform: jablotron_peripheral
        index: 1
        name: Gallery motion
        device_class: motion



See Also
--------
- :apiclass:`:jablotron_peripheral::PeripheralSensor`
- :doc:`/components/jablotron`
- :doc:`/components/uart`
- `JA-121 RS-485 Interface <https://jablotron.com.hk/image/data/pdf/manuel/JA-121T.pdf>`__
- :ghedit:`Edit`
