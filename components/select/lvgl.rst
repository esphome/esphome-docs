.. _lvgl-sel:

LVGL Select
===========

.. seo::
    :description: Instructions for setting up a LVGL widget select.
    :image: ../images/logo_lvgl.png

The ``lvgl`` switch platform creates a select from a LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are :ref:`lvgl-wgt-drp` and :ref:`lvgl-wgt-rol`. A single select supports
a single widget, thus you need to choose among which one's state you want to use, options are mutually exclusive.

Configuration options:
----------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the select.
- **dropdown** (**Required**): The ID of a ``dropdown`` widget configured in LVGL, which will reflect the state of the select; or
- **roller** (**Required**): The ID of a ``roller`` widget configured in LVGL, which will reflect the state of the select.
- All other options from :ref:`Select <config-select>`.

Example:

.. code-block:: yaml

    select:
      - platform: lvgl
        dropdown: dropdown_id
        name: LVGL Dropdown

See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :ref:`Roller widget <lvgl-wgt-rol>`
- :ref:`Dropdown widget <lvgl-wgt-drp>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/light/lvgl`
- :ghedit:`Edit`
