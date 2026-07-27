# aggro_tekkadan_mono_v1_5 — analisi del campione (18 partite, 10-8)

Sintesi trasversale delle partite giocate con `aggro_tekkadan_mono_v1_5`,
evoluzione diretta di `aggro_tekkadan_mono_v1_4` (che non ha un proprio
ANALISI.md — nessuna partita è stata registrata specificamente con quella
lista prima del cambio; vedi comunque `data/games/aggro_tekkadan_mono_v1_1/ANALISI.md`
e `data/games/aggro_mono_p/ANALISI.md` per la lineage completa e i pattern
strutturali più vecchi, che restano il riferimento di fondo). Cambi rispetto
a v1_4: Gundam Exia Repair 4→2, Overflowing Affection rimossa del tutto
(4→0, il secondo colore passa da Bianco a Rosso), aggiunti Airframe Seizure
(GD05-111, x3) e Darkness Finger (GD05-110, x3). Resto della lista invariato
(Graze Custom x4, Gundam Barbatos 1st Form x4, Ryusei-Go x2, Hyakuren x4,
Gundam Barbatos Adapt x4, Shiden Custom (Ryusei-Go) x4, Gundam Gusion Rebake
x3, Gundam Flauros (Ryusei-Go) x2, Gundam Barbatos Lupus x4, Mikazuki Augus
x4, Zeheart Galette x3, Minerva x2, Isaribi x2).

Con **18 sole partite** è ancora presto per isolare pattern definitivi;
questa sezione andrà riscritta man mano che il campione cresce, sul modello
di `aggro_tekkadan_mono_v1_1/ANALISI.md`.

Nota sul conteggio unità perse: include anche le casualties `inferred: true`
(kill da ping multi-target mai loggati come distruzioni esplicite) e, dove il
log non attribuisce chiaramente il possessore (mirror-match parziali/totali
con carte identiche su entrambi i lati), il numero riportato è approssimato
— vedi la nota della singola partita quando rilevante.

## Tabella partite

