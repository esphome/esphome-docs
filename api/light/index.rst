Light
=====

.. cpp:namespace:: light

Lights in esphomelib are implemented like fans. Both the hardware and the MQTT frontend
access a combined :cpp:class:`LightState` object and use only that to set state and receive
state updates.

.. toctree::
    fastled.rst

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

.. doxygenclass:: light::LightColorValues
    :members:
    :protected-members:
    :undoc-members:

LightEffect
***********

.. doxygenclass:: light::LightEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::RandomLightEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenstruct:: light::StrobeLightEffectColor
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::StrobeLightEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::FlickerLightEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::LambdaLightEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::BaseFastLEDLightEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::FastLEDLambdaLightEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::FastLEDRainbowLightEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenstruct:: light::FastLEDColorWipeEffectColor
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::FastLEDColorWipeEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::FastLEDScanEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::FastLEDTwinkleEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::FastLEDRandomTwinkleEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::FastLEDFireworksEffect
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::FastLEDFlickerEffect
    :members:
    :protected-members:
    :undoc-members:

LightOutput
***********

.. doxygenclass:: light::LightOutput
    :members:
    :protected-members:
    :undoc-members:


.. doxygenclass:: light::BinaryLightOutput
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::MonochromaticLightOutput
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::CWWWLightOutput
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::RGBLightOutput
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::RGBWLightOutput
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::RGBWWLightOutput
    :members:
    :protected-members:
    :undoc-members:



LightState
**********

.. doxygenclass:: light::LightState
    :members:
    :protected-members:
    :undoc-members:

LightTraits
***********

.. doxygenclass:: light::LightTraits
    :members:
    :protected-members:
    :undoc-members:


LightTransformer
****************

.. doxygenclass:: light::LightTransformer
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::LightTransitionTransformer
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: light::LightFlashTransformer
    :members:
    :protected-members:
    :undoc-members:

MQTTJSONLightComponent
**********************

.. doxygenclass:: light::MQTTJSONLightComponent
    :members:
    :protected-members:
    :undoc-members:
