# RHVoice Home Assistant add-on

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armv7 Architecture][armv7-shield]

This add-on based on [rhvoice-rest](https://github.com/Aculeasis/rhvoice-rest).

## Installation

- Find a folder to store add-on

    To get started, we first need access to where Home Assistant looks for local add-ons. For this you can use the Samba or the SSH add-ons.

    For Samba, once you have enabled and started it, your Home Assistant instance will show up in your local network tab and share a folder called `addons`.

    For SSH, you will have to install it. Before you can start it, you will have to have a private/public key pair and store your public key in the add-on config (see docs for more info). Once started, you can SSH to Home Assistant and store your custom add-ons in the `/addons` directory.

- Copy the contents of a `ha-rhvoice-addon/` to `addons/ha-rhvoice-addon/`.
- Open the Home Assistant frontend
- Go to "Settings"
- Click on "Add-ons"
- Click "add-on store" in the bottom right corner [![Open your Home Assistant instance and show the Supervisor add-on store.](https://my.home-assistant.io/badges/supervisor_store.svg)](https://my.home-assistant.io/redirect/supervisor_store/)
- On the top right overflow menu, click the "Check for updates" button
- You should now see a new section at the top of the store called "Local add-ons" that lists `RHVoice`
- Click on `RHVoice` add-on to go to the details page
- Install add-on
- Start add-on
- Install and configure the [RHVoice component for Home Assistant](https://github.com/definitio/ha-rhvoice)

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
