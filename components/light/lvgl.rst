.. _lvgl-lgh:

LVGL Light
==========

.. seo::
    :description: Instructions for setting up a LVGL widget light.
    :image: ../images/logo_lvgl.png

The ``lvgl`` light platform creates a light from a LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are :ref:`lvgl-wgt-led`. A single light supports
a single widget, thus you need to choose among which one's state you want to use.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the light.
- **led** (**Required**): The ID of a ``led`` widget configured in LVGL, which will reflect the state of the light.
- **output_id** (**Required**): TODO
- All other options from :ref:`light <config-light>`.


Example:

.. code-block:: yaml

    light:
      - platform: lvgl
        led: led_id
        name: LVGL light

.. note::

    To have linear brightness control, ``gamma_correct`` of the light is set by default to ``0``.


See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :ref:`LED widget <lvgl-wgt-led>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/select/lvgl`
- :ghedit:`Edit`
