Touchscreen Components
======================

.. seo::
    :description: Instruction for using touchscreen components.
    :image: folder-open.svg

The ``touchscreen`` component contains the base code for most touchscreen driver components
available in ESPHome and is responsible for passing the touch events to
``binary_sensors`` with the ``touchscreen`` platform.

.. _config-touchscreen:

Base Touchscreen Configuration
------------------------------

.. code-block:: yaml

    # Example touchscreen
    touchscreen:
      - platform: ...
        display: display1
        on_touch:
          then:
            ...
        on_update:
          then:
            ...
        on_release:
          then:
            ...

Configuration variables:
************************
- **display** (*Required*, :ref:`config-id`): The display to use this touchscreen with. This will be provided automatically if only one display is configured on the device.

- **on_touch** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the touchscreen is touched. See :ref:`touchscreen-on_touch`.
- **on_update** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the touchscreen is touched. See :ref:`touchscreen-on_update`.
- **on_release** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the touchscreen is no longer touched. See :ref:`touchscreen-on_release`.


.. _touchscreen-touchpoint:

``TouchPoint`` Argument Type
----------------------------

Both the :ref:`touchscreen-on_touch` and :ref:`touchscreen-on_update` have an argument of the type :apistruct:`touchscreen::TouchPoint` in a
list (``on_update``) or as an ``optional`` (``on_touch``).

The integer members for the touch positions below are in relation to the display width and height:

- ``x`` and ``y`` are the current position.
- ``x_last`` and ``y_last`` are the previous position.
- ``x_first`` and ``y_first`` are the position of the touch when it was first detected.
- ``x_raw`` and ``y_raw`` are for calibrating the touchscreen in relation of the display. This replaces the properties with the same name in the touchscreen classes.

- ``id`` is a number provided by the touchscreen to uniquely identify the touch on a multi-touch screen.
- ``state`` indicates the state of the touch. This can be **1**, indicating it is an initial touch, or **2** indicating the touch position has changed/moved.

.. _touchscreen-on_touch:

``on_touch`` Trigger
--------------------

This automation will be triggered when the touchscreen initially detects a touch on the touchscreen; it will not be fired again until
all touches (for multi-touch supported drivers) are released.

NOTE: This has changed (from ESPHome 2023.11.6.) To receive continuous updates from touch drags, use :ref:`touchscreen-on_update`.

This trigger provides two arguments named ``touch`` of type *touchpoint* and ``touches`` with a list of all touches.

.. _touchscreen-on_update:

``on_update`` Trigger
---------------------

This new automation will be triggered when the touchscreen detects an extra touch or that a touch has moved around on the screen.


This trigger provides one argument named ``touches`` of type :apiref:`touchscreen::TouchPoints_t` which has a list of
 :ref:`touchscreen-touchpoint`.

This trigger may be useful to detect gestures such as swiping across the display.


.. _touchscreen-on_release:

``on_release`` Trigger
----------------------

This automation will be triggered when all touches are released from the touchscreen.

At this point of time it has no extra arguments.


Binary Sensor
-------------

The ``touchscreen`` binary sensor allows you to setup areas on the touch screen as virtual
buttons.

.. code-block:: yaml

    binary_sensor:
      - platform: touchscreen
        name: Top Left Touch Button
        x_min: 0
        x_max: 100
        y_min: 0
        y_max: 100
        page_id: home_page_id

Configuration variables:
************************

- **name** (*Optional*, string): The name for the binary sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **touchscreen_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the touchscreen.
- **x_min** (**Required**, int): Left coordinate of the screen area to be detected as the virtual button.
- **x_max** (**Required**, int): Right coordinate of the screen area to be detected as the virtual button.
- **y_min** (**Required**, int): Top coordinate of the screen area to be detected as the virtual button.
- **y_max** (**Required**, int): Bottom coordinate of the screen area to be detected as the virtual button.
- **page_id** (*Optional*, :ref:`config-id`): Only trigger this binary sensor if the display is showing this page.

- All other options from :ref:`Binary Sensor <config-binary_sensor>`.


See Also
--------

- :ref:`Binary Sensor Filters <binary_sensor-filters>`
- :doc:`Inkplate 6 Plus </components/display/inkplate6>`
- :doc:`EKTF2232 </components/touchscreen/ektf2232>`
- :doc:`XPT2046 </components/touchscreen/xpt2046>`
- :doc:`TT21100 </components/touchscreen/tt21100>`
- :doc:`GT911 </components/touchscreen/gt911>`
- :apiref:`touchscreen/touchscreen.h`
- :apiref:`touchscreen/binary_sensor/touchscreen_binary_sensor.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
