Wiegand reader, keypad
======================

.. seo::
    :description: Wiegand-standard key input and card/tag reader panel
    :image: matrix_keypad.jpg

The ``matrix_keypad`` component allows you to integrate pads which
have the keys connected at the intersection points of the rows and columns 
of a matrix.

.. figure:: ../images/matrix_keypad.jpg
    :align: center


.. note::

    This component also needs the ``key_provider`` component in order to work.


Define a `keypad` component then add `binary_sensor`s to handle individual keys.  You need to also import the `key_provider` component.
If you want automatic handling for multiple keys, e.g. PIN entry, use the `input_builder` component.

The `keys` parameter is optional for the `keypad`, but then you won't be able to check for it in the `binary_sensor`
and the `input_builder` won't work if you want to use that.
The optional `has_diodes` parameter is for if the buttons have diodes and the row pins are output only. In that case, set it to true.

For the `binary_sensor`, you need to provide either the `row` and `col` parameters or the `key` parameter.


Individual keys can be added to ESPHome as separate ``binary_sensor``s





.. code-block:: yaml

    # Example configuration entry
    key_provider:
    wiegand:
      - id: reader
        d0: 4
        d1: 5
        on_tag:
          - lambda: ESP_LOGD("TEST", "received tag %s", x.c_str());
        on_key:
          - lambda: ESP_LOGD("TEST", "received key %d", x);



Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Set the ID of this device for use in lambdas.
- **d0** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin where the D0 output 
  of the Wiegand's interface connects.
- **d1** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin where the D1 output 
  of the Wiegand's interface connects.


Automations:
------------

- **on_tag** (*Optional*, :ref:`Automation <automation>`): An automation to perform 
  when a card or a tag has been read by the device. The code is placed in variable `x`.
- **on_key** (*Optional*, :ref:`Automation <automation>`): An automation to perform 
  when a key has been pressed on the panel. The key is placed in variable `x`.


.. note::

    Automatic handling of multiple keys (e.g. PIN code entry) is possible with the 
    the ``key_collect`` component.


See Also
--------

- :doc:`/components/key_collect`
- :doc:`/components/key_provider`
- :ref:`automation`
- :ghedit:`Edit`
