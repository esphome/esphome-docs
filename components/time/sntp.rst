SNTP Time Source
================

.. code-block:: yaml

    # Example configuration entry
    time:
      - platform: sntp
        id: sntp_time
        timezone: Europe/Sofia
        servers:  
         - 0.pool.ntp.org
         - 1.pool.ntp.org
         - 2.pool.ntp.org


Configuration variables
-----------------------

- **servers** (*Optional*, list of strings): Choose up to 3 NTP servers that are used for the clock source.
  Defaults to ``0.pool.ntp.org``, ``1.pool.ntp.org`` and ``2.pool.ntp.org``
- All other options from :ref:`base_time_config`.

.. note::

    If your are using :ref:`wifi-manual_ip` make sure to configure a DNS Server (dns1, dns2) or use only IP addresses for the NTP servers.

.. warning::

    Due to limitations of the SNTP implementation, this component will trigger ``on_time_sync`` only once when it detects that the
    system clock has been set, even if the update was not done by the SNTP implementation!
    This must be taken into consideration when SNTP is used together with other real time components, where another time source could
    update the time before SNTP synchronizes.


See Also
--------

- :ghedit:`Edit`
