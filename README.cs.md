<div align="center">

# Repo Visualizer

**Pochopte mechanismus za zdrojovým kódem.**

Otevřený skill pro Codex a Claude Code: z otázky nad repozitářem vytvoří graf komponent, odkazy do kódu a animaci.

[Živá ukázka](https://honzacuhel.github.io/repo-visualizer/?lang=cs) · [Instalace](#instalace) · [Vydané verze](https://github.com/HonzaCuhel/repo-visualizer/releases)

[English](README.md) · Česky

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="site/media/walkthrough-cs-dark.gif">
  <img src="site/media/walkthrough-cs.gif" alt="Graf spouštění příkazu v Codexu, včetně schvalování, podmíněného opakování a odpovídajícího zdrojového kódu." width="100%">
</picture>

Agent přečte implementaci a popíše odpovědnosti a vztahy. Průzkumník pak zobrazí tento graf. Větvení zůstane větvením, opakování smyčkou; volitelný průchod zvýrazní cestu stejnou topologií.

## Instalace

Spusťte uvnitř svého repozitáře:

```sh
npx skills add HonzaCuhel/repo-visualizer --skill repo-visualizer -a codex -a claude-code
```

Pro jednoho agenta ponechte jen jeho `-a`. Volba `-g` nainstaluje skill pro všechny vaše projekty. Instalaci z tohoto GitHub repozitáře zajišťuje existující [skills CLI](https://github.com/vercel-labs/skills).

Poté požádejte agenta:

> Pomocí repo-visualizer vysvětli, jak tato funkce funguje. Zahrň hlavní komponenty, vztahy a chybové větve. Vytvoř interaktivní HTML graf a krátký GIF.

K dispozici je také kompletní ZIP a kontrolní součet SHA-256 ve [vydaných verzích](https://github.com/HonzaCuhel/repo-visualizer/releases). Při ruční instalaci ponechte složku skillu celou.

| Požadavek | K čemu slouží |
| --- | --- |
| Codex nebo Claude Code | Čtení repozitáře a tvorba vysvětlení |
| Node.js 22.20+ | Instalace přes `npx skills` |
| Python 3.9+ | Inventář, ověření zdrojů a sestavení HTML |
| Volitelné vykreslovací nástroje | Export obrázků a animací; viz [návod](skills/repo-visualizer/references/exports.md) |

## Zvolte si pohled

| Pohled | Výsledek |
| --- | --- |
| **Mapa** | Úplná topologie včetně větvení, smyček, paralelních vazeb a vnořených skupin |
| **Okolí** | Vybraná komponenta a její přímé vztahy |
| **Průchod** | Vysvětlení vybrané cesty stejným grafem |

Komponentu nebo vztah lze rozkliknout, přečíst si vložený úryvek a otevřít konkrétní revizi kódu. Přenositelné HTML má hledání, přiblížení, posouvání i klávesové ovládání a funguje offline.

## Jeden graf, více formátů

**Interaktivní HTML · JSON · SVG · PNG · GIF · MP4 · WebM**

HTML zachovává klikatelné důkazy. Obrázky a videa přenášejí vizuální vysvětlení. Přehrávač i exportéry používají stejný graf a scénu; k dispozici je také volitelný adaptér HyperFrames.

Světlý, tmavý a systémový vzhled volí uživatel. Jazyk vysvětlení určuje zadání, nezávisle na agentovi. Ovládání má vestavěnou češtinu a angličtinu; další jazyky mohou dodat vlastní překladový slovník. Zdrojový kód, názvy symbolů a cesty se nepřekládají. [Jazyky a vzhled](skills/repo-visualizer/references/localization.md).

## Důkazy a ověření

Skill ověřuje řádky, otisky a revizi zdrojů. Významové vysvětlení ale tvoří agent: shoda se zdrojem sama nedokazuje správnost interpretace. Animace ilustruje kód, není záznamem skutečného běhu.

Skutečné běhy Codexu a Claude Code vytvořily samostatné grafy, offline HTML a animované GIFy. Nezávislé kontroly pokrývají zdroje, ovládání, topologii, balíček a dekódované snímky. [Výsledky a omezení](docs/verification.md).

Na macOS může sandbox agenta vyžadovat schválení konkrétního příkazu pro vykreslení. Složité grafy se nejlépe prohlížejí v HTML s přiblížením; video zaměřte na jednu otázku.

HTML obsahuje úryvky kódu. Soukromé výstupy ponechte soukromé. Vykreslování a exporty jsou lokální; nadále platí datová nastavení vašeho coding agenta.

## Vývoj

```sh
python3 -m unittest discover -s tests -v
uv sync --locked --extra export
python3 scripts/build_site.py
python3 scripts/package_skill.py
```

Pro testy v prohlížeči nastavte `REPO_VISUALIZER_BROWSER` na Chromium. Volitelné exportní prostředí vyžaduje Python 3.10+. [Instrukce skillu](skills/repo-visualizer/SKILL.md) · [Formát grafu](skills/repo-visualizer/references/graph-format.md) · [Exporty](skills/repo-visualizer/references/exports.md).

## Atribuce a licence

Hlavní ukázka analyzuje [openai/codex](https://github.com/openai/codex) na konkrétní revizi. Vložené úryvky zachovávají licenci Apache-2.0 a soubor NOTICE. [Zdroj a záznam ověření](examples/codex/README.md).

Inspirace: [caru-ini/stack-diagram](https://github.com/caru-ini/stack-diagram). Další ukázky zachovávají atribuci jeho MIT zdrojů na konkrétní revizi.

Původní kód: **MIT**. ELK: **EPL-2.0**, gifenc: **MIT**, Atkinson Hyperlegible Next: **OFL-1.1**. Licence a původ závislostí jsou součástí skillu. [Podrobnosti](skills/repo-visualizer/NOTICE.md).
