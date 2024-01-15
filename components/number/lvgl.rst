.. _lvgl-num:

LVGL Number
===========

.. seo::
    :description: Instructions for setting up a LVGL widget number component.
    :image: ../images/logo_lvgl.png

The ``lvgl`` number platform creates a number component from a LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are :ref:`lvgl-wgt-arc`, :ref:`lvgl-wgt-bar` and :ref:`lvgl-wgt-sli`. A single number supports
a single widget, thus you need to choose among which one's state you want to use.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the number.
- **animated** (*Optional*, boolean): Wether to set the value of the widget with an animation. Defaults to ``true``.
- **obj** (**Required**): The ID of a widget configured in LVGL, which will reflect the state of the switch.
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
- :ref:`Arc widget <lvgl-wgt-arc>`
- :ref:`Bar widget <lvgl-wgt-bar>`
- :ref:`Slider widget <lvgl-wgt-sli>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/sensor/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/light/lvgl`
- :ghedit:`Edit`
