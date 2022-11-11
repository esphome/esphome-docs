Wiegand reader, keypad
======================

.. seo::
    :description: Wiegand-standard key input and card/tag reader panel
    :image: wiegand.jpg

The ``wiegand`` component allows you to integrate Wiegand-standard key 
input and card or tag reader panels in Home Assistant.

.. figure:: ../images/wiegand.jpg
    :align: center



.. note::

    This component also needs the ``key_provider`` component in order to work.



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
