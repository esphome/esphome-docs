UDP Sensor
==========

.. seo::
    :description: Instructions for setting up a UDP sensor.
    :image: udp.svg

The ``udp`` sensor platform allows you to receive sensor data from another device.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: udp
        provider: thermometer
        id: temperature_id
        remote_id: temp_id


Configuration variables
-----------------------

-  **name** (*Optional*, string): The name of the sensor.
-  **internal** (*Optional*, boolean): Whether the sensor should be exposed via API (e.g. to Home Assistant.) Defaults to true if name is not set, required if name is provided.
-  **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
-  **remote_id** (*Optional*, :ref:`config-id`): The ID of the sensor in the remote device. If not specified defaults to the ID configured with ``id:``.
-  All other options from :ref:`Sensor <config-sensor>`.

At least one of ``id`` and ``remote_id`` must be configured. Since



See Also
--------

- :doc:`/components/udp`
- :doc:`/components/binary_sensor/index`
- :ref:`automation`
- :apiref:`udp/udp_component.h`
- :ghedit:`Edit`
