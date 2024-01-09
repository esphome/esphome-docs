.. _lvgl-num:

LVGL Number
===========

.. seo::
    :description: Instructions for setting up a LVGL widget number component.
    :image: ../images/logo_lvgl.png

The ``lvgl`` number platform creates a number component from a LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are ``arc`` and ``slider``. A single number supports
a single widget, thus you need to choose among which one's state you want to use.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the number.
- **animated** (*Optional*, boolean): Wether to set the value of the widget with an animation. Defaults to ``true``.
- **obj** (*Optional*): The ID of a widget configured in LVGL, which will reflect the state of the switch.
- All other options from :ref:`Number <config-number>`.


Example:

.. code-block:: yaml

    number:
      - platform: lvgl
        obj: slider_id
        name: LVGL Slider



See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/sensor/lvgl`
- :doc:`/components/switch/lvgl`
- :ghedit:`Edit`
