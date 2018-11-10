ESP32 Bluetooth Low Energy Tracker
==================================

Example Usage
-------------

.. code-block:: cpp

    auto *tracker = App.make_esp32_ble_tracker();
    // MAC address AC:37:43:77:5F:4C
    App.register_binary_sensor(tracker->make_device("ESP32 Bluetooth Beacon", {
	    0xAC, 0x37, 0x43, 0x77, 0x5F, 0x4C
    }));

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_esp32_ble_tracker`.

API Reference
-------------

.. cpp:namespace:: nullptr

.. doxygenclass:: ESP32BLETracker
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: ESP32BLEPresenceDevice
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: ESP32BLERSSISensor
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: XiaomiSensor
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: XiaomiDevice
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: ESPBTDevice
    :members:
    :protected-members:
    :undoc-members:

.. doxygenvariable:: global_esp32_ble_tracker
.. doxygenvariable:: semaphore_scan_end

.. doxygenclass:: ESPBTUUID
    :members:
    :protected-members:
    :undoc-members:
