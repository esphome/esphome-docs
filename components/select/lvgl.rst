.. _lvgl-sel:

LVGL Select
===========

.. seo::
    :description: Instructions for setting up a LVGL widget select.
    :image: ../images/lvgl_c_sel.png

The ``lvgl`` switch platform creates a select from a LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are :ref:`lvgl-wgt-drp` and :ref:`lvgl-wgt-rol`. A single select supports
a single widget, thus you need to choose among which one's state you want to use.

Configuration options:
----------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the select.
- **widget** (**Required**): The ID of a supported widget configured in LVGL, which will reflect the state of the select.
- All other options from :ref:`Select <config-select>`.

Example:

.. code-block:: yaml

    select:
      - platform: lvgl
        widget: dropdown_id
        name: LVGL Dropdown

See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :ref:`Roller widget <lvgl-wgt-rol>`
- :ref:`Dropdown widget <lvgl-wgt-drp>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/sensor/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/light/lvgl`
- :doc:`/components/text/lvgl`
- :doc:`/components/text_sensor/lvgl`
- :ghedit:`Edit`
