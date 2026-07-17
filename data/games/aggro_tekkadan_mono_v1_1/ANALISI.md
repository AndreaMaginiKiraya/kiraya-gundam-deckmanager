# aggro_tekkadan_mono_v1_1 — analisi del campione (2 partite, 0-2)

Sintesi trasversale delle partite giocate con `aggro_tekkadan_mono_v1_1`,
la prima iterazione derivata da `aggro_mono_p` (vedi
`data/games/aggro_mono_p/ANALISI.md` per l'analisi delle 20 partite del
mazzo precedente — i pattern strutturali di quel mazzo restano il
riferimento finché questo campione non è abbastanza grande da confermarli
o smentirli per conto proprio). Cambi rispetto ad `aggro_mono_p`: Gundam
Gusion Rebake 4→3, Shiden Custom (Ryusei-Go) 2→3, Gundam Barbatos Lupus
3→4, Sword Impulse Gundam e Akihiro Altland rimossi, Become a Shield 1→2,
aggiunti Gundam Barbatos Lupus Rex (GD05-051, x1) e Gundam Barbatos 5th
Form Ground Type (GD03-066, x1 — zona Earth-only, da testare con
attenzione).

Con **2 sole partite** è troppo presto per isolare pattern affidabili;
questa sezione andrà riscritta man mano che il campione cresce, sul
modello di `aggro_mono_p/ANALISI.md`.

Nota sul conteggio unità perse: dall'introduzione delle casualties
`inferred: true` (kill da ping multi-target che il client non logga mai
come distruzioni), i totali includono anche quelle — i record di
`aggro_mono_p` sono stati generati col parser precedente e le
sottocontano.

## Tabella partite

| # | Data | Avversario | Esito | Turni | Mazzo avversario | Shield rimaste (K / avv) | Unità perse (K / avv) | Nota chiave |
|---|------|-----------|-------|-------|-------------------|------------------------|------------------------|-------------|
| 1 | 07-17 | [loklee](2026-07-17_kiraya-vs-loklee.yaml) | **L** | 20 | Verde/Viola, Zeon (Char's Zaku Ⅱ, Zeong, Sazabi, Rezin's/Quess's Jagd Doga) | 0 / 3 | 13 / 17 | Partita punto a punto persa sull'ultima shield; Sazabi (GD05-052) fa 1-per-3 col suo mill-and-recur, Isaribi muore 3 volte e apre finestre Breach ripetute |
| 2 | 07-17 | [sgd](2026-07-17_kiraya-vs-sgd.yaml) | **L** | 13 | Blu/Rosso, Earth Alliance/Phantom Pain (Chaos/Gaia/Raider Gundam, Sting Oakley, Stellar Loussier) + splash OZ (Tallgeese, Corsica Base) | 0 / 4 | 6 / 4 | Persa nei primi 4 turni: doppio mulligan, primo deploy solo al t4 e ucciso subito da Close Combat; Chaos Gundam + Sting = High-Maneuver a ogni attacco, Lupus mai pescato |

## Prime osservazioni (da confermare su più partite)

- **I due Exia Repair aprono bene** (t5-7): uccidono l'EX Base e poi
  tradano 1-per-1 col proprio mill-on-death, come da manuale — nessun
  problema di curva visto in questa partita, coerente con l'argomento
  del mazzo per tenerli in lista.
- **Barbatos Lupus doppia-attivazione (t13) chiude in fretta ma esaurisce
  il trash**: 6 carte esiliate in un turno hanno ucciso Zeong subito, ma
  da lì in poi Lupus è rimasto un 5/5 vanilla per il resto della
  partita — un solo turno di burst, poi nessun carburante residuo per
  ripeterlo. Da verificare se è un problema strutturale di v1_1 (più
  copie di Lupus/Lupus Rex competono per lo stesso trash) o solo
  variance di questa mano.
- **Isaribi come unica base resta un collo di bottiglia**: morta 3 volte
  (t6, t14, t18), ogni sostituzione riapre una finestra Breach fresca
  all'avversario — stesso problema strutturale già annotato per
  `aggro_mono_p` (nessuna seconda base su cui alternare).
- **Gundam Barbatos Lupus Rex e Gundam Barbatos 5th Form (Ground Type)
  non sono ancora apparsi in mano** in nessuna delle due partite: zero
  dati sui due pezzi nuovi di v1_1. Vs sgd non è stato pescato nemmeno
  Lupus base — l'intero piano-finisher è rimasto nel mazzo mentre la
  partita si decideva sul tempo.
- **Il buco strutturale sul block-bypass si ripresenta identico** (già
  in `aggro_mono_p/ANALISI.md`): Chaos Gundam + Sting Oakley linkato
  guadagna High-Maneuver a ogni attacco ("Can't block High-maneuver" t5
  e t7 vs sgd) e ha ucciso EX Base + 2 shield senza contromossa
  possibile. Stessa famiglia di Wing Zero e del When-Paired di Nu
  Gundam LR.
- **La sconfitta vs sgd non è del mazzo ma della mano**: doppio
  mulligan, nessun deploy fino al t4, e il primo corpo (1st Form)
  rimosso da Close Combat in end phase prima di poter fare qualsiasi
  cosa. I trade da metà partita in poi erano alla pari — il buco dei
  primi 4 turni no.

## Checklist provvisoria

Ereditata da `aggro_mono_p` finché non emergono differenze specifiche
per v1_1:

1. Isaribi-replace resta la giocata di default appena disponibile.
2. Self-ping solo su unità che ne beneficiano (1st Form pesca, 2nd Form
   AP+2), mai su un'unità sana che sta per attaccare.
3. Non lasciare Lupus/Lupus Rex come unica unità economica in campo
   contro mazzi con bounce di tipo Strike Freedom.
4. Contro motori di recursion/mill avversari (Sazabi e simili): valutare
   se vale la pena rimuoverli appena schierati, prima che il loro Deploy
   generi vantaggio-carte irreversibile.