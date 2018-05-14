ESP32 LEDC Output
=================

Example Usage
-------------

.. code-block:: cpp

    // Basic
    App.make_ledc_output(33);
    // Custom Frequency
    App.make_ledc_output(33, 2000.0);

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_ledc_output`.

API Reference
-------------

.. cpp:namespace:: nullptr

LEDCOutputComponent
*******************

.. doxygenclass:: output::LEDCOutputComponent
    :members:
    :protected-members:
    :undoc-members:

.. doxygenvariable:: output::next_ledc_channel
