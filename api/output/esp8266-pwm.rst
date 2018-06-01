ESP8266 Software PWM
====================

Software PWM for the ESP8266. Warning: This is a *software* PWM and therefore can have noticeable flickering.
Additionally, this software PWM can't output values higher than 80%. That's a known limitation.

.. _esp8266_pwm-example_usage:

Example Usage
-------------

.. code-block:: cpp

    // Basic
    auto *output = App.make_esp8266_pwm_output(D2);
    // Create a brightness-only light with it:
    App.make_monochromatic_light("Desk Lamp", output);

    // Advanced: Setting a custom frequency globally
    analogWriteFreq(500);

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_esp8266_pwm_output`.

API Reference
-------------

.. cpp:namespace:: nullptr

ESP8266PWMOutput
****************

.. doxygenclass:: output::ESP8266PWMOutput
    :members:
    :protected-members:
    :undoc-members:
