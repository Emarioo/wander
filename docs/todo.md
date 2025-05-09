**Generated by ChatGPT**

# Project todos
- Specify which version of the compiler you need for the project. (BTB tends to break between every version)

# 🧙‍♂️ 3D Multiplayer Magic Game – "You Against the World"

## ✅ Core Systems

### 🎮 Game Foundation
- [ ] Window + renderer initialized
- [ ] Load simple terrain or flat ground
- [ ] Basic input system (keyboard + mouse)
- [ ] Player character controller (walk, run, jump, gravity)

### 🎥 Camera System
- [ ] Third-person follow cam with smooth damping
- [ ] Mouse-controlled orbit (hold RMB to rotate)
- [ ] Scroll zoom (FOV or cam distance)
- [ ] Optional: switch to first-person view
- [ ] Camera collision check with world

## ✨ Magic System (Prototype)
- [ ] Define `Spell` struct: name, mana cost, cooldown, cast type, effect
- [ ] Add spell bar (1-3 to switch spells)
- [ ] Add basic casting system
    - [ ] Cast on click (LMB)
    - [ ] Respect cooldown and mana
- [ ] Implement 3 test spells:
    - [ ] Fireball – projectile, explodes on hit
    - [ ] Blink – teleport forward
    - [ ] Shockwave – AoE pushback around player

## 🌐 Multiplayer (Core Sync)
- [ ] Set up basic LAN multiplayer (server-client or peer-to-peer)
- [ ] Sync player position + rotation
- [ ] Sync spell casts (who cast, which spell, position)
- [ ] Show other players casting + moving
- [ ] Simple interpolation for smooth movement

## 🧪 Testing & Polish
- [ ] Dev HUD for stats: FPS, position, mana
- [ ] Cooldown and mana debug print
- [ ] Add dummy targets or bots for testing spells
- [ ] Add sounds (cast, hit, etc.)
- [ ] Add simple damage system (HP, spell impact)

## 🚀 Optional Features (Stretch Goals)
- [ ] Add NPC enemies with simple AI
- [ ] Loot drops and pickups
- [ ] Magic crafting system (combine runes)
- [ ] Persistent progression (XP, levels)
- [ ] Co-op PvE or open-world PvP
- [ ] World zones (biomes, ruins, dungeons)

