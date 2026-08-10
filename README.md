# Homestretch

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

Homestretch turns the thermostat's `away` preset into a dynamic one. While
everyone is out, the temperature band stretches toward the preset's outer
bounds to save energy; as people head home, it tightens so the house lands in
the right band — the one it should be in at the projected arrival time — by
the time they walk in.

## How it works

Every ~5 minutes while the house is empty, Homestretch recomputes the away
setpoints from:

- **Travel time home** — the minimum over all tracked people, from a
  best-case minutes-to-home sensor, falling back to crow-flies distance at
  100 km/h when no estimate is available.
- **The recovery model** — measured heating/cooling rates for the house,
  valid across the full outdoor temperature range, used to answer: can the
  house reach the target band by the deadline?

The target band is whatever preset the house will be in at the projected
arrival clock time (arrive at 23:15 and it aims for `sleep`, not `home`).
The static away setpoints act as the outer bounds the dynamic band may
occupy.

All input failures degrade toward comfort: a tracker that stops reporting is
treated as homebound immediately (or inherits its partner's tracker if the
two were together), and a missing outdoor temperature assumes the worst-case
recovery rate. Time spent in known far-away zones is handled by asking
("Home tonight?") and by remote-sleep detection, which pushes the deadline to
wake time + travel and lets the house float deep overnight.

## Entities

Deliberately few:

| Entity | Purpose |
| --- | --- |
| Setpoint low/high | The dynamic away band |
| `sensor.homestretch_deadline` | Projected arrival deadline |
| `sensor.homestretch_reason` | Why the current band was chosen |

One config entry per thermostat.

## Design

The decision core (recovery model, deadline resolution, error ladder,
setpoint math) lives in `core/` as pure Python with no Home Assistant
imports, so it can be unit-tested directly — including replaying real drives
from recorded location history.

See [PLAN.md](PLAN.md) for the full design.

## Installation

Copy `custom_components/homestretch/` into your Home Assistant
`custom_components/` directory and restart, or add this repository to HACS as
a custom repository.

[commits-shield]: https://img.shields.io/github/commit-activity/y/shyndman/ha-homestretch.svg?style=for-the-badge
[commits]: https://github.com/shyndman/ha-homestretch/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/shyndman/ha-homestretch.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40shyndman-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/shyndman/ha-homestretch.svg?style=for-the-badge
[releases]: https://github.com/shyndman/ha-homestretch/releases
