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
- **arc_id** (*Optional*): The ID of an arc widget configured in LVGL.
- **slider_id** (*Optional*): The ID of a slider widget configured in LVGL.
- All other options from :ref:`Number <config-number>`.


Example:

.. code-block:: yaml

    number:
      - platform: lvgl
        slider_id: lv_slider
        id: lvgl_slider_sensor
        name: LVGL Slider



See Also
--------
- :ref:`LVGL <lvgl-main>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/sensor/lvgl`
- :ghedit:`Edit`
