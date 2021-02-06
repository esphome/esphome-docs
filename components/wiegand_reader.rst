Wiegand Reader
==============

.. seo::
    :description: Instructions for setting up a Wiegand Reader or keypad with ESPHome.
    :image: wiegand.png
    :keywords: wiegand, reader, keypad, security, RFID

The ``wiegand_reader`` component can be used to handle RFID tags and key presses of a Wiegand Reader.

.. note::

    More features related to status, keypad and more are coming soon, Stay tuned !

.. figure:: images/wiegand_reader.png
    :align: center
    :width: 70.0%

    Wiegand Reader with keypad.

.. warning::

    Wiegand protocol use 5v while ESP devices operate on 3.3v.
    Usage of a level converter is **strongly** recommended.

.. code-block:: yaml

    # Example configuration entry
    wiegand_reader:
      d0_pin: 5
      d1_pin: 4
      on_tag:
        then:
          - homeassistant.tag_scanned: !lambda 'return x;'

Configuration variables:
------------------------
- **d0_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): Pin connected to the ``D0`` of the Reader.
- **d1_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): Pin connected to the ``D1`` of the Reader.
- **on_tag** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a tag is read. See :ref:`wiegand-on_tag`.

.. _wiegand-on_tag:

``on_tag``
----------

This automation will be triggered when the Wiegand Reader responds with a tag or a key press.

The parameter ``x`` this trigger provides is of type ``std::string`` and is the tag UID in the format
``46568D`` which is the Hexadecimal value of the tag. On a key press, the value of the key will be returned.

The configuration below will for example publish the tag ID on the MQTT topic ``wiegand/tag``.

.. code-block:: yaml

    wiegand_reader:
      # ...
      on_tag:
        then:
          - mqtt.publish:
              topic: wiegand/tag
              payload: !lambda 'return x;'

A tag scanned event can also be sent to the Home Assistant tag component.

.. code-block:: yaml

    wiegand_reader:
      # ...
      on_tag:
        then:
          - homeassistant.tag_scanned: !lambda 'return x;'


See Also
--------

- :apiref:`wiegand_reader/wiegand_reader.h`
- `Yet Another Arduino Wiegand Library <https://github.com/paulo-raca/YetAnotherArduinoWiegandLibrary>`__ by `Paulo Costa (@paulo-raca) <https://github.com/paulo-raca>`__
- :ghedit:`Edit`
