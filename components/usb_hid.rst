USB HID
=======

.. seo::
    :description: Instructions for setting up the USB HID component in ESPHome.

USB Human Interface Devices (HID) specifies devices such as keyboards, mice, game controllers and alphanumeric display devices.

.. code-block:: yaml

    # Example configuration
    hid:
      - platform: usb_device
        id: usb_hid
        type:
          composite:
            - keyboard
            - media_keys


Configuration variables:
------------------------

- **name** (**Required**, *string*): The name for the USD HID.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **type** (**Required**, *string*): Type of USB HID: ``composite`` or ``boot_protocol``. Use ``boot_protocol`` for BIOS control.

  - **composite** (*Optional*, *list*): List of devices to include: ``keyboard``, ``media_keys``, ``mouse``.
  - **boot_protocol** (*Optional*, *string*): ``keyboard`` or ``mouse``.


See Also
--------

- :doc:`/components/usb_device`
- :doc:`/components/keyboard/hid_keyboard`
- :ghedit:`Edit`
