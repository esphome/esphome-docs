FastLED Light Output
====================

Since version 1.5.0 esphomelib supports many types of addressable LEDs using the FastLED
library.

Example Usage
-------------

.. code-block:: cpp

    // Binary
    auto fast_led = App.make_fast_led_light("Fast LED Light");
    // 60 NEOPIXEL LEDS on pin GPIO23
    fast_led.fast_led->add_leds<NEOPIXEL, 23>(60);

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_fast_led_light`.

API Reference
-------------

.. cpp:namespace:: nullptr

FastLEDLightOutputComponent
***************************

.. doxygenclass:: light::FastLEDLightOutputComponent
    :members:
    :protected-members:
    :undoc-members:
