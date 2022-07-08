.. _remote_receiver_nf:

Remote Receiver NF
==================

.. seo::
    :description: Instructions for setting up remote receiver binary sensors for infrared and RF codes.
    :image: remote.svg
    :keywords: RF, infrared

The ``remote_receiver_nf`` provide an alternative way to receive RF/IR remote signal with noise filtering.

It is **not** to replace :ref:`remote-receiver`, the component is a specialized remote receiver that cope with
nosiy hardware receivers and protocols with short gaps between repeating signals. It works best
if the characteratics of the signal of interest is known.

Recommendation on choosing between ``remote_receiver`` and ``remote_receiver_nf``:

- Choose ``remote_receiver`` if the hardware receiver provides relatively clean
  signal or the receiver is required to decode protocols with different characteratics.

  Most IR receivers and some RF receivers fall into this category.

- Choose ``remote_recevier_nf`` if the output from the hardware receiver is noisy, i.e. output pins keeps toggling
  even  no RF signal of interest is received.
  It is not uncommon among inexpense RF receivers.

.. code-block:: yaml

    # Example configuration entry
    remote_receiver:
      pin: GPIO12
      sync_space_min: 8300us
      sync_space_max: 9500us
      early_check_thres: 100
      sync_space_is_high: false
      repeat_space_min: 1100us

Configuration variables:
------------------------

All ``remote_receiver`` configuration variables are valid for ``remote_receiver_nf``, except the one listed below.
Those common variables are **not** list here. Please see ``remote_receiver``'s :ref:`Configuration Variables <remote-recevier-configuration>` for details.

- **memory_blocks**: ``remote_revevier_nf`` does not use ESP32's builtin RMT hardware, this varialbe is ignored.

To understand how to configure new variables for this recevier, let's first take a look at a typical remote signial:

.. figure:: /components/images/rf_signal_wave.png
     :align: center

Ideally, without sigal of interest, the output from the hardware should park at
``space``. However, for noisy receiver, it keeps toggling. After receiving ring buffer is filled with noise data, the timing
data for real signal could be dropped.

It is very common that timing of ``GAP`` between repeating codes is quite long, so ``IDLE`` and ``GAP`` can be treated the same.
However, ``GAP`` for some protocol is very short, it leads to possible buffer overflow and longer decoding latency for ``remote_receiver``.


``remote_recevier_nf`` introduces additional configuration variables for a different receiving algorithm to combact those issues:

- **sync_space_min** (**Rquired**,int): the minimum time of ``space`` of ``SYNC`` signal
- **sync_space_max** (**Required**,int): the maximum time of ``space`` of ``SYNC`` signal. It should be smaller than ``IDLE``
- **sync_space_is_high** (**Optional**,bool): the logic level of ``space``. Typical is high for IR receiver, low for RF receiver. Default is false
- **num_edge_min** (**Optional**,int): the minimum edges to be considered as a validate code. For example, it would be 34 for
  a 16-bit data (i.e. 32 for ``DATA``, and 2 for ``SYNC``). Default is 16
- **repeat_space_min** (**Optional**,int): the minimum timing of ``GAP`` between repeating codes. If ``IDLE`` and ``GAP``
  can be treated the same, set to a number larger than ``idle``
- **early_check_thres** (**Optional**,int): Typically, received data are sent to decoders after ``IDLE`` being detected.
  However, for a protocol with small ``GAP`` and large number of  repeating codes could lead to buffer overflow, also much
  longer latency. This setting is to trigger decoding before ``IDLE`` is detected. The number should be higher than number
  of edges of a validate code.  Set to 0 to disable this, not recommendated if ``repate_space_min`` is smaller than ``idle``

Automations:

  The automations are the same as ``remote_receiver``'s :ref:`Automations <remote-receiver-automations>`


Binary Sensor
-------------

  The binary sensor is the same as ``remote_receiver``'s :ref:`remote-receiver-binary-sensor`



See Also
--------

- :doc:`index`
- :doc:`/components/remote_receiver`
- :doc:`/components/remote_transmitter`
- `RCSwitch <https://github.com/sui77/rc-switch>`__ by `Suat Özgür <https://github.com/sui77>`__
- `IRRemoteESP8266 <https://github.com/markszabo/IRremoteESP8266/>`__ by `Mark Szabo-Simon <https://github.com/markszabo>`__
- :apiref:`remote/remote_receiver.h`
- :ghedit:`Edit`
