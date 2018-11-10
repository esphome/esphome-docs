Pulse Counter Sensor
====================

Example Usage
-------------

.. code-block:: cpp

    // Basic
    App.make_pulse_counter_sensor("Pulse Counter", 13);
    // Unit conversion
    auto pcnt_1 = App.make_pulse_counter_sensor("Pulse Counter 2", 13);
    pcnt_1.pcnt->set_unit_of_measurement("kW");
    pcnt_1.pcnt->clear_filters();
    pcnt_1.pcnt->add_multiply_filter(0.06f); // convert from Wh pulse to kW

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_pulse_counter_sensor`.

API Reference
-------------

.. cpp:namespace:: nullptr

.. doxygenclass:: sensor::PulseCounterSensorComponent
    :members:
    :protected-members:
    :undoc-members:
