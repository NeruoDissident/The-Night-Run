# Fractured City: Night Run

![Night Run logo](icons/icon-192.png)

**[Play the live game](https://neruodissident.github.io/The-Night-Run/)** · Installable on iPhone · Offline after the first load

A standalone, turn-based urban survival RPG. An original, compressed interpretation of the supplied game brief, playable from character creation to escape, faction commitment, or permadeath.

## Play on iPhone

1. Open **https://neruodissident.github.io/The-Night-Run/** in Safari.
2. Tap **Share → Add to Home Screen**. Keep **Open as Web App** enabled if shown, then tap **Add**.
3. Open the **Night Run** icon once while online. Wait for **Ready to play offline** on the title screen. It can now launch without a connection.
4. Use the eight-direction pad, action buttons, and **Target / Fire / Dash** controls. A full run is playable without a keyboard. The map and controls remain on screen together; dialogs scroll separately.

Game saves stay on the device. Safari, an installed web app, and another browser may have separate storage. To move a run, choose **Export save**, save the JSON to Files, then **Import save** inside the installed app. Clearing browser/app data may remove saves. There is no account or cloud sync.

Updates are downloaded in the background and offered through **Install app / offline status → Save & apply update**. A waiting update never interrupts a run. App caches are isolated to this repository path and do not delete saved games or other apps’ caches.

## Play on desktop / portable edition

Open **Night Run.html** in a current desktop browser. No installation, account, internet connection, external assets, or server is required. All game code, artwork and sound generation are inside that file.

Choose **Enter the city**, pick a class, and begin. A seed is optional. Speak to Mara one step east, spend your first talent point, and explore. Use the in-game **Field guide** for controls and survival advice.

If your browser restricts storage for local files, **Export save** from the pause menu and use **Import save** next time. Browser storage is specific to the browser and location where you play. The autosave indicator reports a storage failure. Private browsing may discard saves when closed.

For local development, run `python build.py`, then `python -m http.server 8765 --bind 127.0.0.1` from this folder and open `http://127.0.0.1:8765/`. Service workers work on localhost and HTTPS. A phone needs the HTTPS live site; a desktop localhost address is not reachable from your phone.

## Controls

| Action | Control |
| --- | --- |
| Move / bump attack | WASD or arrow keys |
| Dash | Shift + movement; costs energy |
| Interact | E; or click an adjacent object |
| Use class ability | 1 |
| Toggle stealth | X |
| Select enemy / attack | Tab / F; or click an enemy |
| Wait | Space or period |
| Quick medical supply | H |
| Inventory / character | I / C |
| Journal / city atlas | J / M |
| Craft | K |
| Pause | Escape |
| Walk to known floor | Click; automatically stops when a hostile is seen |

Mouse controls and a touch directional pad are also included. On narrow screens, the pause menu provides the panels normally shown in the sidebar. A click on an out-of-range enemy still selects it, allowing a grenade to be used from inventory.

## In this game

- **Eight persistent procedural districts:** Lowlight Blocks, Mercy Arcade, Rainline Viaduct, Cinderworks, Suture Ward, Glass Meridian, Drowned Exchange, and the Listening Spire. Connected urban interiors, locked doors, cover, hidden caches, service ducts, hazards, and fog of war.
- **Six classes:** Street Kid, Deserter, Wirewalker, Patch Doctor, Scrapper, and Signal Touched. Each has its own equipment, attributes, active power, and two exclusive three-tier specializations: **12 paths and 36 talents**.
- **Four factions and eight named contacts.** Finite-stock trade, reputation prices, medical care, augmentation clinics, local jobs, rivalry consequences, and faction endings.
- **Eight district quests plus eight local contracts**, optional encounters, and three escape campaigns. Objectives support force, hacking, social influence, or paid access.
- **Tactical combat:** melee and ranged weapons, ammunition, line of sight, cover, stealth, sound, evasion, retreat, flanking, patrols, machines, signal enemies, elite guardians, deployable sentries, and converted drones.
- **An interconnected item pool:** weapons, armor, packs, consumables, ammunition, materials, valuables, weapon modifications, and 12 Chrome/Flesh augmentations. Carrying pressure, durability, repairs, contextual loot, finite vendors, and 10 crafting recipes.
- **Survival across days:** nutrition, hydration, fatigue, injuries, safe beds, clinic treatment, weather, blackouts, nighttime salvage, and roaming threats.
- **The Echo:** exposure, fragments, signals, anomalies, altered bodies, and an ambiguous escape route.
- **Three distinct escape endings, faction futures, and death summaries.** Export a run’s story as a text file. Previous lives leave a remembered count; they do not confer power bonuses.
- **Local autosaving, save export/import, settings, sound effects, combat feedback, a field guide, mouse and keyboard controls, and a responsive interface.**

## Progression and endings

District objectives lie in the far rooms. Resolve them to gain experience, credits, an Echo fragment, and faction consequences. Guardians can be fought or avoided. Choose who receives each objective; an alliance often angers its rival. A completed objective's route knowledge remains yours even if you choose the rival.

**Train:** resolve Rainline and Cinderworks, carry 8 scrap, and reach Rainline’s train. Requires Union reputation 15 or intellect 6.

**Aircraft:** resolve Glass Meridian, gain Directorate reputation 15, and bring 160 credits to its landing pad.

**Echo:** resolve the Spire, gather at least 3 fragments, and reach the impossible door at night.

**Stay:** reach reputation 45 with a faction and pledge yourself through one of its contacts.

You do not need to clear every district to end a run. Death removes the active local save. Exported files are ordinary user-owned saves and are not deleted.

## Source and maintenance

- `src/data.js`: classes, items, factions, zones, enemy archetypes, talents, recipes.
- `src/engine.js`: deterministic state, generation, vision, AI, combat, progression, quests, trade, survival, saves, and endings. It has no DOM dependency.
- `src/ui.js`: presentation, canvas renderer, input, menus, audio, and browser persistence.
- `src/style.css`, `src/mobile.css`, and `src/index.html`: layout and visual styling, including safe-area-aware touch controls.
- `src/pwa.js`, `src/sw.template.js`, and `manifest.webmanifest`: install UI, lifecycle saves, versioned offline caching, and app identity.
- `icons/` and `apple-touch-icon.png`: original SVG mark, standard/maskable icons, and the 180px Apple icon. Regenerate with `python tools/make_icons.py` (Pillow needed only for this optional art tool).
- `build.py`: reconstructs `index.html`, the portable `Night Run.html`, `sw.js`, and the clean `_site/` deployment folder. Run `python build.py` after changing source. Normal builds have no third-party dependencies. The worker version changes with the bundled game, its assets, or worker logic.
- `tests/engine.test.cjs`: automated integration checks. Run `node tests/engine.test.cjs` with Node 18 or later.

The game uses a seeded xorshift random stream stored in each save. Revisiting a district preserves its objects, occupants, loot, and vendor stock. Generated maps are compact room-and-corridor urban dungeons, with district-specific structure and decoration. The campaign is a complete smaller game rather than a simulation of every detail of an actual city.

## Validation

Automated checks cover 800 generated district maps for reachable content; deterministic seeds; saved world and random-state round trips; sight blocking and doors; all six class powers; branching progression; recipes; ranged combat; all district objectives and local jobs; escape conditions and endings; finite trade; augmentations; second-heart survival; permadeath; and resting across days.

Browser checks cover character creation, movement, contact dialogue, trade, inventory, talents, resume, and desktop/narrow-screen layout. These checks establish functional coverage; they do not imply exhaustive balance testing of every build and seed.

## Publish / continuous checks

GitHub Pages uses **GitHub Actions** as its publishing source. Every push to `main` runs the game, PWA worker, and artifact checks before publishing `_site/`. Pull requests run the same checks without deploying. The workflow can also be dispatched manually. Relative manifest, icon, start, and service worker URLs support the `/The-Night-Run/` repository path.

Run locally:

```text
python build.py
node tests/engine.test.cjs
node tests/pwa.test.cjs
python tests/build_test.py
```

The worker suite checks root and repository-subpath installs, offline navigation, server-error fallback, cached icons, cache isolation, and player-controlled updates. The artifact suite checks iPhone metadata, icon sizes, touch controls, and a complete self-contained build. Mobile viewport checks are not a claim of testing on a physical iPhone; the platform follows Safari's standard home-screen app support.
