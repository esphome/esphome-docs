.. _lvgl-swi:

LVGL Switch
===========

.. seo::
    :description: Instructions for setting up a LVGL widget switch.
    :image: ../images/lvgl_c_swi.png

The ``lvgl`` switch platform creates a switch from a LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are :ref:`lvgl-wgt-btn` (with ``checkable`` option enabled), :ref:`lvgl-wgt-swi` and :ref:`lvgl-wgt-chk`. A single switch supports a single widget, thus you need to choose among which one's state you want to use, options are mutually exclusive.


Configuration options:
----------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the switch.
- **widget** (**Required**): The ID of a widget configured in LVGL, which will reflect the state of the switch.
- **output_id** (*Optional*, :ref:`config-id`): The ID of a binary output to drive in sync with the state of the switch widget.
- All other options from :ref:`Switch <config-switch>`.

Example:

.. code-block:: yaml

    switch:
      - platform: lvgl
        widget: checkbox_id
        name: LVGL switch

Check out :ref:`lvgl-cook-outbin` in the Cookbook for an example how to set up a LVGL Switch component to interact directly with a GPIO.

See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :ref:`Button widget <lvgl-wgt-btn>`
- :ref:`Switch widget <lvgl-wgt-swi>`
- :ref:`Checkbox widget <lvgl-wgt-chk>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/light/lvgl`
- :doc:`/components/output/index`
- :ghedit:`Edit`
