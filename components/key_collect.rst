Key collect component
=====================

.. seo::
    :description: Key collect component

The ``key_collect`` component collects key presses from ``key_provider`` 
components like ``matrix_keypad`` or ``wiegand``. It allows you to process 
key sequences and treat them as one, for example to ease up inputting of 
a PIN code or a passkey. The component outputs the result of the keypress
sequence as a variable usable in automations.


Component
---------

.. code-block:: yaml

    # Example configuration entry
    key_collect:
      - id: pincode_reader
        source_id: mykeypad
        min_length: 4
        max_length: 4
        end_keys: "#"
        end_key_required: true
        back_keys: "*"
        clear_keys: "C"
        allowed_keys: "0123456789"
        timeout: 5s
        on_progress:
          - logger.log: 
              format: "input progress: '%s'"
              args: [ 'x.c_str()' ]
        on_result:
          - logger.log: 
              format: "input result: '%s'"
              args: [ 'x.c_str()' ]


Configuration variables:

- **id** (*Optional*, :ref:`config-id`): Set the ID of this entry for use in lambdas.
- **source_id** (*Optional*, :ref:`config-id`): The ID of the key input device (relying on ``key_provider`` component).
- **min_length** (*Optional*, integer): The minimal length of the desired key sequence. Below
  this, ``on_result`` automation will not trigger even if any of the ``end_keys`` was pressed.
- **max_length** (*Optional*, integer): The maximum length of the desired key sequence, after 
  which the sequence will trigger the ``on_result`` automation witout having to press any of the ``end_keys``
- **end_keys** (*Optional*, string): Keys used to *enter* the sequence.
- **end_key_required** (*Optional*, boolean): Only trigger ``on_result`` automation when one of
  the ``end_keys`` was pressed. Defaults to ``false``.
- **back_keys** (*Optional*, string): Keys used to delete the last pressed key. Like *Backspace* on a keyboard.
- **clear_keys** (*Optional*, string): Keys used to entirely clear the sequence, all the pressed keys.
- **allowed_keys** (*Optional*, string): Keys allowed to be used. If not specified, then any otherwise 
  unused keys will be allowed.
- **timeout** (*Optional*, :ref:`config-time`): Timeout after which to cancel building the sequence and delete all the keys.

At least ``end_keys`` or ``max_length`` have to be specified. The rest are optional.

Automations:
------------

- **on_progress** (*Optional*, :ref:`Automation <automation>`): An automation to perform 
  when keys are pressed. The increasing sequence of the pressed is placed in variable `x`.
  Useful if you want to have a display showing, or a speaker beeping while keys are being pressed.
- **on_result** (*Optional*, :ref:`Automation <automation>`): An automation to perform 
  when the sequence has been finished (eg. ``max_length`` has been reached or one of
  the ``end_keys`` was pressed). The finalized key sequence is placed in variable `x`.


See Also
--------

- :doc:`/components/matrix_keypad`
- :doc:`/components/viegand`
- :doc:`/components/key_provider`
- :ref:`automation`
- :ghedit:`Edit`
