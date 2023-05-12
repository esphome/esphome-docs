Automatic Updates with Home Assistant
=====================================

.. seo::
    :description: Have Home Assistant keep your ESPHome firmware updated automatically.
    :image: ../images/home-assistant.svg
    :keywords: update upgrade

Have Home Assistsant automatically install updates on your ESPHome devices.

.. figure:: ../images/home-assistant.svg
    :align: center
    :width: 40%


Introduction
------------

ESPHome regularly releases new updates but it is tedious to apply them and ensure all of your online devices have the latest version of ESPHome firmware. 
Using the "python script" feature of ESPHome with a simple automation you can apply upgrades regularly and get notified when upgrades fail.

Configuration
-------------

1. If you don't yet have `Python Scripts <https://www.home-assistant.io/integrations/python_script/>`__  enabled in Home Assistant 
    1. Add ``python_script:`` on it's own line to your ``configuration.yaml``.
    2. Create a folder in your configuration directory called ``python_scripts``
2. Create a new file ``python_scripts/update_esphome_device.py`` with the contents below.

   .. code-block:: python

       # This script find an ESPHome device that needs a upgrade and kicks of the
       # upgrade.
       # It tracks the device it tried to update and next time if confirms
       # it is no longer in the list of upgradable devices. If found it creates
       # a persistant notifcation and trys the next devices in the list. 
       # 
       # This upgrades one device at a time and is designed to do upgrades in the
       # background in no particular hurry. I don't mind if it takes a few days for 
       # my deices to upgrade just so long as I don't have to do anything.
       #
       # Note: If the last device in the list of devices neeeding upgrades fails the
       # script will won't try to update any devices. This script assumes
       # someone will follow up on upgrade failures. If you want to restart from the
       # front of the list delete the entity idenfied by LAST_UPDATE_ENTITY_REC below
       #


       # To make troubleshooting easier change "logger.info" to "logger.error" to put
       # the log lines in the log summary. 
       LOGGER = logger.info

       # Text helper that tracks the last device we tried to update 
       LAST_UPDATE_ENTITY_REC="input_text.esphome_last_upgraded_device"


       last_updated = hass.states.get(LAST_UPDATE_ENTITY_REC).state
       # Ensure we have the helper we need to detect if last update failed.
       if last_updated is None:
           last_updated = "NOT SET"
           hass.states.set(LAST_UPDATE_ENTITY_REC, last_updated)

       LOGGER(f"{last_updated=}")

       # Get a list off every ESPHome device that needs a upgrade
       all_needing_updates = []
       for state in list(hass.states.all()):
         if state.entity_id.startswith("update.") \
           and state.entity_id.endswith("_firmware") \
           and state.state == "on" \
           and state.attributes["title"] == "ESPHome":

           all_needing_updates.append(state.entity_id)

       all_needing_updates.sort() # Don't assume hass.states.all order is dependable

       LOGGER(f"{all_needing_updates=}")

       # If something needs updates
       if all_needing_updates:

         # Look for the last updated device and if found to still be in need of a
         # update assume it's last updated failed. Alert and move on.
         try:
           next_idx = all_needing_updates.index(last_updated) + 1
           hass.services.call(
             "persistent_notification", 
             "create", 
             {
               "message": f"Update of {last_updated} may have failed.",
                "notification_id": f"update_{last_updated}"
             }, 
               False
           )
           except ValueError:
             # If we didn't find our last updated device restart to the begining
             next_idx = 0

           # Ensure the failure didn't happen at the end of the list as we have
           # nothing else todo
           if next_idx < len(all_needing_updates):
             entity_to_update = all_needing_updates[next_idx]
             hass.states.set(LAST_UPDATE_ENTITY_REC, entity_to_update)
             LOGGER(f"Updating {entity_to_update}")
             hass.services.call("update", "install", 
                                {"entity_id": entity_to_update}, False)
           else:
             LOGGER((f"No more devices to try to update, update {last_updated} manually"
                     " to clear this."))
       else:
         LOGGER(f"No ESPHome devices need a update.")

3. Reload your Home Assistant server
4. In Home Assistant create a auotmation to run the python script. Below is a example suitable for a low performance server. It updates a ESPHome device every 20 minutes between 3-6AM every night.

    .. code-block:: yaml

        alias: "ESPHome: Apply updates"
        description: ""
        trigger:
        - platform: time_pattern
            hours: "3"
            minutes: /20
            seconds: "23"
        - platform: time_pattern
            hours: "4"
            minutes: /20
            seconds: "23"
        - platform: time_pattern
            hours: "5"
            minutes: /20
            seconds: "23"
        condition: []
        action:
        - service: python_script.update_esphome_devices
            data: {}
        mode: single
