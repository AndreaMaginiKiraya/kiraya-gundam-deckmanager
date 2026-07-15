# aggro_mono_p — analisi del campione (11 partite, 8-3)

Sintesi trasversale delle 11 partite giocate con `aggro_mono_p`, costruita
incrociando le `study_notes` di ogni record in questa cartella. Obiettivo:
non ripetere quello che è già scritto partita per partita, ma isolare i
pattern che si vedono **solo** guardando le 11 partite insieme — cosa
funziona sempre, cosa va storto sempre, contro cosa il mazzo fatica
strutturalmente. Ultima sezione = checklist pratica per le prossime partite.

Rigenerare/estendere: quando importi una nuova partita con
`import_game_log`, aggiungi una riga alla tabella e rileggi questo file
per vedere se conferma o smentisce i pattern sotto.

## Tabella partite

| # | Data | Avversario | Esito | Turni | Mazzo avversario | Shield rimaste (K / avv) | Unità perse (K / avv) | Nota chiave |
|---|------|-----------|-------|-------|-------------------|------------------------|------------------------|-------------|
| 1 | 07-14 | [Tonii](2026-07-14_kiraya-vs-tonii.yaml) | **W** | 26 | Blu/Verde, Londo Bell (Nu Gundam, Amuro, Guntank) | 1 / 0 | 14 / 8 | Corsa alle shield vinta nettamente; Lupus chiude col trash accumulato dai sacrifici |
| 2 | 07-14 | [0622](2026-07-14_kiraya-vs-0622.yaml) | **L** | 24 | Blu/Bianco SEED (Strike Freedom, Kira Yamato) | 0 / 0 | 12 / 10 | Persa ai punti: card advantage avversario (~15 carte extra) + bounce di Strike Freedom su Lupus |
| 3 | 07-14 | [Fjfnc](2026-07-14_kiraya-vs-fjfnc.yaml) | **W** | 22 | Blu/Verde, Londo Bell + Wing Zero | 1 / 1 | 10 / 7 | Isaribi-replace debutta come linea standard; Wing Zero (High-Maneuver) unico vero problema tecnico |
| 4 | 07-14 | [waxtrax](2026-07-14_kiraya-vs-waxtrax.yaml) | **W** (abbandono) | 21 | Rosso, Neo Zeon (Kshatriya, Sazabi, Jagd Doga) | 3 / 0 | 6 / 9 | Miglior partita sul piano del danno puro; tripla Activate di Lupus in un turno |
| 5 | 07-14 | [umberduel](2026-07-14_kiraya-vs-umberduel.yaml) | **L** | 17 | Blu/Rosso, League Militaire + splash Strike Freedom | 0 / 3 | 9 / 6 | Zero shield rotte in 17 turni; V2 Gundam (doppio attacco/turno) + bounce di Strike Freedom su Lupus |
| 6 | 07-15 | [アスファルトの雑草](2026-07-15_kiraya-vs-asphalt-weed.yaml) | **L** | 25 | Blu/Rosso, control/removal (Banshee, Strike Freedom, Strike Rouge) | 0 / 2 | 17 / 1 | Sconfitta peggiore: removal da 1-2 costi in end phase + self-ping che alimenta il loro removal condizionale |
| 7 | 07-15 | [4444](2026-07-15_kiraya-vs-4444.yaml) | **W** | 18 | Blu/Bianco, SEED/Orb (Archangel, Strike Rouge, Freedom, Akatsuki) | 4 / 1 | 9 / 6 | Prima partita con errori isolati e nominati (self-ping su sé stesso, attacco prima di un ping-finisher gratis) |
| 8 | 07-15 | [B Reichwald](2026-07-15_kiraya-vs-b-reichwald.yaml) | **W** | 10 | Bianco/Viola, Neo Zeon (Rick Dias, Axis, Sazabi) | 6 / 0 | 2 / 2 | La più lopsided: 0 shield perse, board avversario mai sviluppato |
| 9 | 07-15 | [Komsanw](2026-07-15_kiraya-vs-komsanw.yaml) | **W** | 18 | Bianco/Viola, After War Gundam X (Airmaster, Leopard Destroy, Gundam DX) | 3 / 1 | 6 / 6 | Trade quasi simmetrici; le lezioni della partita 7 (no self-ping sprecato, ping-prima-di-attaccare) applicate senza errori |
| 10 | 07-15 | [Pelumu](2026-07-15_kiraya-vs-pelumu.yaml) | **W** | 13 | Verde, Londo Bell (Nu Gundam entrambe le stampe, Amuro, Re-GZ) | 0 / 0 | 7 / 3 | Vinta sulla velocità nonostante 7 unità perse contro 3, ed entrambi a 0 shield: race pericolosamente in parità |
| 11 | 07-15 | [Forlun](2026-07-15_kiraya-vs-forlun.yaml) | **W** | 14 | Viola/Rosso, Gundam 00/Celestial Being (Virtue, Kyrios, GN Armor) | 5 / 0 | 7 / 3 | 0 shield perse nonostante più unità perse: l'avversario non ha mai attaccato il player, solo i corpi |

