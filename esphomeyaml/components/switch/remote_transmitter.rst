Remote Transmitter Switch
=========================

The ``remote_transmitter`` switch platform allows you to create switches
that send a pre-defined remote control sequence
using the :doc:`/esphomeyaml/components/remote_transmitter`. Every time
the switch is turned on, the configured remote signal is sent.

Use cases include, but are not limited to, infrared remotes, 433MHz signals and so on.

.. figure:: images/remote_transmitter-ui.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    remote_transmitter:
      pin: 32

    # Individual switches
    switch:
      - platform: remote_transmitter
        name: "Panasonic TV Off"
        panasonic:
          address: 0x4004
          command: 0x100BCBD
        repeat: 25

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **name** (**Required**, string): The name for the switch.
- The remote code, see :ref:`remote_transmitter-codes`. Only one
  of them can be specified per switch.
- **repeat** (*Optional*, int): How often the command should be sent.

  - **times** (int): The number of times the code should be sent. Defaults to ``1``.
  - **wait_time** (:ref:`time <config-time>`): The time to wait between repeats.

- **remote_transmitter_id** (*Optional*, :ref:`config-id`): The id of the :doc:`/esphomeyaml/components/remote_transmitter`.
  Defaults to the first hub specified.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>` and :ref:`MQTT Component <config-mqtt-component>`.

.. _remote_transmitter-codes:

Remote Codes
~~~~~~~~~~~~

Supported remote codes:

.. code:: yaml

    nec:
      address: 0x4242
      command: 0x8484
    lg:
      data: 0x01234567890ABC
      nbits: 28
    sony:
      data: 0xABCDEF
      nbits: 12
    panasonic:
      address: 0x4004
      command: 0x1000BCD
    raw:
      carrier_frequency: 35kHz
      data:
        - 1000
        - -1000

Configuration variables:

- **nec**: Send a NEC IR code.

  - **address**: The address of the device.
  - **command**: The command to send.

- **lg**: Send an LG IR code.

  - **data**: The data bytes to send.
  - **nbits**: The number of bits to send, defaults to 28.

- **sony**: Send an Sony IR code.

  - **data**: The data bytes to send.
  - **nbits**: The number of bits to send, defaults to 12.

- **panasonic**: Send an Panasonic IR code.

  - **address**: The address of the device.
  - **command**: The command to send.

- **raw**: Send an arbitrary signal.

  - **carrier_frequency**: The frequency to use for the carrier. A lot
    of IR sensors only respond to a very specific frequency.
  - **data**: List containing integers describing the signal to send.
    Each value is a time in µs declaring how long the carrier should
    be switched on or off. Positive values mean ON, negative values
    mean OFF.

.. _finding_remote_codes:

Finding Remote Codes
--------------------

Each remote transmitter uses a different protocol to send its information. So to replicate an infrared or 433MHz
remote you will first need to "learn" these codes. You will first need to hook up a receiver and sniff the codes
using the :doc:`remote receiver component </esphomeyaml/components/remote_receiver>` like this:

.. code:: yaml

    remote_receiver:
      pin: GPIO34
      # dump all signals we find
      dump: all

And then activate the remote control you want to have in esphomelib. you will see a log output like this:

.. figure:: images/rf_receiver-log_raw.png
    :align: center

    Example log output for a 433MHz proprietary remote control.

If esphomelib has a decoder set up for the code, it will spit out the decoded code in the logs. In this case,
it's however a propietary protocol which would be difficult to reverse engineer. Fortunately, we can just
do a "replay attack" by repeating the signal we just saw for our own purposes. The output you see in above image
is encoded in microseconds: A negative value represents the output being LOW for x microseconds and a positive
value denotes the output being HIGH for the specified number of microseconds.

Now you only need to set up the remote transmitter (which well *send* the code) like this:

.. code:: yaml

    remote_transmitter:
       pin: GPIO23
       # Set to 100% when working with RF signals, and 50% if working with IR leds
       carrier_duty_percent: 100%

And lastly, we need to set up the switch that, when turned on, will send our pre-defined remote code:

.. code:: yaml

    switch:
      - platform: remote_transmitter
        name: "My awesome RF switch"
        raw: [4088, -1542, 1019, -510, 513, -1019, 510, -509, 511, -510, 1020,
              -1020, 1022, -1019, 510, -509, 511, -510, 511, -509, 511, -510,
              1020, -1019, 510, -511, 1020, -510, 512, -508, 510, -1020, 1022,
              -1021, 1019, -1019, 511, -510, 510, -510, 1022, -1020, 1019,
              -1020, 511, -511, 1018, -1022, 1020, -1019, 1021, -1019, 1020,
              -511, 510, -1019, 1023, -1019, 1019, -510, 512, -508, 510, -511,
              512, -1019, 510, -509]

Note that you don't need to include the leading ``32519`` here, as it denotes a final space at the end of
a transmission.

See Also
--------

- :doc:`index`
- :doc:`/esphomeyaml/components/remote_transmitter`
- :doc:`/esphomeyaml/components/remote_receiver`
- :doc:`API Reference </api/switch/remote_transmitter>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/switch/remote_transmitter.rst>`__
