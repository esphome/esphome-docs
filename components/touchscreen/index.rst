Touchscreen Components
======================

.. seo::
    :description: Instruction for using touchscreen components.
    :image: folder-open.svg

The ``touchscreen`` component holds the base code for most touchscreen components
available in ESPHome and is responsible for passing the touch events to
``binary_sensors`` with the ``touchscreen`` platform.

.. _config-touchscreen:

Base Touchscreen Configuration
------------------------------

.. code-block:: yaml

    # Example touchscreen
    touchscreen:
      - platform: ...
        on_touch:
          then:
            ...

Configuration variables:
************************

- **on_touch** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the touchscreen is touched. See :ref:`touchscreen-on_touch`.
- **display** (**Required**, :ref:`config-id`): The display to use. If only one display is
  available, this can be omitted.

.. _touchscreen-on_touch:

``on_touch`` Trigger
--------------------

This automation will be triggered when the touchscreen detects a touch.

This trigger provides one arguments of type :apistruct:`touchscreen::TouchPoint` which has two integer members: ``x`` and ``y`` which
represent the position of the touch in relation to the display width and height. It also has optional members that will be set
depending on the touchscreen platform.

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
- :doc:`XPT2046 </components/binary_sensor/xpt2046>`
- :apiref:`touchscreen/touchscreen.h`
- :apiref:`touchscreen/binary_sensor/touchscreen_binary_sensor.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