**Bilancio per famiglia di mazzo avversario:**

| Archetipo avversario | Record | Partite |
|---|---|---|
| Londo Bell (Amuro/Nu Gundam/Re-GZ) | **3-0** | Tonii, Fjfnc, Pelumu |
| Neo Zeon / Sleeves | **2-0** | waxtrax, B Reichwald |
| SEED/Orb (Cosmic Era) | **1-1** | 4444 (W), 0622 (L) |
| After War Gundam X | **1-0** | Komsanw |
| Gundam 00 / Celestial Being | **1-0** | Forlun |
| League Militaire | **0-1** | umberduel |
| Control/removal ibrido | **0-1** | アスファルトの雑草 |

## Il dato che spiega le tre sconfitte

**Strike Freedom Gundam è presente in tutte e tre le sconfitte** (0622,
umberduel, アスファルトの雑草) e in nessuna delle otto vittorie. Non è
una coincidenza isolata: il suo bounce ("scarta 2, rimanda un'unità
nemica nel mazzo — quella di livello più basso") è l'unica carta vista
nel campione capace di annullare **Gundam Barbatos Lupus** senza
combatterlo e senza alimentare né trash né esili — la sua controparte
offensiva. Nelle tre sconfitte Lupus è stato rimbalzato nel mazzo un
totale di **4 volte** (0622: 1×, umberduel: 2×, asphalt-weed: 1×,
verificato riga per riga sui log grezzi), sempre azzerando in un colpo
solo il piano B del mazzo in un momento chiave della partita.

La seconda causa comune alle stesse tre sconfitte: **assenza di un
motore di carte**. `aggro_mono_p` non ha nulla di equivalente a
Overflowing Affection / A Show of Resolve / Strike Freedom-che-pesca-a-
ogni-attacco. Contro avversari che pescano 10-15 carte extra a partita,
il mazzo finisce regolarmente a mano vuota dal turno 10 (0622, umberduel,
asphalt-weed lo notano indipendentemente, con le stesse identiche
parole: "mano vuota dal t10").

## Dinamiche efficaci (confermate su più partite)

- **Isaribi-replace al posto dell'EX Base intatta** (t5-9 a seconda della
  mano): converte una difesa monouso da 3 HP in una base da 5 HP che
  pesca. Diventata linea standard dalla partita 3 in poi (Fjfnc,
  waxtrax, 4444, forlun, komsanw, pelumu) — quando manca (Tonii, 0622,
  umberduel, primi turni), la difesa regge di meno.
- **Danno-parziale-poi-rifinitura con un corpo da 1 costo**: ping
  obbligato (Gusion Rebake, Barbatos Adapt) che ammorbidisce un bersaglio,
  poi un attaccante economico lo finisce esatto. Visto pulito in almeno
  4 partite (waxtrax t15, 4444 t15, komsanw t9, e come principio anche
  in Fjfnc t9). Zero sprechi quando eseguito bene.
- **Barbatos Lupus come chiusura**: attivazioni multiple nello stesso
  turno (fino a 3, waxtrax t15) che convertono il trash accumulato dai
  sacrifici in rimozione ripetuta o danno diretto. Il pattern che chiude
  più partite del campione — ed è anche l'unico punto debole sfruttabile
  (vedi sopra, bounce di Strike Freedom).
- **Prioritizzazione dei blocchi sotto doppio attacco**: quando arrivano
  due minacce nello stesso turno con un solo blocker disponibile, salvare
  l'unità che morirebbe sicura (HP basso) e sacrificare quella che ha già
  reso valore o che comunque sopravvivrebbe peggio. Eseguito bene in 4444
  (t12) e komsanw (t12-13, t16) — nessun errore di questo tipo nelle
  ultime partite.
- **Ping-prima-di-attaccare quando un kill gratis è disponibile**: se un
  pair/ping automatico può già finire un bersaglio in kill-range, va
  giocato PRIMA di rischiare un'unità in combattimento per lo stesso
  kill. Violato una volta (4444 t17), poi mai più ripetuto — segno che è
  un'abitudine correggibile, non un limite del mazzo.

## Errori ricorrenti lato Kiraya

Elencati in ordine di frequenza osservata, con l'esempio più chiaro:

1. **Self-ping sprecato su se stessi invece che su un'unità che ne
   beneficia** (1st Form pesca se danneggiato, 2nd Form ottiene AP+2).
   Esempio più netto: 4444 t7, Ryusei-Go pinga se stesso e resta a 1 HP
   per il resto della partita, morendo per niente al t9. Corretto nella
   stessa partita al t17 (ping su 1st Form) e mai più ripetuto nelle
   partite successive (komsanw, forlun, pelumu) — è il singolo errore più
   comune ma anche il più risolto.
