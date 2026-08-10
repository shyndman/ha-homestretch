# Homestretch — Design Plan

Dynamic away-mode HVAC for Home Assistant. The band stretches while you're
away, and tightens on the home stretch.

## Concept

`away` is not a static preset. It is a dynamic, automation-driven preset whose
setpoints are recomputed on a schedule (~every 5 minutes) from:

1. **Distance/travel time to home** — minimum over Scott and Hilary (they may
   not be together).
2. **The house's recovery ability** — can it reach the preset the house WILL
   be in at the projected arrival *clock time*? (Arrive 23:15 → target the
   `sleep` band, not `home`.)

The static `away` setpoints (16–30 °C) become the **outer min/max bounds** the
dynamic setpoints may occupy. Far away → float wide (savings). Approaching →
band tightens so the house lands in the target band by arrival.

Away mode is therefore its own recovery controller — no separate
trigger/guard-rail automation.

## Entry / exit

- Enter: both Scott and Hilary leave the house. (Dogs later, once leash
  trackers are back up.)
- Trackers of record: `device_tracker.google_maps_scott_hyndman`,
  `device_tracker.google_maps_hilary_hacksel` (the person-entity Google Maps
  trackers — NOT `pixel_7a`). Both write lat/lon to InfluxDB
  (`homeassistant` org, `habucket`, ~2 min cadence, 3 y retention) for replay
  testing.
- `apply_computed_preset` remains the **sole writer** to the thermostat.

## Travel time

- Scott is building a numeric **best-case minutes-to-home** sensor. (Does not
  exist yet.)
- Best-case is deliberate: it biases toward comfort. Do NOT add buffers or
  error factors on top — if the estimate is wrong, HA can't know; do nothing.
- Fallback when travel time is missing/unresolvable: crow-flies distance at
  **100 km/h** (unrealistically fast on purpose — comfort-biased). Locations
  Google Maps can never route (e.g. the cottage) get special-casing later,
  by Scott.

## Error states — fail toward COMFORT

All input degradation biases toward a tighter band (the dogs must not get
hot).

| Failure | Behavior |
|---|---|
| Tracker offline | Distrust **immediately** (no staleness window). |
| Tracker offline, pair was "fairly close" at that moment | Assume still together — inherit the partner's tracker. |
| Tracker offline, pair was apart | Assume that person homebound **from the offline instant**, deadline from last known position (crow-flies @ 100 km/h). |
| Travel time missing | Crow-flies fallback above. |
| Travel time present but wrong | Nothing. No buffers. |
| Outdoor temp missing | Assume **worst-case** recovery rate. |

- "Fairly close" radius: **1 km** to start (test pending on a real drive
  home).
- Co-freshness rule: separation is only computed from **co-fresh fixes**
  (both trackers' fixes timestamped within ~90 s of each other); comparing a
  live fix against a stale one fabricates separation. Validated against the
  July 2 drive: at every co-fresh pair the two were < 1 km apart; apparent
  1–2.4 km excursions were staleness artifacts (highway update gaps of
  2–8 min). Implementation shape in HA terms: hold "distance at last
  co-fresh pair" and read that when a tracker drops.

## Far-zone handling (e.g. The Farm, ~65 km out)

Being in a named zone means *staying somewhere*, not en route — do NOT assume
homebound.

1. **Ask** — actionable notification ("Home tonight?"). Yes → provided ETA is
   the deadline. No → float to the outer band until they leave the zone.
   **Hilary is always asked.**
2. **No answer — Scott's remote-sleep signals** (either):
   - after 21:00 + stationary + laptop input/media active in the past hour
     (`binary_sensor.scott_linux_laptop_input_active`,
     `media_player.scott_linux_laptop_desktop_media`), or
   - `sensor.pixel_7a_sleep_confidence` > 70 — known to really mean "settled
     in a dark room"; accepted as correct *for this purpose* (can't
     false-fire while driving; motion kills it).
3. Sleep detected → deadline = assumed wake **07:30** + travel time; the
   house floats deep overnight and still recovers.

## Recovery model — rebuild required

The current cooling model floors to 0 above ~29.5 °C outdoor
(`cool_net = max(0, 1.4 − 0.09·(T_out − 14))`), making the ETA −1 exactly
when it matters (observed at 35 °C). Unacceptable — this hole shipped
silently once; never again.

- The rebuilt model MUST produce finite, sane estimates across the **full**
  outdoor range the house can encounter (heating and cooling).
- A few degrees of prediction error is fine. Failure to predict is not.
- Existing measured anchors: heat_net ≈ 3.1 °C/h flat; passive drift
  k ≈ 0.031 °C/h per °C ΔT; 13 months of InfluxDB ramps available to refit.

## Architecture

Custom integration (`custom_components/homestretch`), not
PyScript/AppDaemon — this is a state machine (deadline resolution, error
ladder, zone/ask/sleep branches, periodic recompute), and it must be typed
and testable.

- **`core/`** — pure Python, zero `homeassistant` imports. All math and
  decisions: recovery model, deadline resolution, setpoint computation, error
  ladder. Fully pytest-able, including full-range model tests and drive
  replays from Influx history.
- **Coordinator** — feeds `core/` from HA state on the ~5 min cadence, owns
  the config entry. One config entry per thermostat (single thermostat is the
  base case; multi falls out of entry-per-thermostat later).
- **Exported entities (few, deliberately):**
  - dynamic setpoint pair (low/high)
  - `sensor.homestretch_deadline` — projected arrival deadline
  - `sensor.homestretch_reason` — diagnostic: WHY it chose what it chose
- Scaffold cleanup: the template is an air-purifier example. Delete `fan/`,
  `select/`, `number/`, `button/`, `switch/`, `api/`, `example_service`.
  Keep `coordinator/`, `config_flow*`, `sensor/`, `binary_sensor/`,
  `diagnostics`.

## Open items

- Scott: travel-time sensor (best-case minutes to home).
- Scott: cottage-style special cases for unroutable locations.
- 1 km "fairly close" radius: validate on a real drive home.
- Both-out entry signal: derive from the two Google Maps trackers
  (`is_anyone_out` is *either*, not *both*).
- Dogs' leash trackers, once running.
