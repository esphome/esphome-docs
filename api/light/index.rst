Light
=====

.. cpp:namespace:: light

Lights in esphomelib are implemented like fans. Both the hardware and the MQTT frontend
access a combined :cpp:class:`LightState` object and use only that to set state and receive
state updates.

.. toctree::
    :glob:

    *

Example Usage
-------------

.. code-block:: cpp

    // Binary
    App.make_binary_light("Desk Lamp", App.make_gpio_output(15));
    // Brightness-only
    App.make_monochromatic_light("Kitchen Lights", App.make_ledc_output(16));
    // RGB, see output for information how to setup individual channels.
    App.make_rgb_light("RGB Lights", red, green, blue);
    App.make_rgbw_light("RGBW Lights", red, green, blue, white);

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_binary_light`, :cpp:func:`Application::make_monochromatic_light`,
:cpp:func:`Application::make_rgb_light`, :cpp:func:`Application::make_rgbw_light`.

API Reference
-------------

.. cpp:namespace:: nullptr

LightColorValues
****************

.. doxygenfile:: esphomelib/light/light_color_values.h

LightEffect
***********

.. doxygenfile:: esphomelib/light/light_effect.h

LightOutput
***********

.. doxygenfile:: esphomelib/light/light_output.h

LightState
**********

.. doxygenfile:: esphomelib/light/light_state.h

LightTraits
***********

.. doxygenfile:: esphomelib/light/light_traits.h


LightTransformer
****************

.. doxygenfile:: esphomelib/light/light_transformer.h

MQTTJSONLightComponent
**********************

.. doxygenfile:: esphomelib/light/mqtt_json_light_component.h