| # | Data | Avversario | Esito | Turni | Mazzo avversario | Shield rimaste (K / avv) | Unità perse (K / avv) | Nota chiave |
|---|------|-----------|-------|-------|-------------------|------------------------|------------------------|-------------|
| 1 | 07-24 | [Hichem](2026-07-24_kiraya-vs-hichem.yaml) | **L** | 24 | Rosso/Viola, ZAFT SEED (Duel Gundam Assault Shroud chain-deploy, Eliminate Target x2, Jachin Due/Blitz Gundam First Strike, Aegis/Destiny/Providence Gundam) | 0 / 1 | 16 / 12 | t12 decisivo: 2 Eliminate Target eliminano i piloti appaiati (Mikazuki Augus, Zeheart Galette) mentre l'unico Blocker era già speso; t13/t15 ottimo recupero con Lupus dal trash accumulato |
| 2 | 07-24 | [Ironman655](2026-07-24_kiraya-vs-ironman655.yaml) | **W** | 15 | Viola/Rosso, Celestial Being (Gundam Exia/Kyrios/Virtue, Trans-Am) | 5 / 0 | 5 / 4 | Partita pulita, nessun errore individuato; entrambe le copie di Lupus milled dal proprio Exia Repair al t6, vinta comunque solo sulla curva d'apertura |
| 3 | 07-24 | [RYOMARU](2026-07-24_kiraya-vs-ryomaru.yaml) | **L** | 14 | Verde, Neo Zeon (Char's Zaku Ⅱ + Char Aznable High-Maneuver, Zeong, Zaku Ⅱ) | 0 / 2 | 5 / 9 | Unico vero errore di sequenza del campione: al t11 Shiden Custom, già Linked ed eleggibile ad attaccare, resta inutilizzato mentre un secondo Barbatos Adapt viene sacrificato per lo stesso identico kill |
| 4 | 07-24 | [240pBrian](2026-07-24_kiraya-vs-240pbrian.yaml) | **L** | 21 | Blu/Rosso, control pesante (Close Combat x2, Improved Technique x2, Darkness Finger x2, Battle of Aces, Strike Freedom Gundam x2, Unicorn Gundam 02 Banshee, Kshatriya, 5x pesca-2) | 2 / 3 | 13 / 3 | Resa corretta al t21 contro il matchup più difficile del campione; unico neo un piccolo tempo perso al t5 (Exia Repair non attacca pur eleggibile), il resto giocato bene |
| 5 | 07-24 | [Bill](2026-07-24_kiraya-vs-bill.yaml) | **W** | 18 | Blu/Verde, Earth Federation/Londo Bell (Amuro Ray, Nu Gundam, famiglia Re-GZ, Gundam ST01-001) | 4 / 2 | 9 / 9 | Vittoria per resa; Amuro Ray resta il Blocker prima di attaccare (tech da ricordare), Lupus chiude al t18 con due attivazioni sul trash accumulato |
| 6 | 07-24 | [HortyPidge](2026-07-24_kiraya-vs-hortypidge.yaml) | **W** | 17 | Blu/Bianco, Zeon (Char's Zaku Ⅱ/Char Aznable, Z'Gok E, Hy-Gogg, Gelgoog, Rick Dom, Kämpfer) | 0 / 0 | 8 / 9 | Vinta per un pelo: entrambi i giocatori a 0 shield, vera guerra di logoramento; t13 tripla attivazione di Lupus elimina entrambe le copie di Rick Dom nello stesso turno |
| 7 | 07-24 | [Fusiki](2026-07-24_kiraya-vs-fusiki.yaml) | **L** | 21 | Blu/Bianco, SEED-Destiny (Strike Freedom Gundam + Kira Yamato, Aile Strike Gundam, Strike Rouge Ootori/Kira's Unit) | 1 / 4 | 13 / 9 | Errore reale trovato: Gundam Barbatos 1st Form Linked al t7 ma non attacca fino al t13, 3 turni di danno gratuito lasciati sul tavolo; terza sconfitta recente contro il pacchetto Strike Freedom/Kira Yamato |
| 8 | 07-25 | [Chebycheff](2026-07-25_kiraya-vs-chebycheff.yaml) | **W** | 26 | Blu/Bianco, League Militaire/SEED ibrido (Reineforce Jr., Overflowing Affection x2, Victory Gundam, Strike Freedom Gundam x2, Riddhe Marcenas) | 3 / 0 | 14 / 16 | Partita più lunga e pulita del campione, nessun errore individuato; Lupus decisivo due volte, t9 gestisce bene un Reineforce Jr. che si rigenera di continuo |
| 9 | 07-26 | [dadada](2026-07-26_kiraya-vs-dadada.yaml) | **L** | 14 | Verde, Londo Bell (Amuro Ray, Nu Gundam combo esilio+battaglia-bonus x3+ copie, Jegan, famiglia Re-GZ) | 0 / 4 | 7 / 5 | Lupus scartato dalla shield pile al t12 (sfortuna, non errore); il combo Nu Gundam/Amuro Ray (esilia 3, battaglia extra) infligge 3 attacchi pieni da un solo dispiegamento due volte |
| 10 | 07-26 | [AnyingORNG](2026-07-26_kiraya-vs-anyingorng.yaml) | **W** | 13 | Viola/Bianco, shell quasi-mirror Tekkadan (Barbatos 1st Form, Gusion Rebake, Ryusei-Go identici, McGillis'/Gaelio's Schwalbe Graze) | 6 / 1 | 2 / 4+ | Vittoria shield-perfect (6/6 mai toccate); t7 ping di precisione chirurgica su un Barbatos 1st Form nemico già indebolito |
| 11 | 07-26 | [WanChin](2026-07-26_kiraya-vs-wanchin.yaml) | **W** | 12 | Rosso, Earth Alliance/ZAFT Extended (Chaos Gundam, Forbidden Gundam, GFreD, Destroy Gundam) | 5 / 1 | 3 / 0 | Vittoria dominante e ben giocata, non solo statistiche favorevoli; Darkness Finger usata proattivamente a metà combattimento per preparare il finish successivo |
| 12 | 07-26 | [Amo](2026-07-26_kiraya-vs-amo.yaml) | **L** | 22 | Rosso, mirror-ish Tekkadan + splash Neo Zeon (Barbatos Lupus/Adapt/Gusion Rebake speculari, Sazabi, Char Aznable) | 0 / 2 | 4 / 5+ | Partita di margine sottilissimo: t21 riduce Sazabi a 1 HP esatto senza finirlo, e quell'1 HP consegna il colpo di grazia al t22; Char Aznable qui è una stampa diversa (GD05-093) da quella vista contro RYOMARU/HortyPidge (ST03-011) |
| 13 | 07-26 | [OuO](2026-07-26_kiraya-vs-ouo.yaml) | **W** | 19 | Blu/Rosso, stesso mazzo di 240pBrian (Close Combat, Improved Technique, Battle of Aces, Strike Freedom Gundam, Kshatriya, Unicorn Gundam 02 Banshee) | 3 / 0 | 9 / 6 | Stesso identico archetipo che aveva battuto duramente come 240pBrian - stavolta vinta: prova concreta che il matchup è giocabile, non una sconfitta garantita |
| 14 | 07-26 | [Ja Rul](2026-07-26_kiraya-vs-jarul.yaml) | **L** | 21 | Blu/Rosso, control ancora più denso (Improved Technique x3, Close Combat, Darkness Finger, Overwhelming Pressure, Kindhearted, Strike Freedom Gundam x2, Unicorn Gundam 02 Banshee) | 0 / 0 | 14 / 2 | Gundam Barbatos Lupus non tocca mai il campo in tutta la partita, bloccato nella shield pile fino allo scarto al t20 - sfortuna pura, nessun errore tattico individuato |
| 15 | 07-26 | [Musou](2026-07-26_kiraya-vs-musou.yaml) | **L** | 16 | Verde/Bianco, Gundam Wing (Heavyarms, Wing Gundam, Heero Yuy, Peacemillion, Zaku Ⅱ, Rick Dom) | 0 / 4 | 8 / 6 | Vera guerra di logoramento senza errori individuati; Lupus perso a uno scarto da shield, poi Zeheart Galette mill Darkness Finger e Mikazuki Augus nello stesso colpo il turno dopo |
| 16 | 07-26 | [dajematti](2026-07-26_kiraya-vs-dajematti.yaml) | **W** | 14 | Rosso/Bianco, G Gundam "MF con Master Asia" (Gundam Maxter, Cyclone Punch/Chibodee Crocket, Shining Gundam a recursione, Master Gundam/Master Asia, Domon Kasshu) | 4 / 0 | 6 / 3 | Primo vero dato su questo archetipo meta segnalato come minaccia emergente - vinta senza perdere neanche uno shield; t6 Darkness Finger su Gundam Maxter nega il combo Maxter+Cyclone Punch sul nascere |
| 17 | 07-26 | [Niki](2026-07-26_kiraya-vs-niki.yaml) | **W** | 11 | Blu/Bianco, League Militaire/UC ibrido (Reineforce Jr., Victory Gundam, Strike Freedom Gundam, Unicorn Gundam 02 Banshee Norn, Zoloat) | 6 / 0 | 3 / 3 | Vittoria shield-perfect (6/6 mai toccate); t10 il turno migliore, Airframe Seizure + Darkness Finger + 4 attacchi in un solo colpo |
| 18 | 07-26 | [bladee](2026-07-26_kiraya-vs-bladee.yaml) | **W** | 17 | Verde/Bianco, Gundam Wing (Heavyarms, Wing Gundam/Zero EW, Heero Yuy, Altron Gundam, Silver Bullet, Flat (Militia)) | 2 / 0 | 7 / 9 | Analisi rigorosa richiesta esplicitamente da Kiraya: nessun errore trovato in tutta la partita; risultato d'importazione corretto da un "Winner!" non attribuito, verificato via shields_tally |

## Prime osservazioni (da confermare su più partite)

- **Il cambio di lista (Exia Repair 4→2, Overflowing Affection fuori,
  Airframe Seizure x3 + Darkness Finger x3 dentro) sposta il mazzo verso
  interazione diretta invece che pura pesca**: Darkness Finger è stata
  determinante o quantomeno rilevante in quasi ogni partita (uccisioni
  puntuali su Zoloat, Gundam Maxter, Chaos Gundam, Nu Gundam, Graze
  Commander Type, Char's Zaku Ⅱ...), mentre Airframe Seizure ha convertito
  più volte una copia di riserva in gas (Bill, hortypidge, jarul, Ja Rul,
  bladee). Troppo presto per dire se il taglio di Overflowing Affection
  (motore di pesca puro) sia stato un compromesso netto positivo.
- **Il pacchetto Strike Freedom Gundam + Kira Yamato resta il problema
  strutturale numero 1, ma non è più una sconfitta garantita**: ha deciso
  o pesato molto in 3 sconfitte (Hichem, 240pBrian, Fusiki) contro lo
  stesso identico mazzo di 240pBrian rivisto **vinto** come OuO - la
  prova concreta più chiara finora che il matchup si può giocare, non solo
  subire. Chebycheff, Ja Rul e Niki confermano che l'archetipo (Strike
  Freedom/Kira Yamato + varianti League Militaire/UC) è molto diffuso nel
  meta attuale ma il risultato dipende dall'esecuzione, non è deciso a
  priori dalla lista avversaria.
- **Secondo problema ricorrente, distinto: la combo esilio+battaglia-bonus
  di Nu Gundam (GD05-017) abbinato ad Amuro Ray** - vista contro Bill
  (sopravvissuta), dadada (decisiva nella sconfitta, 3+ copie viste, ognuna
  capace di 3 attacchi pieni da un solo dispiegamento) e Amo (mirror-ish,
  partita di margine sottile). Meccanicamente distinto dal blocco di
  High-Maneuver già documentato in v1_1 - qui si salta dichiarazione/blocco
  del tutto tramite l'abilità stessa, non tramite un keyword.
- **Primo vero dato sul "MF con Master Asia" (G Gundam), segnalato da
  Kiraya come minaccia meta emergente prima ancora di incontrarlo**: vinto
  nettamente contro dajematti (0 shield perse). Il combo Gundam
  Maxter+Cyclone Punch (che aveva causato danni reali in una partita
  precedente di questa sessione, "ASDF") è stato negato sul nascere da una
  Darkness Finger proattiva al t6, prima ancora che potesse iniziare a
  girare - un solo campione, da confermare, ma un buon segno.
- **Solo due errori tattici reali individuati in tutto il campione, ed
  entrambi della stessa famiglia**: al t11 vs RYOMARU, Shiden Custom
  (Ryusei-Go) già Linked ed eleggibile ad attaccare resta inutilizzato
  mentre un secondo Barbatos Adapt viene sacrificato per lo stesso identico
  kill (nessun costo netto per fortuna, ma un'inefficienza reale); al
  t7-t11 vs Fusiki, Gundam Barbatos 1st Form Linked resta fermo per 3 turni
  interi contro un board avversario passivo, lasciando sul tavolo danno
  gratuito e pesca via Attack-trigger. In tutte le altre 16 partite, revisioni
  anche esplicitamente richieste e rigorose (bladee) non hanno trovato
  nulla da correggere - il livello di esecuzione del campione è alto.
- **La fortuna nel mazzo/shield pile resta la causa di sconfitta più
  frequente, non gli errori**: Gundam Barbatos Lupus perso senza mai
  combattere per scarto diretto dalla shield pile (dadada t12, Ja Rul -
  intera partita, Musou t14) o per danno incidentale (Amo t20, un ping da 1
  di Rewloola). Lo stesso vale per il mill: Zeheart Galette e il
  self-mill di Gundam Exia Repair hanno tolto pezzi chiave di continuo
  (Ironman655 t6: entrambe le copie di Lupus; Musou t15: Darkness Finger +
  Mikazuki Augus nello stesso colpo, subito dopo aver perso Lupus).
- **Correzione doppia sull'attribuzione del risultato d'importazione**: sia
  Amo che bladee avevano un log con la riga finale "Winner!" priva del nome
  giocatore, causando una prima lettura sbagliata in entrambi i casi -
  risolta incrociando `shields_tally` (chi ha 0 shield rimanenti è chi ha
  perso) prima di fidarsi della riga grezza. Vale la pena controllare
  sempre quella tabella quando la riga finale del log non è inequivocabile.
- **Char Aznable conferma di poter essere stampe diverse contro avversari
  diversi pur nello stesso archetipo**: ST03-011 (bonus High-Maneuver in
  Attack) contro RYOMARU e HortyPidge, ma GD05-093 (recupera una Base Neo
  Zeon dal trash al Link) contro Amo - stesso principio già consolidato in
  v1_1, qui riconfermato con lo stesso identico nome carta in tre partite
  diverse della stessa sessione.
- **Kira Yamato: stampe miste nella stessa partita in alcuni casi, singola
  stampa in altri**: Fusiki, Chebycheff e 240pBrian mostrano sia GD05-081
  (pesca al Link) sia ST04-010 (debuff AP-2 nemico in attacco) nello stesso
  log; OuO, Ja Rul e Niki mostrano solo evidenza di GD05-081 per l'intera
  partita. Nessuna scorciatoia valida: va verificato ogni volta con
  l'abilità osservata, mai assunto dal nome.
- **Vittorie shield-perfect (0 shield perse) già in due partite su 18**
  (AnyingORNG, Niki, entrambe 6/6 residue) - più due dominanti quasi
  altrettanto pulite (WanChin 5/1, dajematti 4/0) - un tasso di blowout
  incoraggiante quando la curva d'apertura tiene, coerente col principio
  già visto in v1_1 che il piano-motore (Lupus) non è sempre necessario.
- **"Missing destroy event" nel log/parser resta un'anomalia costante,
  ormai attesa più che sospetta**: ricorrente in quasi ogni partita (ping
  che dovrebbero uccidere un'unità a HP1 ma non producono una riga di
  distruzione esplicita). Il caso vs dajematti (t8-t9) è stato per la
  prima volta confermato indirettamente da un requisito di costo di una
  carta successiva (il Deploy di Shining Gundam richiede 2 unità MF già
  nel trash) - buona prova che l'anomalia è di logging, non di regola.
- **Stesso quirk di visualizzazione Linked-unit già in CLAUDE.md,
  riconfermato**: "Strike Rouge (Kira's Unit)" (vs Chebycheff) è
  effettivamente Kira's Strike Rouge (GD05-010), stesso pattern già visto
  più volte in v1_1.
- **Stesso quirk "una carta rivelata dalla shield pile colpisce il
  proprietario della shield, non l'avversario" riconfermato** (vs WanChin,
  t9): la Darkness Finger di WanChin, rivelata dalle shield di Kiraya,
  colpisce un'unità di WanChin stesso - comportamento carta-specifico da
  aspettarsi, non un errore da segnalare quando si ripresenta.
- **Due mirror-match parziali/totali nello stesso campione**: AnyingORNG
  gioca un nucleo Tekkadan quasi identico (Barbatos 1st Form, Gusion
  Rebake, Ryusei-Go con gli stessi id) con innesti Gundam/G Generation
  diversi; Amo gioca una lista ancora più speculare (Lupus/Adapt/Gusion
  Rebake condivisi) con uno splash Neo Zeon (Sazabi, Char Aznable) - la
  partita di margine più sottile del campione (decisa da 1 HP esatto).
