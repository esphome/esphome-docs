Helpers
=======

esphomelib uses a bunch of helpers to make the library easier to use.

API Reference
-------------

helpers.h
*********

.. doxygentypedef:: json_parse_t

.. doxygentypedef:: json_build_t

.. doxygenvariable:: HOSTNAME_CHARACTER_WHITELIST

.. doxygenfunction:: get_mac_address

.. doxygenfunction:: generate_hostname

.. doxygenfunction:: sanitize_hostname

.. doxygenfunction:: truncate_string

.. doxygenfunction:: is_empty

.. doxygenfunction:: reboot

.. doxygenfunction:: add_shutdown_hook

.. doxygenfunction:: safe_reboot

.. doxygenfunction:: add_safe_shutdown_hook

.. doxygenfunction:: to_lowercase_underscore

.. doxygenfunction:: build_json

.. doxygenfunction:: parse_json

.. doxygenfunction:: clamp

.. doxygenfunction:: lerp

.. doxygenfunction:: make_unique

.. doxygenfunction:: random_uint32

.. doxygenfunction:: random_double

.. doxygenfunction:: random_float

.. doxygenfunction:: gamma_correct

.. doxygenfunction:: value_accuracy_to_string

.. doxygenfunction:: uint64_to_string
.. doxygenfunction:: uint32_to_string

.. doxygenfunction:: sanitize_string_whitelist

.. doxygenfunction:: disable_interrupts
.. doxygenfunction:: enable_interrupts

.. doxygenfunction:: crc8

.. doxygenclass:: Optional
    :members:
    :protected-members:
    :undoc-members:

.. doxygenfunction:: parse_on_off

.. doxygenclass:: SlidingWindowMovingAverage
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: ExponentialMovingAverage
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: CallbackManager
    :members:
    :protected-members:
    :undoc-members:

ESPPreferences
**************

.. doxygenclass:: ESPPreferences
    :members:
    :protected-members:
    :undoc-members:

.. doxygenvariable:: global_preferences

esphal.h
********

This header should be used whenever you want to access some `digitalRead`, `digitalWrite`, ... methods.

.. doxygenclass:: GPIOPin
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: GPIOOutputPin
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: GPIOInputPin
    :members:
    :protected-members:
    :undoc-members:


ESPOneWire
**********

esphomelib has its own implementation of OneWire, because the implementation in the Arduino libraries
seems to have lots of timing issues with the ESP8266/ESP32. That's why ESPOneWire was created.

.. doxygenclass:: ESPOneWire
    :members:
    :protected-members:
    :undoc-members:

defines.h
*********

.. doxygenfile:: esphomelib/defines.h
