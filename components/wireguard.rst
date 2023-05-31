WireGuard Component
===================

.. |wireguard| unicode:: WireGuard 0xAE
.. _wireguard: https://www.wireguard.org/

.. seo::
    :description: Instructions to setup WireGuard for your ESP board.
    :keywords: WireGuard, VPN, ESP32

|wireguard|_ is an extremely simple yet fast and modern VPN that utilizes
state-of-the-art cryptography. This component uses a **custom**
implementation not developed by original authors.

  Please note that *"WireGuard" and the "WireGuard" logo are
  registered trademarks of Jason A. Donenfeld.* See
  `"WireGuard" Trademark Usage Policy <https://www.wireguard.com/trademark-policy/>`__
  for additional information.

.. warning::

    This component requires the system clock to be synchronized.

    See :doc:`time/index` to setup a time source
    and **do not use** ``homeassistant`` time platform if
    Home Assistant is on the remote peer because the time
    synchronization is a prerequisite to establish the VPN link.

A VPN tunnel can be created to a **single** remote peer
adding the following to your configuration:

.. code-block:: yaml

    # Example configuration entry
    wireguard:
      address: x.y.z.w
      private_key: private_key=
      peer_endpoint: wg.server.example
      peer_public_key: public_key=

      # Optional netmask (this is the default if omitted)
      netmask: 255.255.255.255

      # Optional pre-shared key
      peer_preshared_key: shared_key=

      # Optional list of ip/mask (any host is allowed if omitted)
      peer_allowed_ips:
        - x.y.z.0/24
        - l.m.n.o/32  # the /32 can be omitted for single host
        - [...]

      # Optional keepalive (disabled by default)
      peer_persistent_keepalive: 25s

It is recommended to use *secrets* at least for private and pre-shared keys:

.. code-block:: yaml

    wireguard:
      private_key: !secret wg_privkey
      peer_preshared_key: !secret wg_shrdkey

Configuration variables
------------------------

- **address** (**Required**, IPv4 address): The local VPN address of the device.

- **netmask** (*Optional*, IPv4 address): The netmask for the configured address.
  Default to ``255.255.255.255``.

  See section :ref:`wireguard-static-routes` if outgoing connections are
  expected to transit through the VPN link (e.g. with :doc:`mqtt` to a
  remote MQTT broker).

- **private_key** (**Required**, string): The private key of the device.

- **peer_endpoint** (**Required**, string): The hostname of the remote peer.

- **peer_public_key** (**Required**, string): The public key of the remote peer.

- **peer_port** (*Optional*, UDP port): The port where remote peer is listening.
  The |wireguard| default is ``51820``.

- **peer_preshared_key** (*Optional*, string): The chosen pre-shared key between
  local device and remote peer.

- **peer_persistent_keepalive** (*Optional*, :ref:`config-time`): The amount of
  time after which a *keepalive* packet is sent through the tunnel.
  By default this feature is disabled (``0s``).

  If there are NATs or firewalls between the device and the remote peer set
  this value to something like ``25s``.

- **peer_allowed_ips** (*Optional*, list of IPv4 networks): A list of networks
  in CIDR notation (*IP/mask*) to be allowed through the tunnel. Any host
  (``0.0.0.0/0``) will be allowed if this parameter is omitted.

  The device own ``address/32`` is always added by default to this list.

  See section :ref:`wireguard-static-routes` if outgoing connections are
  expected to transit through the VPN link (e.g. with :doc:`mqtt` to a
  remote MQTT broker).

- **reboot_timeout** (*Optional*, :ref:`config-time`): The amount of time to wait
  before rebooting the device when the remote peer is unreachable. Can be disabled
  by setting this to ``0s``. Default to ``15min``.

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _wireguard-static-routes:

Static routes and outgoing connections
--------------------------------------

Currently there is no way on ESP32 devices to configure static routes for
network interfaces, so the ``peer_allowed_ips`` list is used only to allow
(or drop) packets that pass through the VPN tunnel, not to define static
routes for remote hosts.

The routes are implicitly added by the configured ``netmask`` and
**only** packets with destination *inside* the same network defined
by ``address/netmask`` will be routed to the tunnel.

This means that the user has to tweak the ``netmask`` parameter
to "cover" **all** the networks in the allowed IPs list in order
to successfully establish *outgoing* connections to remote hosts.
Incoming connections are not affected by ``netmask``.

Let's explain with some examples:

+--------------+---------------------+----------------------+------------------------------+
| address      | netmask             | allowed ips          | working outgoing connections |
+==============+=====================+======================+==============================+
| 172.16.0.100 | *omitted* or        | *omitted* or         | **none**,                    |
|              | 255.255.255.255     | any other value      | no routes are created        |
+              +---------------------+----------------------+------------------------------+
|              | 255.255.255.0       | *omitted*            | only to ``172.16.0.0/24``    |
+              +                     +----------------------+ because ``192.168.0.0/24``   +
|              |                     | - 172.16.0.0/24      | and any other network will   |
|              |                     | - 192.168.0.0/24     | be outside ``172.16.0.0/24`` |
|              |                     | - *any other*        |                              |
+              +                     +----------------------+------------------------------+
|              |                     | -   192.168.0.0/24   | **none** because             |
|              |                     |                      | ``192.168.0.0/24`` is not    |
|              |                     |                      | part of ``172.16.0.0/24``    |
+--------------+---------------------+----------------------+------------------------------+
| 10.44.0.100  | 255.0.0.0           | *omitted*            | to ``10.0.0.0/8`` network    |
+              +                     +----------------------+------------------------------+
|              |                     | - 10.44.0.0/16       | only to the networks in      |
|              |                     | - 10.10.0.0/16       | the allowed list because the |
|              |                     |                      | netmask will route the whole |
|              |                     |                      | ``10.0.0.0/8`` but wireguard |
|              |                     |                      | allows only those two        |
|              |                     |                      | subnets                      |
+--------------+---------------------+----------------------+------------------------------+
| any          | 0.0.0.0             | *omitted*            | **any**                      |
+              +                     +----------------------+------------------------------+
|              |                     | - 172.16.0.0/24      | to any network that is in    |
|              |                     | - 10.44.0.0/16       | the list of allowed IPs      |
|              |                     | - 10.10.0.0/16       | because the netmask will     |
|              |                     |                      | route any traffic but        |
|              |                     |                      | wireguard allows only its    |
|              |                     |                      | own list                     |
+--------------+---------------------+----------------------+------------------------------+

.. note::

    Setting the ``netmask`` to ``0.0.0.0`` has the effect of routing
    through the VPN link any traffic. It is like having set the wireguard
    interface as the system default.

See Also
--------

- :doc:`binary_sensor/wireguard_status`
- :doc:`sensor/wireguard_handshake`
- :doc:`time/index`
- :doc:`time/sntp`
- :ghedit:`Edit`
