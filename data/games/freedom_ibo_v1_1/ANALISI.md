# freedom_ibo_v1_1 — analisi del campione (17 partite, 12-5)

Sintesi delle partite giocate con `freedom_ibo_v1_1`, l'archetipo Freedom/IBO
(Blue/Purple, Tekkadan + Strike Freedom Gundam/Kira Yamato) adottato dopo il
pivot da `aggro_tekkadan_mono` — la ricerca su questa sessione aveva
quantificato il vecchio archetipo MF/G-Gundam al 37,5% (3-5) e mostrato che
il "meta imbattibile" lamentato da Kiraya era in realtà specifico contro
Strike Freedom Gundam (41%, campione più grande) e MF, non contro il campo
in generale. `freedom_ibo_v1_1` è la seconda iterazione, derivata da
`freedom_ibo` (lista MetaSheep trascritta) rimuovendo il motore Impulse
Gundam (Impulse/Force Impulse/Blast Impulse, Fatal Strike, Zoloat) in favore
di più corpi Tekkadan: 2 Gundam Exia Repair, 4 Graze Custom, 2 M1 Astray
Shrike, 4 Gundam Barbatos 1st Form, 4 Hyakuren, 4 Gundam Barbatos Adapt, 3
Strike Rouge (Ootori), 4 Gundam Gusion Rebake, 1 Gundam Flauros (Ryusei-Go),
3 Gundam Barbatos Lupus, 3 Strike Freedom Gundam, 4 Mikazuki Augus, 4 Kira
Yamato, 2 A Show of Resolve, 2 Widespread Annihilation, 4 Axis.

Con **17 partite** il campione resta piccolo — questa sezione andrà
riscritta man mano che cresce, sullo stesso modello di
`aggro_tekkadan_mono_v1_1/ANALISI.md`.

Nota sul conteggio unità perse: include le casualties `unattributed` (kill
simultanei da effetti multi-target come Widespread Annihilation, dove non è
sempre chiaro a chi extra-attribuire ogni singola unità nel parser).

## Tabella partite

