UDP Binary Sensor
=================

.. seo::
    :description: Instructions for setting up a UDP binary sensor.
    :image: udp.svg

The ``udp`` binary sensor platform allows you to receive binary sensor data from another device.

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: udp
        provider: light-switch
        id: switch_status
        remote_id: light_switch


Configuration variables
-----------------------

-  **name** (*Optional*, string): The name of the binary sensor.
-  **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
-  **remote_id** (*Optional*, :ref:`config-id`): The ID of the binary sensor in the remote device. If not specified defaults to the ID configured with ``id:``.
-  All other options from :ref:`Binary Sensor <config-binary_sensor>`.

At least one of ``id`` and ``remote_id`` must be configured.


See Also
--------

- :doc:`/components/udp`
- :doc:`/components/binary_sensor/index`
- :ref:`automation`
- :apiref:`udp/udp_component.h`
- :ghedit:`Edit`
