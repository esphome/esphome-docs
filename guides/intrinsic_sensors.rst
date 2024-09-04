List of Sensors Intrinsic to ESPHome
====================================

.. seo::
    :description: An exhaustive list of all current sensors intrinsic or internal to ESPHome.
    :image: folder-open.svg


.. _intrinsic-sensors:

This page intends to list all sensors intrinsic to the ESPHome platform requiring nothing more than a compatible device.

Here is the list of sensors in each category:

Bluetooth:
----------

- :doc:`components/text_sensor/ble_scanner`
- :doc:`components/sensor/ble_rssi`

WiFi:
-----

- :doc:`components/text_sensor/wifi_info`
- :doc:`components/sensor/wifi_signal`

Debug:
------

- :doc:`components/sensor/uptime`
- :doc:`components/debug`
- :doc:`components/sensor/internal_temperature`
- :doc:`components/text_sensor/version`

Misc.:
------

- :doc:`components/copy`
- :doc:`components/binary_sensor/esp32_touch`

See Also
--------

- :ref:`config-sensor`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