| # | Avversario | Esito | Turni | Mazzo avversario | Shield rimaste (K / avv) | Unità perse (K / avv + non attr.) | Nota chiave |
|---|-----------|-------|-------|-------------------|--------------------------|-------------------------------------|-------------|
| 1 | [bluebob](2026-08-10_kiraya-vs-bluebob.yaml) | **W** | 22 | Verde/Viola, Neo Zeon (Sazabi, Zeong + token Wire-Guided Arm/Head, Char Aznable, Zaku Ⅱ, Quess's Jagd Doga, Rick Dom, Giant Killing) | 1 / 0 | 7 / 7 + 7 | Giant Killing rimuove entrambi i Blocker uno alla volta (t11) — la ridondanza di copie non aiuta contro rimozione mirata single-target; Widespread Annihilation 3-per-0 col campo proprio vuoto (t16), il caso ideale |
| 2 | [Roy Taric](2026-08-10_kiraya-vs-roytaric.yaml) | **W** | 15 | Blu/Rosso, SEED misto (Gundam ST01-001 + Amuro Ray, Aegis Gundam MA Mode + Athrun Zala, Gundam Virsago, Vesalius) | 1 / 4 | 8 / 3 | Widespread Annihilation di nuovo 3-per-0 (t10), terza partita di fila con questo risultato; l'avversario si arrende con board completamente vuoto pur avendo perso una sola shield in tutta la partita - il board conta più della corsa alle shield |
| 3 | [Rei03](2026-08-10_kiraya-vs-rei03.yaml) | **W** | 20 | Blu/Bianco, toolbox SEED/Orb (Aile Strike Gundam, Akatsuki Oowashi, Andrew Waldfeld, Archangel, Argama, Buster Gundam, Waldfeld's Murasame, Rick Dias, Strike Freedom Gundam, Kira's Strike Rouge) | 1 / 0 | 7 / 9 | Mill di Exia Repair costa un'intera copia di Strike Freedom Gundam (t7); Waldfeld's Murasame si autocura via Andrew Waldfeld e resiste ai ping parziali, serve una doppia attivazione dedicata di Lupus per finirla (t16); Widespread Annihilation chiude una partita lunga ed equilibrata (t20) |
| 4 | [Vash](2026-08-10_kiraya-vs-vash.yaml) | **W** | 26 | Blu/Rosso, rimozione diretta pesante (Close Combat, Darkness Finger, Improved Technique, Overwhelming Pressure) + Kshatriya/Marida Cruz + Unicorn Gundam 02 Banshee (Destroy Mode) + Kira's Strike Rouge | 2 / 0 | 14 / 5 | Partita più lunga del campione; Unicorn Gundam 02 Banshee (Destroy Mode) uccide Strike Freedom Gundam senza subire danno (t22) - "la cosa più spaventosa che gioca Vash"; Lupus risponde subito bruciando persino una propria copia duplicata come carburante (t23); vinta per logoramento, non per un singolo colpo decisivo |
| 5 | [ZimZam](2026-08-10_kiraya-vs-zimzam.yaml) | **L** | 15 | Blu/Bianco, League Militaire (Aile Strike Gundam + Kira Yamato, Victory Gundam, Gundam Lfrith, Zoloat, Gun EZ, Silver Bullet, Reineforce Jr./token Parts, Üso Ewin) | 0 / 5 | 9 / 5 | **Unico errore tattico chiaramente auto-individuato del campione** (t12): Barbatos Adapt attacca Gundam Lfrith per puro chip non-letale invece di spingere su una shield - non ottiene nulla, resta a 1 HP e muore gratis a un token Parts il turno dopo; Aile Strike Gundam colpisce il player senza risposta dal t9 all'11, decidendo la corsa alle shield (0 contro 5) |
| 6 | [Lamka](2026-08-10_kiraya-vs-lamka.yaml) | **W** | 18 | Rosso/Bianco, **shell MF/G Gundam completa** (Master Gundam + Master Asia, Shining Gundam + Domon Kasshu, Haow Gundam, Gundam Maxter, Darkness Finger, Cyclone Punch/Chibodee Crocket, Graviton Hammer/Argo Gulskii) | 0 / 3 | 12 / 5 | **Prima vittoria diretta contro un mazzo MF/G-Gundam completo con questo archetipo** - la motivazione originale del pivot da `aggro_tekkadan_mono` (37,5% di winrate contro questa famiglia); partenza dura (doppio Darkness Finger 2-per-1, t6), poi il debutto di Strike Freedom Gundam genera 3 carte in una sola sequenza (t15) |
| 7 | [Marcos sim](2026-08-10_kiraya-vs-marcossim.yaml) | **L** | 27 | Viola/Bianco, Minerva Squad/Destiny (Destiny Gundam, famiglia Impulse Gundam, Shinn Asuka, Aile Strike Gundam, Kira Yamato ST04-010, Noin's Taurus, Graceful Demeanor, Widespread Annihilation propria) | 1 / 1 | 7 / 7 + 4 | **Destiny Gundam è strutturalmente imbloccabile e si autorigenera dal trash pagandone il costo all'infinito** - il problema è di matchup, non di sequenza di gioco (t15); la Widespread Annihilation avversaria spazza il campo di Kiraya 3-per-0 subito dopo che Destiny aveva già tradato Lupus (t21); due turni completamente bianchi (0 azioni, t22) da mani sfortunate, ma l'imbloccabilità di Destiny avrebbe reso inutili anche pescate normali |
| 8 | [Komadori](2026-08-10_kiraya-vs-komadori.yaml) | **L** | 19 | Blu/Bianco, stesso toolbox SEED/Orb di Rei03 (Aile Strike Gundam, doppio Akatsuki Oowashi, Andrew Waldfeld, Archangel, Argama, Javelin, Rick Dias, Kira's Strike Rouge, Waldfeld's Murasame) | 0 / 1 | 9 / 5 | Widespread Annihilation scartata come costo dell'abilità di Strike Freedom Gundam senza mai risolvere il proprio effetto, **due volte nella stessa partita** (t14, t17); due bounce simmetrici di Strike Freedom Gundam nemico colpiscono i due investimenti più grossi di Kiraya - più sfortuna di sequenza che un errore individuabile |
| 9 | [Direshift](2026-08-10_kiraya-vs-direshift.yaml) | **W** | 33 | Blu/Bianco, League Militaire (V-Dash Gundam + Üso Ewin, Zoloat, Victory Gundam in due stampe, Freedom Gundam, Strike Rouge Ootori, Kira Yamato in due stampe) | 0 / 0 | 19 / 14 + 3 | "Vinta per il rotto della cuffia" non regge del tutto alla revisione: l'avversario è senza shield dal t27, sei turni prima della fine effettiva - la lunghezza viene da stalli di board e due Unforeseen Incident, non da un finale davvero in bilico |
| 10 | [clairfryer](2026-08-10_kiraya-vs-clairfryer.yaml) | **W** | 42 | Blu/Rosso, rimozione pesante (Improved Technique, Close Combat, Darkness Finger) + Unicorn Gundam 02 Banshee (Destroy Mode) + doppio Strike Freedom Gundam | 0 / 0 | 20 / 3 + 9 | Partita più lunga e più equilibrata del campione, vinta per esaurimento del mazzo shield dopo aver spento il motore di rigenerazione scudi avversario (Mining Asteroid Palau, t36); Barbatos Lupus fa da vero motore di recupero contro un avversario che vinceva quasi ogni scambio di rimozione diretta |
| 11 | [Chong](2026-08-10_kiraya-vs-chong.yaml) | **W** | 19 | Blu/Verde, Gundam + Amuro Ray (beater AP6/HP6 auto-curante) + famiglia Nu Gundam | 0 / 3 | 8 / 10 | Partita di logoramento vera, non stravinta: Widespread Annihilation persa a uno scudo senza mai essere lanciata (t13), il rifornimento scudi di Kiraya si esaurisce al t16 - coerente con la sensazione "zero carte in mano" della vittoria |
| 12 | [pylon](2026-08-10_kiraya-vs-pylon.yaml) | **L** | 17 | Blu/Verde, stesso archetipo Gundam+Amuro Ray/Nu Gundam di Chong | 0 / 2 | 7 / 7 + 1 | **Nessun errore tattico individuato dopo revisione richiesta da Kiraya**: il turno decisivo (t9) è semplicemente un'ottima sequenza avversaria; corretta a posteriori una falsa affermazione ("il mazzo non ha Blocker") - Gundam Gusion Rebake e Strike Rouge (Ootori) sono entrambi Blocker regolari, semplicemente morti presto in questa partita specifica |
| 13 | [Belele](2026-08-10_kiraya-vs-belele.yaml) | **W** | 14 | Viola mono, mirror parziale Tekkadan (Barbatos 1st Form, Barbatos Adapt, Gundam Gusion Rebake, Widespread Annihilation propria) | 5 / 0 | 1 / 1 + 6 | Vittoria schiacciante, 0 shield perse; la Widespread Annihilation dell'avversario finisce scartata da uno scudo prima di poter fare qualcosa |
| 14 | [Bench](2026-08-10_kiraya-vs-bench.yaml) | **W** | 16 | Blu/Bianco, SEED/Orb (Strike Rouge Ootori, Kira's Strike Rouge + Kira Yamato, Aile Strike Gundam, Amuro Ray ST01-010) | 4 / 3 | 2 / 2 + 1 | Widespread Annihilation al t12 (3-per-1 reale) è lo snodo della partita; avversario mai più ripreso, resa al t16 con entrambi gli Strike Freedom Gundam a 1 HP in uno scambio a specchio |
| 15 | [daedaedaes](2026-08-10_kiraya-vs-daedaedaes.yaml) | **L** | 17 | Blu/Bianco, SEED/Orb (Waldfeld's Murasame, Kira's Strike Rouge x2, famiglia Freedom Gundam, Kshatriya) | 0 / 4 | 5 / 4 + 1 | Revisione richiesta da Kiraya convinta di combo giocate male: **il turno sospettato (t14) è in realtà il migliore della partita** (Lupus + Strike Freedom rimuovono 2 minacce in un colpo); decisa da 5 carte perse a scudo nei t11-13 e da un secondo Akatsuki Oowashi passato sbloccato dopo che entrambi i Blocker erano morti presto |
| 16 | [Neid](2026-08-10_kiraya-vs-neid.yaml) | **W** | 29 | Blu/Bianco, League Militaire/SEED (V-Dash Gundam, Victory Gundam in due stampe, Freedom Gundam, Kira Yamato in due stampe, Üso Ewin) | 0 / 0 | 11 / 14 + 4 | Vera guerra a specchio Strike Freedom Gundam (t19-23), risolta simmetricamente; **tre critiche auto-individuate da Kiraya rivelatesi infondate dopo verifica diretta delle carte** (blocker disponibili al t7, keyword Blocker assente su Strike Freedom Gundam al t19, soglia di livello di Widespread Annihilation al t23) |
| 17 | [KBB](2026-08-10_kiraya-vs-kbb.yaml) | **W** | 24 | Verde/Rosso, toolbox Celestial Being/00 Gundam (Gundam Exia, Gundam Kyrios in più stampe, Gundam Dynames, Trinity Warship, Hallelujah/Allelujah Haptism) | 0 / 0 | 10 / 8 + 1 | Prima partita contro questo archetipo; Widespread Annihilation pulisce l'intero campo nemico al t12; rimonta di logoramento vera - sia Strike Freedom Gundam (1 HP) che Barbatos Lupus (2 HP) a un soffio dalla morte al t22, vinta perché l'avversario resta completamente a secco al t23 |

## Prime osservazioni (da confermare su più partite)

- **Widespread Annihilation è genuinamente incostante, ma con un pattern
  chiaro**: colpi puliti da 3-per-0 in bluebob (t16), Roy Taric (t10) e Rei03
  (t20) — contro scarti-come-costo-abilità senza mai risolversi in Komadori
  (t14 **e** t17, due volte nella stessa partita) e Marcos sim (t14). Il
  fattore comune nelle partite dove funziona bene: viene lanciata contro un
  campo nemico ricco di bersagli Lv.4 o inferiore col proprio campo già
  vuoto o quasi. Quando finisce come "carta a caso da scartare" per Strike
  Freedom Gundam, spesso il campo nemico in quel momento non aveva
  comunque bersagli validi sotto soglia (confermato esplicitamente contro
  Neid, t23) — non è sempre un errore, va controllato caso per caso prima
  di etichettarlo come spreco.
- **Kira Yamato continua a dividersi per uso, non per proprietario**:
  confermato di nuovo in ZimZam, Komadori, Marcos sim, Direshift, Bench e
  Neid — la copia che appaiata attiva un debuff AP-2 in attacco (ST04-010)
  è distinta da quella che pesca al Link (GD05-081), anche quando le gioca
  lo stesso avversario nella stessa partita. Mai distinguibile dal colore.
- **Waldfeld's Murasame (il quirk di visualizzazione "Murasame (Andrew
  Waldfeld Unit)") è un'unità-problema ricorrente**: vista in Komadori,
  daedaedaes e Rei03. La cura garantita da Andrew Waldfeld (<Repair 2> via
  la sua abilità When-Linked, non del testo dell'unità) vanifica i ping
  parziali — serve rimozione dedicata (di solito una doppia attivazione di
  Lupus) per chiuderla davvero.
- **Due avversari diversi con lo stesso identico toolbox SEED/Orb**
  (Komadori e Rei03: Aile Strike Gundam, Akatsuki Oowashi, Andrew Waldfeld,
  Archangel, Argama, Kira's Strike Rouge, Waldfeld's Murasame) — sembra un
  archetipo riconoscibile del meta locale, non una coincidenza. Vale la
  pena tenerlo a mente come matchup ricorrente da studiare a parte.
- **Prima vittoria diretta contro un mazzo MF/G-Gundam completo** (vs
  Lamka) — la motivazione originale del pivot da `aggro_tekkadan_mono`
  (che contro questo archetipo aveva un winrate del 37,5%, 3-5). Un solo
  dato non basta a dire se il problema strutturale sia risolto, ma è il
  primo segnale positivo diretto.
- **Destiny Gundam resta un matchup strutturalmente difficile** (vs Marcos
  sim, unica sconfitta con una causa chiaramente esterna al piano di gioco
  di Kiraya): imbloccabile su ogni attacco più capacità di rischierare
  unità Minerva Squad dal trash pagandone il costo, potenzialmente
  all'infinito - un problema di matchup, non di sequenza di gioco.
- **Gundam Barbatos Lupus si conferma il motore più affidabile del mazzo**
  anche in questa lista più snella (3 copie contro le 5 totali
  Lupus/Lupus Rex di `aggro_tekkadan_mono_v1_1`): prestazioni solide in
  bluebob, Rei03, Vash, clairfryer, Neid, KBB — inclusa la disponibilità a
  bruciare le proprie copie duplicate come carburante per l'attivazione di
  un'altra copia in campo (vs Vash, t23).
- **L'unico errore tattico chiaramente auto-individuato dell'intero
  campione è contro ZimZam** (t12: Barbatos Adapt attacca per chip
  non-letale invece di spingere su una shield, muore gratis il turno dopo)
  — in netto contrasto con Komadori, Marcos sim, daedaedaes e Neid, dove
  Kiraya ha chiesto revisioni "hypercritical" convinta di propri errori e
  non ne è emerso nessuno di sostanziale, solo varianza o veri problemi
  strutturali di matchup.
- **Tre autocritiche di Kiraya smentite dai dati delle carte nella stessa
  partita** (vs Neid): "troppi blocker in campo" al t7 era vero e la scelta
  di non attaccare era corretta; l'attacco a un'unità invece che al player
  al t19 aveva un razionale valido anche se non per il motivo esatto
  ipotizzato (Strike Freedom Gundam non ha affatto la keyword Blocker); lo
  scarto di Widespread Annihilation al t23 era obbligato perché nessun
  bersaglio nemico era sotto la soglia di livello della carta. Promemoria
  utile: verificare sempre il testo esatto delle carte prima di confermare
  o correggere un'autocritica, in entrambe le direzioni.
- **Il mazzo NON è privo di Blocker** (correzione fatta durante la sessione
  dopo un'affermazione sbagliata nella revisione vs pylon): Gundam Gusion
  Rebake (4 copie) e Strike Rouge (Ootori) (3 copie) sono entrambi
  `<Blocker>` regolari e bloccano ripetutamente in quasi ogni partita del
  campione — il problema quando compare "No blockers available" è quasi
  sempre densità/tempismo (nessuna delle 7 copie ancora pescata o già
  morta), non assenza strutturale.
- **Partite vinte per esaurimento delle risorse avversarie più che per un
  singolo colpo decisivo**: clairfryer (mazzo shield esaurito), Chong
  (stesso, con Kiraya quasi altrettanto a secco), KBB (avversario
  letteralmente senza mosse al t23) — un pattern di vittorie da logoramento
  che si ripete più spesso delle vittorie nette (Belele, Bench, Roy Taric),
  coerente con un mazzo di grinding/valore piuttosto che puro rush.
