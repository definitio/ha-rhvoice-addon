# RHVoice Home Assistant add-on

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/definitio/ha-rhvoice-addon/builder.yml)
![Docker Pulls](https://img.shields.io/docker/pulls/definitio/ha-rhvoice-addon-aarch64?label=aarch64%20pulls)
![Docker Pulls](https://img.shields.io/docker/pulls/definitio/ha-rhvoice-addon-amd64?label=amd64%20pulls)

This add-on based on [rhvoice-rest](https://github.com/Aculeasis/rhvoice-rest).

## Installation

1. Add a repository by clicking a button: [![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fdefinitio%2Fha-rhvoice-addon)
   or by going to the Supervisor panel in Home Assistant, clicking on the store icon in the top right, paste the URL `https://github.com/definitio/ha-rhvoice-addon` into the repository textarea and click on Save.

2. Install RHVoice Home Assistant add-on
3. Install [RHVoice Home Assistant integration](https://github.com/definitio/ha-rhvoice)
4. Set `host: localhost` in RHVoice configuration.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

## Rhasspy integration

Add to your profile:

```json
"text_to_speech": {
  "system": "remote",
  "remote": {
      "url": "http://localhost:8080/rhasspy?voice=anna"
  }
}
```

[Documentation](https://rhasspy.readthedocs.io/en/latest/text-to-speech/#remote)

## Other

You can buy me a coffee via Bitcoin donation: `bc1qd6khey9xkss6vgd6fqpqdyq4lehtepajkcf256`
