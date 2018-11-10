Fan
====

.. cpp:namespace:: fan

Fans in esphomelib are implemented like lights. Both the hardware and the MQTT frontend
access a combined :cpp:class:`FanState` object and use only that to set state and receive
state updates.

Example Usage
-------------

.. code-block:: cpp

    // Basic
    auto fan = App.make_fan("Fan");
    fan.output->set_binary(App.make_gpio_output(34));
    // Speed
    auto speed_fan = App.make_fan("Speed Fan");
    fan.output->set_speed(App.make_ledc_output(34));
    // Oscillation
    auto oscillating_fan = App.make_fan("Oscillating Fan");
    oscillating_fan.output->set_binary(App.make_gpio_output(34));
    oscillating_fan.output->set_oscillation(App.make_gpio_output(35));

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_fan`.

API Reference
-------------

.. cpp:namespace:: nullptr

FanState
********

.. doxygenclass:: fan::FanState
    :members:
    :protected-members:
    :undoc-members:

FanTraits
*********

.. doxygenclass:: fan::FanTraits
    :members:
    :protected-members:
    :undoc-members:

BasicFanComponent
*****************

.. doxygenclass:: fan::BasicFanComponent
    :members:
    :protected-members:
    :undoc-members:

MQTTFanComponent
****************

.. doxygenclass:: fan::MQTTFanComponent
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: fan::ToggleAction
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: fan::TurnOnAction
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: fan::TurnOffAction
    :members:
    :protected-members:
    :undoc-members:
