Touchscreen Components
======================

.. seo::
    :description: Instruction for using touchscreen components.
    :image: folder-open.svg

The ``touchscreen`` component holds the base code for most touchscreen driver components
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
- **display** (*Required*, :ref:`config-id`): The display to use this touchscreen with.

- **on_touch** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the touchscreen is touched. See :ref:`touchscreen-on_touch`.
- **on_update** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the touchscreen is touched. See :ref:`touchscreen-on_update`.
- **on_release** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the touchscreen is touched. See :ref:`touchscreen-on_release`.


.. _touchscreen-touchpoint:

``TouchPoint`` argument type.
-----------------------------

Both the :ref:`touchscreen-on_touch` and :ref:`touchscreen-on_update` have an argument of the type :apistruct:`touchscreen::TouchPoint` in a
list or as variable (only ``on_touch``).

The integer members for the touch positions below are in relation to the display width and height:

  ``x`` and ``y`` this shows the current position.
  ``x_last`` and ``y_last`` this shows the priveus position.
  ``x_first`` and ``y_first`` This shows the position of when the touch was firstly detected.

  ``x_raw`` and ``y_raw`` This if for calibrating the touchscreen in relation of the display. This replaces the properties with the same name in the touchscreen classes.

  ``id`` is a number given by the touchscreen referencing the detected touch on a multi touch screen.
  ``state`` shows the state of the touch. This can be **1** as just touched or **2** when the touched position has been moved around.


.. _touchscreen-on_touch:

``on_touch`` Trigger
--------------------

This automation will be triggered when the touchscreen detects a first touch on the touchscreen. And will not be fired until
all touches (for multi touch supported drivers) are release.

NOTE: This is different from before [TODO]release number[/TODO]. When you still want to get the update positions use the :ref:`touchscreen-on_update`.

This trigger provides two arguments named ``touch`` of type :apiref:`touchscreen-touchpoint` and ``touches`` with a list of all touches.


.. _touchscreen-on_update:

``on_update`` Trigger
---------------------

This new automation will be triggered when the touchscreen detects an extra touch or that a touch has moved around on the screen.


This trigger provides one argument named ``touches`` of type :apistruct:`touchscreen::TouchPoints_t` which has has a list of
 :ref:`touchscreen::TouchPoint`.

You can use this trigger for example for gesturn's etc.


.. _touchscreen-on_release:

``on_release`` Trigger
----------------------

This new automation will be triggered when all earlier touches where release from the touchscreen.

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
- :apiref:`touchscreen/touchscreen.h`
- :apiref:`touchscreen/binary_sensor/touchscreen_binary_sensor.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
