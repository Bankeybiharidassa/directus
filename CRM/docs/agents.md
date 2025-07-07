# 🤖 agents.md — CLI ↔ GUI Mapping

## 📌 Doel
Deze module beschrijft hoe elke functie beschikbaar is in zowel CLI als GUI, conform Nucleus-ontwikkelmodel.

Alle CLI-functies moeten óf 1-op-1 terugkomen in de GUI, óf als bundeling op logische plekken beschikbaar zijn. Het
volledige overzicht staat in het [root `AGENTS.md`](../AGENTS.md) document en wordt bij elke release gevalideerd.

## 🔍 Testinstructies
Gebruik `lynx` voor handmatige pagina- en menuvalidatie. Draai eerst `./test_install.sh` om de services lokaal te starten.
Vanaf daar kun je naar `http://localhost:8000/core/login?role=<rol>` navigeren en alle menu's doorlopen. Log de resultaten in `logs/codex_gui_loop_<rol>_<datum>.log` en documenteer per rol de dekking in `docs/loops/coverage_<rol>.md`.
