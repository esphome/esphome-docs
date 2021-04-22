DDNS IP updater Component
=========================

.. seo::
    :description: Instructions for setting up the DDNS IP updater in ESPHome.
    :image: ddns.png
    :keywords: DDNS

The DDNS IP updater Component sets up connection with your DDNS provider for update your public IP for a domain.

.. code-block:: yaml

    # Example configuration entry
    ddns:
      service: dynu
      domain: <your_domain>
      username: <your_username>
      password: <your_password>
    # or
    # ddns:
      # service: dynu
      # domain: <your_domain>
      # token: <your_token>
     update_interval: 10000  # Optional default 10000
     use_local_ip: false  # Optional default false


Configuration variables:
------------------------

- **service** (**Required**, string): The host of your MQTT broker.
- **domain** (**Required**, string): The domain for update in
  your DDNS provider.
- **username** (*Optional*, string): The username to use for
  authentication. Empty (the default) means no authentication.
- **password** (*Optional*, string): The password to use for
  authentication. Empty (the default) means no authentication.
- **token** (*Optional*, string): The password to use for
  authentication. Empty (the default) means no authentication.
- **update_interval** (*Optional*, int): Interval for update
  check if the IP change in `ms`. Default ``10000 ms`` (10 seconds)
- **use_local_ip** (*Optional*, boolean): Set ``True`` for send
  local IP to DDNS provider.Defaults to ``False``.


Supported DDNS Providers:
-------------------------

- **DuckDNS**: ``duckdns``
- **No-ip**: ``noip``
- **DynDNS**: ``dyndns``
- **Dynu**: ``dynu``
- **ENom**: ``enom``
- **all-inkl**: ``all-inkl``
- **selfhost.de**: ``selfhost.de`` or ``dyndns.it``
- **strato**: ``strato``
- **freemyip**: ``freemyip``
- **afraid.org**: ``afraid.org``
- **OVH.com**: ``ovh``
