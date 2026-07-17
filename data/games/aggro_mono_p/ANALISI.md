# aggro_mono_p — analisi del campione (20 partite, 14-6)

Sintesi trasversale delle 20 partite giocate con `aggro_mono_p`, costruita
incrociando le `study_notes` di ogni record in questa cartella. Obiettivo:
non ripetere quello che è già scritto partita per partita, ma isolare i
pattern che si vedono **solo** guardando le partite insieme — cosa
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
| 12 | 07-15 | [やーこん](2026-07-15_kiraya-vs-yaakon.yaml) | **L** | 22 | Rosso/Bianco, G Gundam/Mobile Fighter (Domon Kasshu, Shining/Dragon Gundam, Maxter) | 0 / 1 | 13 / 8 | Nessun errore isolato di Kiraya: sconfitta pulita contro un motore di recursion (Shining Gundam) + spam di Darkness Finger (4 copie in un turno) |
| 13 | 07-16 | [big stan](2026-07-16_kiraya-vs-big-stan.yaml) | **W** | 11 | Blu/Rosso, Londo Bell (ReZEL, Gundam ST01-001, Amuro Ray, White Base) | 5 / 0 | 3 / 2 | Vittoria fulminea; turno 11 da manuale di saturazione (2 Adapt + Mikazuki nello stesso turno, poi 4 attacchi) |
| 14 | 07-16 | [Zeding](2026-07-16_kiraya-vs-zeding.yaml) | **W** | 15 | Bianco/Verde, Academy/Suletta Mercury (Chuchu's Demi Trainer, Gundam Aerial Rebuild, Gundam Pharact, Wing Gundam Bird Mode) | 5 / 2 | 7 / 5 | Turno 13 da manuale (Lupus su trash morto + Mikazuki + 3 attacchi, brucia 3 shield); il contrattacco al t14 costa 3 unità ma il margine accumulato prima regge |
| 15 | 07-17 | [IAN](2026-07-17_kiraya-vs-ian.yaml) | **W** | 17 | Viola/Bianco, precon ST05 Destiny Ignition + Aile Strike Gundam (Impulse Gundam, Force Impulse Gundam, Shinn Asuka, Minerva) | 4 / 0 | 3 / 6 | Widespread Annihilation gioca 2 volte, azzera il board di Kiraya entrambe le volte; regge solo per la ridondanza a 4 copie e nutre Lupus col trash risultante |
| 16 | 07-17 | [SSS](2026-07-17_kiraya-vs-sss.yaml) | **W** | 15 | Blu/Verde, Londo Bell (Jegan, Kayra's Re-GZ, Re-GZ BWS, Nu Gundam, Amuro Ray, Ra Cailum) + splash Strike Freedom Gundam | 4 / 0 | 8 / 7 | Prima vittoria con Strike Freedom in lista avversaria: il bounce colpisce Graze Custom (decoy economico) invece di Lupus, mai calato |
| 17 | 07-17 | [Anuy](2026-07-17_kiraya-vs-anuy.yaml) | **W** | 9 | Mono-Verde, Academy (Suletta Mercury, Guel's Dilanza, Demi Barding, Guel Jeturk/Overcoming Hardships) | 5 / 0 | 2 / 1 | Vittoria più rapida del campione: board avversario mai sviluppato, 4 shield colpite già al t7 |
| 18 | 07-17 | [SaintAbbel](2026-07-17_kiraya-vs-saintabbel.yaml) | **W** | 11 | Blu/Bianco, League Militaire (V-Dash Gundam, Victory Gundam, Zoloat, Üso Ewin, Rick Dias, Argama) | 5 / 1 | 2 / 3 | Errore isolato: t7 passato senza attaccare con Graze Custom sano contro un Rick Dias a 1 HP |
| 19 | 07-17 | [MMorelli](2026-07-17_kiraya-vs-mmorelli.yaml) | **L** | 24 | Blu/Rosso, control/removal ibrido (Gundam/Amuro Ray, Unicorn Gundam 02 Banshee, V-Dash Gundam, Darkness Finger) | 0 / 3 | 14 / 8 | Darkness Finger x2 uccide Gundam Exia Repair e ne innesca il mill casuale (Lupus perso al t6); Unicorn Gundam 02 Banshee (riciclo trash + First Strike) è lo snodo della partita al t14 |
| 20 | 07-17 | [MMorelli](2026-07-17_kiraya-vs-mmorelli-2.yaml) | **L** | 24 | Blu/Rosso, stesso mazzo control/removal (rivincita) | 1 / 0 | 17 / 11 | Prima metà pulita lato Kiraya; Unicorn Gundam 02 Banshee compare 2 volte (t16, t22) e decide la partita da sola |

**Bilancio per famiglia di mazzo avversario:**

| Archetipo avversario | Record | Partite |
|---|---|---|
| Londo Bell (Amuro/Nu Gundam/Re-GZ) | **5-0** | Tonii, Fjfnc, Pelumu, big stan, SSS |
| Neo Zeon / Sleeves | **2-0** | waxtrax, B Reichwald |
| SEED/Orb (Cosmic Era) | **1-1** | 4444 (W), 0622 (L) |
| After War Gundam X | **1-0** | Komsanw |
| Gundam 00 / Celestial Being | **1-0** | Forlun |
| Academy / Suletta Mercury | **2-0** | Zeding, Anuy |
| Destiny Ignition (Impulse/Shinn Asuka) | **1-0** | IAN |
| League Militaire | **1-1** | SaintAbbel (W), umberduel (L) |
| Control/removal ibrido (SEED/UC, MMorelli) | **0-3** | アスファルトの雑草, MMorelli x2 |
| G Gundam / Mobile Fighter | **0-1** | やーこん |

## Il dato che spiega le sei sconfitte

**Ogni singola sconfitta del campione ha in lista Strike Freedom Gundam
o Darkness Finger (o entrambe)**, verificato con un grep diretto sui log
grezzi di tutte le 20 partite, non solo sulle note scritte partita per
partita:

| Sconfitta | Strike Freedom | Darkness Finger |
|---|---|---|
| 0622 | ✅ | — |
| umberduel | ✅ | — |
| アスファルトの雑草 | ✅ | ✅ |
| やーこん | — | ✅ |
| MMorelli (1) | — | ✅ |
| MMorelli (2) | — | ✅ |

Il contrario però **non è più vero da quando SSS (partita 16) ha vinto
Kiraya con Strike Freedom Gundam in lista**: il bounce ha rimandato nel
mazzo Graze Custom (Lv.2, una carta quasi gratis) invece di una
minaccia reale, semplicemente perché **Gundam Barbatos Lupus non era
mai stato calato** quella partita e Graze Custom era l'unità di livello
più basso in campo. Questo corregge il modello: **Strike Freedom non è
pericoloso di per sé — lo è solo se Lupus (o un'altra minaccia chiave)
risulta essere l'unità di livello più basso di Kiraya in campo nel
momento in cui l'abilità si attiva** ("Choose 1 enemy Unit with the
lowest Lv."). Nelle tre sconfitte con Strike Freedom, Lupus è stato
rimbalzato nel mazzo un totale di **4 volte** (0622: 1×, umberduel: 2×,
asphalt-weed: 1×, conteggio verificato sui log grezzi) — sempre perché
era l'unica/più economica unità rimasta in campo in quel momento. Avere
sempre un'unità economica "sacrificabile" viva insieme a Lupus
disinnesca l'effetto facendolo cadere a vuoto, come visto vs SSS.
**Darkness Finger** invece è pura rimozione ripetibile da 2 danni a
basso costo, che NON sceglie per livello più basso ma colpisce quello
che vuole: da sola non tocca Lupus specificamente, ma in quantità
(asphalt-weed ne aveva 4 copie diverse osservate nel removal-package,
やーこん ne ha giocate 4 nello stesso turno, MMorelli l'ha rigiocata due
volte in due turni distinti) risponde a qualsiasi minaccia economica
del mazzo una alla volta, più in fretta di quanto Kiraya possa
svilupparne di nuove — e per questa resta una minaccia strutturale a
prescindere da cosa sia in campo. Scoperta nuova vs MMorelli:
**Gundam Exia Repair (1 HP) è il bersaglio perfetto per Darkness
Finger**, e il suo '[Destroyed] Mill 2' amplifica il danno — entrambe
le volte che è morto a Darkness Finger (t6, t10) ha scaricato nel trash
una carta viva a caso, incluso Gundam Barbatos Lupus stesso al t6 (mai
più rivisto in gioco). Contro un mazzo con rimozione ripetuta da 1-2
danni, Exia Repair passa da motore di valore a doppio svantaggio.

Il filo comune non è la carta specifica ma il tipo di risposta:
**interazione ripetibile a basso costo** (bounce o removal da 1-2
danni) contro cui il mazzo non ha contromisure strutturali. Per
Darkness Finger l'unica mitigazione è la saturazione (vedi checklist);
per Strike Freedom, a differenza di quanto pensato in precedenza,
**esiste una contromossa concreta**: non lasciare mai Lupus come
l'unità più economica del board.

La seconda causa, presente in 3 delle 4 sconfitte (manca solo in
やーこん, che vince comunque prima che serva): **assenza di un motore
di carte**. `aggro_mono_p` non ha nulla di equivalente a Overflowing
Affection / A Show of Resolve / Strike Freedom-che-pesca-a-ogni-attacco.
Contro avversari che pescano 10-15 carte extra a partita, il mazzo
finisce regolarmente a mano vuota dal turno 10 (0622, umberduel,
asphalt-weed lo notano indipendentemente, con le stesse identiche
parole: "mano vuota dal t10"). やーこん aveva comunque Overflowing
Affection (6 pescate osservate), ma qui il colpo di grazia è arrivato
per interazione diretta (Darkness Finger) più che per differenziale di
carte puro — le due cause si sommano ma non sono la stessa cosa.

## Dinamiche efficaci (confermate su più partite)

- **Isaribi-replace al posto dell'EX Base intatta** (t5-9 a seconda della
  mano): converte una difesa monouso da 3 HP in una base da 5 HP che
  pesca. Diventata linea standard dalla partita 3 in poi (Fjfnc,
  waxtrax, 4444, forlun, komsanw, pelumu) — quando manca (Tonii, 0622,
  umberduel, primi turni), la difesa regge di meno. Beneficio extra
  confermato vs SSS (t10, t12): finché è viva, una Base assorbe il
  danno da `<Breach>` al posto delle shield (regola 13-1-2-4) — Isaribi
  ha preso 3 e poi 5 danni da Breach ed è morta lei, non le shield.
- **Danno-parziale-poi-rifinitura con un corpo da 1 costo**: ping
  obbligato (Gusion Rebake, Barbatos Adapt) che ammorbidisce un bersaglio,
  poi un attaccante economico lo finisce esatto. Visto pulito in almeno
  4 partite (waxtrax t15, 4444 t15, komsanw t9, e come principio anche
  in Fjfnc t9). Zero sprechi quando eseguito bene.
- **Barbatos Lupus come chiusura**: attivazioni multiple nello stesso
  turno (fino a 3, waxtrax t15) che convertono il trash accumulato dai
  sacrifici in rimozione ripetuta o danno diretto. Il pattern che chiude
  più partite del campione — ed è anche l'unico punto debole sfruttabile
  (vedi sopra, bounce di Strike Freedom). Esempio pulito: Zeding t13,
  esiliate 3 carte già morte/nel trash (nessun valore vivo sacrificato)
  per uccidere un'unità nemica, poi il pair di Mikazuki Augus piazza
  altro danno ad area nello stesso turno.
- **Ping-prima-di-attaccare per attivare l'abilità della stessa unità**
  (non solo per finire un bersaglio): confermato anche con Gundam
  Barbatos 1st Form (pesca se danneggiato in attacco) — Zeding t9,
  Ryusei-Go lo pinga apposta prima che attacchi, pescando una carta in
  più. Costo collaterale: l'unità resta scoperta a bassa HP fino al
  turno successivo (vedi errori).
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
- **Saturazione: 2+ minacce nello stesso turno chiudono la partita**.
  Esempio più pulito: big stan t11, due Barbatos Adapt schierati nello
  stesso turno (3 ping totali con Mikazuki) seguiti da 4 attacchi in
  fila — partita finita lì su probabile resa. Stesso principio dietro
  la tripla Activate di Lupus in un turno (waxtrax t15) e la
  raccomandazione esplicita contro i mazzi control (vedi checklist).
- **Amuro Ray spreca spesso il proprio When Paired** (rest di un'unità
  nemica): in 4 partite su 4 in cui l'avversario lo ha giocato (Tonii,
  Fjfnc, Pelumu, big stan) il bersaglio era già rested dall'attacco di
  Kiraya del turno precedente — un pilota che sembra pericoloso ma il
  cui effetto è quasi sempre già "consumato" prima di attivarsi. Non è
  un'azione di Kiraya, ma utile saperlo: non è la minaccia che il nome
  suggerisce se Kiraya ha già attaccato con tutto il turno prima.

## Errori ricorrenti lato Kiraya

Elencati in ordine di frequenza osservata, con l'esempio più chiaro.
Nota preliminare: non tutte le sconfitte hanno un errore da correggere
— やーこん è stata una sconfitta pulita contro un motore avversario
(recursion + removal ripetuto) senza nessuna sequenza scorretta
individuata lato Kiraya. Vale la pena distinguere "ho giocato male" da
"l'avversario aveva in mano la risposta giusta": solo il primo caso è
azionabile con più disciplina, il secondo richiede un piano diverso
(vedi sezione successiva).

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
   standard del mazzo (di solito t4-5). Ripetuto in scala minore vs
   SaintAbbel (t7): Graze Custom sano e disponibile, Rick Dias
   dell'avversario a 1 HP residuo (kill gratis), nessun attacco
   dichiarato quel turno.
4. **Lasciare Lupus come l'unica/più economica unità in campo contro
   mazzi con Strike Freedom**. Causa diretta di tutte e tre le sconfitte
   con Strike Freedom (vedi sopra) — ma ora è una lezione più precisa e
   più risolvibile di quanto pensato: l'abilità sceglie l'unità nemica
   di **livello più basso** in campo, non la più pericolosa. Vs SSS
   (partita 16) l'effetto è caduto su Graze Custom invece che su Lupus
   proprio perché quest'ultimo non era l'unità più economica presente.
   Non serve quindi "non calare Lupus" in astratto: basta tenere in
   campo anche solo un'unità economica viva insieme a lui. Contro
   Darkness Finger/removal ripetuto (アスファルトの雑草, やーこん,
   MMorelli) non c'è un equivalente "non fare X": è un problema di
   lista avversaria, non di sequenza di gioco (vedi sotto).
5. **Attivare un buff "durante questo turno" su un'unità che non può
   comunque attaccare quel turno**. Isolato ma a costo pieno: vs
   MMorelli (t7), Isaribi (risorsa Activate una volta a turno) dà AP+2
   a Sword Impulse Gundam appena schierato nello stesso turno — un'unità
   non-Link non può attaccare al turno del proprio dispiegamento, quindi
   il buff scade inutilizzato e l'unità muore al turno successivo senza
   averlo mai sfruttato. Controllo semplice da fare prima di ogni
   Activate: l'unità bersaglio può *effettivamente* attaccare questo
   turno?

## Problematiche strutturali del mazzo (non correggibili col solo gioco)

- **Nessun motore di pesca/vantaggio carte.** Il mazzo compete sulla
  velocità pura; quando la corsa si allunga oltre il t10 (removal,
  stallo, doppio blocco) resta sistematicamente a corto di risorse
  mentre l'avversario continua a pescare. Presente in 3 sconfitte su 5
  (0622, umberduel, asphalt-weed) — やーこん e MMorelli perdono per
  interazione diretta/mill piuttosto che per differenziale di pesca
  puro, anche se MMorelli mostra una variante dello stesso problema
  (vedi sotto).
- **Nessuna risposta a interazione ripetibile a basso costo** (bounce
  tipo Strike Freedom, removal da 1-2 danni tipo Darkness Finger): è la
  causa singola più consistente delle sconfitte (5 su 5, vedi sopra). Il
  mazzo non ha counterplay strutturale — solo mitigazione tattica
  (saturare, non esporre Lupus, ridurre il self-ping).
- **Gundam Exia Repair è una liability contro removal ripetuto a basso
  costo.** Il suo 1 HP lo rende un bersaglio perfetto per una rimozione
  da 2 danni come Darkness Finger, e il suo '[Destroyed] Mill 2' allora
  si ritorce contro: ogni volta che muore così, scarica nel trash 2
  carte a caso del proprio mazzo, a volte carte vive di valore (Gundam
  Barbatos Lupus stesso, vs MMorelli t6). Contro questi mazzi il suo
  valore normale (pesca/riciclo) si trasforma in un moltiplicatore di
  svantaggio ogni volta che viene rimosso.
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
- **Zero risposta a Unicorn Gundam 02 Banshee (Destroy Mode).** Rimescola
  carte dal proprio trash nel mazzo, ottiene First Strike (colpisce per
  primo) e quindi uccide senza subire contraccolpo, poi in un secondo
  attacco nello stesso turno abbatte anche una base — vista decidere da
  sola entrambe le partite contro MMorelli (t14/t16 nella prima, t16 e
  di nuovo t22 nella seconda). Il mazzo non ha modo di romperle il First
  Strike né di evitare il danno: l'unica risposta vista funzionare è
  ucciderla in combattimento quando è già in campo (visto riuscire al
  t15 e al t21 della seconda partita vs MMorelli), non prevenire
  l'attacco in primo luogo.
- **Zero risposta a un board wipe generico** (tipo Widespread
  Annihilation, "distruggi tutte le unità Lv.4 o inferiore" — quasi
  ogni unità del mazzo rientra in quella soglia). Vista due volte nella
  stessa partita (IAN, t10 e t16): il mazzo l'ha retta solo grazie alla
  ridondanza a 4 copie quasi ovunque, non per una contromossa reale.
  Con un avversario meno generoso di risorse o un secondo wipe più
  tempestivo, lo stesso schema potrebbe non reggere.

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
   qualunque bounce che rimanda l'unità di livello più basso)**: la
   difesa non è "non calare Lupus", è **non lasciarlo come l'unità più
   economica in campo**. Prima di attaccare/passare con Lupus in gioco,
   controlla se hai anche un'unità a basso costo viva insieme a lui (un
   Graze Custom, un Ryusei-Go già scoperto) che farebbe da bersaglio
   "gratis" per il bounce al posto suo. Se il board è solo Lupus,
   valuta se aspettare un turno o schierare qualcos'altro prima di
   impegnarlo. Se non sai ancora se l'avversario ha Strike Freedom,
   aspetta un segnale (un Kira Yamato in campo, uno scarto sospetto) prima
   di impegnarlo.
6. **Contro mazzi che sembrano removal/control (tante Action/Command da
   1-2 costo, poca board avversaria — es. Darkness Finger, Close Combat,
   Battle of Aces)**: riduci il self-ping al minimo e punta a saturare —
   calare 2-3 minacce nello stesso turno invece di una alla volta, così
   almeno una sopravvive e colpisce. Contro questi mazzi non esiste una
   singola giocata che "risolve" il matchup: l'obiettivo è chiudere
   prima che accumulino abbastanza copie per rispondere a tutto.
7. **Isaribi-replace resta la giocata di default nei primi turni** quando
   disponibile: non aspettare che l'EX Base venga distrutta, sostituiscila
   appena hai 1 risorsa libera.
8. **Se il tuo turno lascia 2+ unità sane in campo che possono attaccare,
   fallo con tutte** — anche solo per portare via il pilota-rest
   dell'avversario (Amuro Ray e simili) o costringerlo a decisioni. Le
   partite più nette (b-reichwald, big stan) condividono proprio questo:
   nessuna unità sana lasciata inattiva a fine turno.
9. **Contro un board wipe generico (es. Widespread Annihilation)**: non
   c'è modo di prevenirlo, ma il mazzo lo assorbe bene grazie alle 4
   copie — non esitare a schierare tutto anche se "rischioso", e usa il
   trash che ne risulta come carburante immediato per Lupus nel turno
   successivo (visto funzionare due volte nella partita vs IAN).
10. **Prima di ogni Activate "durante questo turno" (Isaribi e simili)**:
    l'unità bersaglio può davvero attaccare questo turno? Un'unità
    appena schierata (non-Link) non può farlo — sprecare il buff su di
    lei equivale a non averla usata affatto (vs MMorelli t7).
11. **Contro mazzi con removal ripetuto a basso costo (Darkness Finger e
    simili)**: valuta se calare Gundam Exia Repair vale il rischio — il
    suo 1 HP e il suo Mill 2 alla morte possono trasformarsi in un
    doppio svantaggio (carta persa + una seconda carta a caso scartata
    dal mazzo, a volte Lupus stesso).