2. **Attaccare un bersaglio non urgente invece del player**. Se
   un'unità nemica è già rested e non può colpire di nuovo prima del
   prossimo turno dell'avversario, non c'è fretta di rimuoverla — meglio
   colpire le shield. Violato in pelumu (t9, Exia Repair contro Re-GZ BWS
   già "innocuo" per un turno) e strutturalmente in umberduel/asphalt-weed
   dove *tutta* la pressione è finita su basi/corpi invece che sul player.
3. **Passare un turno intero senza attaccare con unità sane e attive
   contro un board avversario esposto**. Isolato ma costoso: pelumu t5
   (Exia Repair + Graze Custom entrambi disponibili, board di Pelumu
   completamente rested, zero attacchi dichiarati) — il primo vero
   attacco della partita è arrivato solo al t7, molto tardi per lo
   standard del mazzo (di solito t4-5).
4. **Esporre Lupus troppo presto contro mazzi con Strike Freedom**,
   invece di calarlo solo nel turno in cui le sue attivazioni chiudono
   qualcosa di concreto. Causa diretta di tutte e tre le sconfitte (vedi
   sopra) — è la lezione più importante e ancora la meno "risolta" delle
   quattro, perché dipende dal leggere in anticipo se l'avversario ha
   Strike Freedom in lista, non solo dall'esecuzione nel turno.

## Problematiche strutturali del mazzo (non correggibili col solo gioco)

- **Nessun motore di pesca/vantaggio carte.** Il mazzo compete sulla
  velocità pura; quando la corsa si allunga oltre il t10 (removal,
  stallo, doppio blocco) resta sistematicamente a corto di risorse
  mentre l'avversario continua a pescare. Le tre sconfitte lo confermano
  tutte.
- **Il self-ping è un'arma a doppio taglio contro il removal
  condizionale.** Diverse rimozioni osservate colpiscono solo unità
  *danneggiate* (es. Battle of Aces nell'archetipo control di
  アスファルトの雑草): il motore stesso del mazzo (auto-danneggiarsi per
  attivare sinergie) rende ogni corpo un bersaglio legale del loro
  removal migliore. Contro questi mazzi il ping va riservato al minimo
  indispensabile, mai automatico.
- **Zero risposta a High-Maneuver / bypass del blocco.** Wing Gundam
  Zero (Fjfnc) e il When Paired di Nu Gundam LR (Pelumu) ignorano
  completamente la possibilità di bloccare. Il mazzo non ha strumenti
  reattivi per questo — l'unica contromossa vista funzionare è arrivare
  prima (correre più veloce) o rimuovere la minaccia preventivamente.
- **Nessun piano C quando il piano A (corsa) si spegne e il piano B
  (Lupus) viene neutralizzato.** Lo dice esplicitamente la nota della
  partita vs umberduel: quando entrambi falliscono, la partita è persa
  strutturalmente, non per una singola giocata sbagliabile diversamente.

## Checklist pratica per le prossime partite

Punti azionabili, in ordine di impatto atteso sul win-rate:

1. **Prima di ogni deploy con self-ping opzionale**: c'è un'unità in
   gioco che *beneficia* dall'essere danneggiata (1st Form: pesca
   all'attacco; 2nd Form: AP+2)? Se sì, il ping va lì, mai su un'unità
   che sta per attaccare o che vuoi tenere sana.
2. **Prima di dichiarare un attacco contro un'unità nemica (non contro
   il player)**: quell'unità può colpire di nuovo prima del tuo prossimo
   turno? Se è rested e non minaccia nulla nell'immediato, preferisci
   colpire le shield — puoi sempre finirla dopo con un ping gratuito.
3. **Prima di attaccare un bersaglio già in kill-range**: hai un
   pair/ping disponibile che lo finisce da solo? Giocalo PRIMA
   dell'attacco, non dopo — un kill gratis non vale un'unità sacrificata
   per lo stesso risultato.
4. **A ogni tuo turno, controlla se hai unità sane e attive che non
   stanno attaccando.** Se il board avversario è rested/esposto, non c'è
   motivo di passare senza attaccare — è l'errore isolato più costoso
   visto nel campione (pelumu t5).
5. **Contro un avversario Blu che gioca Strike Freedom Gundam (o
   qualunque bounce che rimanda unità di livello basso), NON calare
   Lupus in anticipo.** Tienilo in mano finché non puoi attivarlo per
   chiudere la partita nello stesso turno o nel giro immediatamente
   successivo. Se non sai ancora se l'avversario ha Strike Freedom,
   aspetta un segnale (un Kira Yamato in campo, uno scarto sospetto) prima
   di impegnarlo.
6. **Contro mazzi che sembrano removal/control (tante Action da 1-2
   costo, poca board avversaria)**: riduci il self-ping al minimo e punta
   a saturare — calare 2-3 minacce nello stesso turno invece di una alla
   volta, così almeno una sopravvive e colpisce.
7. **Isaribi-replace resta la giocata di default nei primi turni** quando
   disponibile: non aspettare che l'EX Base venga distrutta, sostituiscila
   appena hai 1 risorsa libera.
