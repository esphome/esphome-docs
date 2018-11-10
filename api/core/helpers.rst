Helpers
=======

esphomelib uses a bunch of helpers to make the library easier to use.

API Reference
-------------

helpers.h
*********

.. doxygenfile:: esphomelib/helpers.h

optional.h
**********

.. doxygenfile:: esphomelib/optional.h

ESPPreferences
**************

.. doxygenclass:: ESPPreferences
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: ESPPreferenceObject
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
