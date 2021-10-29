<h1 align="center">
  <br>
  <img src="./docs/logo.png" alt="EDTVélizy Discord" width="300">
</h1>

<p align="center">
  <a href="https://github.com/Astropilot/EDTVelizyDiscord/actions?query=workflow%3ATest">
    <img src="https://github.com/Astropilot/EDTVelizyDiscord/workflows/Test/badge.svg"
         alt="Test">
  </a>
  <a href="https://github.com/Astropilot/EDTVelizyDiscord/actions?query=workflow%3APublish">
    <img src="https://github.com/Astropilot/EDTVelizyDiscord/workflows/Publish/badge.svg"
         alt="Publish">
  </a>
  <a href="https://codecov.io/gh/Astropilot/EDTVelizyDiscord" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/Astropilot/EDTVelizyDiscord?color=%2334D058" alt="Coverage">
</a>
  <img src="https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-brightgreen">
  <a href="https://github.com/Astropilot/EDTVelizyDiscord/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Astropilot/EDTVelizyDiscord"
         alt="MIT License">
  </a>
  <img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-yellow.svg">
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#usage">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#authors">Authors</a> •
  <a href="#license">License</a>
</p>

## About

EDTVelizyDiscord is a tool that allows you to get the changes of the schedule of the [IUT of Vélizy](https://www.iut-velizy-rambouillet.uvsq.fr/) on a channel discord via the principle of [webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

## Installation

### With Docker

If you want a quick installation and you have Docker, you can use the `astropilot/edtvelizydiscord` image directly.
See [Usage section](#usage) for properly configure the tool.

### Manual installation

EDTVelizyDiscord requires one of the following python versions:
* Python 3.7
* Python 3.8
* Python 3.9

Note: Python 3.6 may work but has not been tested!

Dependencies are managed with the Poetry tool. If you don't have it I invite you to install it by following [the instructions here](https://python-poetry.org/docs/master/#installation).

Then clone this repository and install the dependencies:
```sh
$ git clone https://github.com/Astropilot/EDTVelizyDiscord.git
$ cd EDTVelizyDiscord/
$ poetry install
```

Then use poetry to launch a shell in the python environment containing these dependencies:
```sh
$ poetry shell
```

## Usage

Default settings are defined in `edtvelizydiscord/config.py`:
```python
class Settings(BaseSettings):
    edt_endpoint: str = "http://chronos.iut-velizy.uvsq.fr/EDT/"
    storage_folder: str = "storage/"
    check_delay: float = 900
    color_embed: int = 12866584
    icon_url_embed: str = "https://i.epvpimg.com/iqfidab.png"
    timeout: int = 30

    log_level: int = logging.DEBUG

    groups: List[str] = []
```

All those parameters can be changed with environment variables of the same name, which will automatically rewrite over the default values.

Note: If you use the script directly with python you can also change the parameters directly in the file without going through the environment variables

The `groups` parameter is mandatory to modify to define the groups to monitor and their webhook to use.
To do this you need to pass in an environment variable a JSON list of strings in the following format:
```json
["GROUP_ID1:WEBHOOK_URL1", "GROUP_ID2:WEBHOOK_URL2", ...]
```

The ID of the group to be monitored can be obtained from the URL of the schedule page of a group, for example for the group INF1-A1, the link is `http://chronos.iut-velizy.uvsq.fr/EDT/g178207.html`
The ID here is the number preceded by the g but without the g: `178207`

For example to monitor a particular group you can do the following command:
```sh
# On Linux system
$ export groups='["178207:https://discord.com/api/webhooks/id/token"]'
# On Windows system using PowerShell
PS> $env:groups = '["178207:https://discord.com/api/webhooks/id/token"]'

$ cd edtvelizydiscord
$ python main.py
```

For Docker see the example below:
```sh
$ docker run --env groups='["178207:https://discord.com/api/webhooks/id/token"]' astropilot/edtvelizydiscord:0.1.0-beta
```

## Contributing

The project is open for contributions! [Open an Issue](https://github.com/Astropilot/EDTVelizyDiscord/issues/new) to propose new features or directly make a pull request if you want to implement it yourself. Please respect the conventions defined by editorconfig and the linters/formatters!

## Authors

|            |               Github profile                |   Discord   |
| ---------- | :-----------------------------------------: | :---------: |
| Astropilot | [Astropilot](https://github.com/Astropilot) | [Anos]#2347 |

## License

MIT - See LICENSE file
