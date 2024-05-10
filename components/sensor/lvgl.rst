.. _lvgl-sns:

LVGL Sensor
===========

.. seo::
    :description: Instructions for setting up an LVGL widget sensor component.
    :image: ../images/lvgl_c_num.png

The ``lvgl`` sensor platform creates a semsor component from an LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are :ref:`lvgl-wgt-arc`, :ref:`lvgl-wgt-bar`, :ref:`lvgl-wgt-sli` and :ref:`lvgl-wgt-spb`. A single sensor supports only a single widget; in other words, it's not possible to have multiple widgets associated with a single ESPHome sensor.

Configuration variables:
------------------------

- **widget** (**Required**): The ID of a supported widget configured in LVGL, which will reflect the state of the sensor.
- All other variables from :ref:`Sensor <config-sensor>`.

Example:

.. code-block:: yaml

    sensor:
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
- :doc:`/components/switch/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/light/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/text/lvgl`
- :doc:`/components/text_sensor/lvgl`
- :ghedit:`Edit`
