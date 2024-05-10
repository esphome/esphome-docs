.. _lvgl-num:

LVGL Number
===========

.. seo::
    :description: Instructions for setting up an LVGL widget number component.
    :image: ../images/lvgl_c_num.png

The ``lvgl`` number platform creates a number component from an LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are :ref:`lvgl-wgt-arc`, :ref:`lvgl-wgt-bar`, :ref:`lvgl-wgt-sli` and :ref:`lvgl-wgt-spb`. A single number supports a single widget, thus you need to choose among which one's state you want to use.

Configuration options:
----------------------

- **widget** (**Required**): The ID of a supported widget configured in LVGL, which will reflect the state of the number.
- **animated** (*Optional*, boolean): Whether to set the value of the widget with an animation (if supported by the widget). Defaults to ``true``.
- All other options from :ref:`Number <config-number>`.

Example:

.. code-block:: yaml

    number:
      - platform: lvgl
        widget: slider_id
        name: LVGL Slider

See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :ref:`Arc widget <lvgl-wgt-arc>`
- :ref:`Bar widget <lvgl-wgt-bar>`
- :ref:`Slider widget <lvgl-wgt-sli>`
- :ref:`Spinbox widget <lvgl-wgt-spb>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/sensor/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/light/lvgl`
- :doc:`/components/text/lvgl`
- :doc:`/components/text_sensor/lvgl`
- :ghedit:`Edit`
