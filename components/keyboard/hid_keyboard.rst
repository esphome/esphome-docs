HID Keyboard
============

.. seo::
    :description: Instructions for setting up HID keyboard in ESPHome that control a HID component.

The ``hid`` keyboard platform allows you to use any HID component as a keyboard.

.. code-block:: yaml

    # Example configuration entry
    keyboard:
      - platform: hid
        name: Blue kbd
        hid_id: usb_hid
        id: kbd

    hid:
      - platform: usb_device
        id: usb_hid
        type:
          composite:
            - keyboard
            - media_keys

Configuration variables:
------------------------

- **hid_id** (**Required**, :ref:`config-id`): The ID of the HID component to use.
- **name** (**Required**, string): The name for the keyboard.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Keyboard <config-keyboard>`.

See Also
--------

- :doc:`/components/usb_hid`
- :ghedit:`Edit`
