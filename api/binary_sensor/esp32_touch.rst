ESP32 Touch Binary Sensor
=========================

Example Usage
-------------

.. code-block:: cpp

    auto *touch = App.make_esp32_touch_component();
    touch->set_setup_mode(true);
    touch->set_iir_filter(1000);
    App.register_binary_sensor(touch_hub->make_touch_pad("ESP32 Touch Pad 9", TOUCH_PAD_NUM9, 1000));

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_esp32_touch_component`.

API Reference
-------------

.. cpp:namespace:: nullptr

.. doxygenclass:: binary_sensor::ESP32TouchComponent
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::ESP32TouchBinarySensor
    :members:
    :protected-members:
    :undoc-members:
