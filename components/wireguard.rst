WireGuard Component
===================

.. |wireguard| unicode:: WireGuard 0xAE
.. _wireguard: https://www.wireguard.org/

.. seo::
    :description: Instructions to setup WireGuard for your ESP board.
    :keywords: WireGuard, VPN, ESP32

|wireguard|_ is an extremely simple yet fast and modern VPN that utilizes
state-of-the-art cryptography. This component uses a **custom**
implementation not directly developed by |wireguard| authors.

  Please note that *"WireGuard" and the "WireGuard" logo are
  registered trademarks of Jason A. Donenfeld.*

.. warning::

    This component requires the system clock to be synchronized.

    See :doc:`/components/time/index` to setup a time source
    and **do not use** ``homeassistant`` time platform if
    Home Assistant is on the remote peer because the time
    synchronization is a prerequisite to establish the VPN link.

A VPN tunnel can be created to a **single** remote peer
adding the following to your configuration:

.. code-block:: yaml

    # Setup WireGuard
    wireguard:
      address: x.y.z.w
      private_key: private_key=
      peer_endpoint: wg.server.example
      peer_public_key: public_key=

      # Optional pre-shared key
      peer_preshared_key: shared_key=

      # Optional list of allowed ip/mask (any host is allowed if omitted)
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

- **address** (**Required**, IPv4 address): The local VPN address of your board.
- **netmask** (*Optional*, IPv4 address): The netmask for the configured ``address``.
  Default to ``255.255.255.255``.
- **private_key** (**Required**, string): The private key of your board.

- **peer_endpoint** (**Required**, string): The hostname of the remote peer.
- **peer_public_key** (**Required**, string): The public key of the remote peer.
- **peer_port** (*Optional*, UDP port): The port where remote peer is listening.
  The |wireguard| default is ``51820``.
- **peer_preshared_key** (*Optional*, string): The chosen pre-shared key.
- **peer_persistent_keepalive** (*Optional*, :ref:`config-time`): The amount of
  time after which a *keepalive* packet is sent through the tunnel. If there
  are NATs or firewalls between your board and the remote peer set this value to
  something like ``25s``. By default this feature is disabled (``0s``).
- **peer_allowed_ips** (*Optional*, list of IPv4 networks): A list of networks
  in CIDR notation (*IP/mask*) to be allowed through the tunnel. Any host
  (``0.0.0.0/0``) will be allowed if this parameter is omitted.

- **reboot_timeout** (*Optional*, :ref:`config-time`): The amount of time to wait
  before rebooting the board when the remote peer is unreachable. Can be disabled
  by setting this to ``0s``. Default to ``15min``.

See Also
--------

- :doc:`binary_sensor/wireguard_status`
- :doc:`sensor/wireguard_handshake`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    
    ../components/time/index
    ../components/time/ds1307
    ../components/time/gps
    ../components/time/pcf85063
    ../components/time/sntp
    

- `"WireGuard" Trademark Usage Policy <https://www.wireguard.com/trademark-policy/>`__
