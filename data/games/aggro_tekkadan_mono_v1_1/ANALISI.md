# aggro_tekkadan_mono_v1_1 — analisi del campione (32 partite, 21-11)

Sintesi trasversale delle partite giocate con `aggro_tekkadan_mono_v1_1`,
la prima iterazione derivata da `aggro_mono_p` (vedi
`data/games/aggro_mono_p/ANALISI.md` per l'analisi delle 20 partite del
mazzo precedente — i pattern strutturali di quel mazzo restano il
riferimento finché questo campione non è abbastanza grande da confermarli
o smentirli per conto proprio). Cambi rispetto ad `aggro_mono_p`: Gundam
Gusion Rebake 4→3, Shiden Custom (Ryusei-Go) 2→3, Gundam Barbatos Lupus
3→4, Sword Impulse Gundam e Akihiro Altland rimossi, Become a Shield 1→2,
aggiunti Gundam Barbatos Lupus Rex (GD05-051, x1) e Gundam Barbatos 5th
Form Ground Type (GD03-066, x1 — la zona Earth non è un vincolo di gioco
attuale, vedi CLAUDE.md).

Con **32 sole partite** è troppo presto per isolare pattern affidabili;
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
| 3 | 07-17 | [SaintAbbel](2026-07-17_kiraya-vs-saintabbel.yaml) | **W** | 14 | Blu/Bianco, League Militaire/UC (Rick Dias, Strike Rouge Ootori, Perfect Strike Gundam, Argama, A Show of Resolve) | 6 / 0 | 5 / 4 | Prima vittoria: 0 shield perse nonostante 5 unità perse contro 4; Barbatos 5th Form (Ground Type) mai calato, scartato al t5 per l'abilità di Ryusei-Go; Lupus/Lupus Rex ancora mai pescati (3 partite su 3) |
| 4 | 07-17 | [iceberg](2026-07-17_kiraya-vs-iceberg.yaml) | **W** | 15 | Rosso/Viola, Earth Alliance/Phantom Pain (Chaos/Gaia/Abyss Gundam, Auel Neider, Sting Oakley, Stellar Loussier) + splash 0 Gundam | 2 / 0 | 6 / 8 | Prima vera prova di Barbatos Lupus: doppia attivazione t13 + kill al t15 chiudono la partita, nonostante Gaia Gundam/Abyss Gundam (MA Mode) abbiano scartato dalla mano (non dal campo) una copia di Lupus e una di Gusion Rebake |
| 5 | 07-17 | [liko](2026-07-17_kiraya-vs-liko.yaml) | **L** | 20 | Verde/Bianco, Londo Bell + Operation Meteor (Re-GZ family, Nu Gundam x2 stampe, Wing Gundam/Zero/Zero EW, Heero Yuy, Amuro Ray, Ra Cailum) | 0 / 0 | 11 / 5 | Svolta al t14: Nu Gundam LR uccide Lupus e 2nd Form nella stessa turno via un'abilità che salta dichiarazione/blocco; chiusa al t20 da Wing Gundam Zero (High-Maneuver) - stesso buco di block-bypass già visto vs sgd |
| 6 | 07-17 | [Robotech](2026-07-17_kiraya-vs-robotech.yaml) | **L** | 20 | Blu/Bianco, SEED (Kira Yamato) + Orb/AEUG (Strike Freedom Gundam, Aile Strike Gundam, Strike Rouge x2, Freedom Gundam, Murasame/Andrew Waldfeld, Archangel) | 0 / 2 | 12 / 9 | Strike Freedom Gundam rimanda Lupus Rex (t14) e 1st Form (t16) nel mazzo - stesso problema-chiave di aggro_mono_p, non risolto dalle 5 copie totali di v1_1; saturazione avversaria da 3 shield in un turno (t20) chiude la partita |
| 7 | 07-17 | [GenocidGIC](2026-07-17_kiraya-vs-genocidgic.yaml) | **W** | 23 | Blu/Bianco, Titans/Jupitris (The-O, Messala, Paptimus Scirocco, Delta Plus) + splash Unicorn Gundam 02 Banshee Norn (Destroy Mode), Gundam/Amuro Ray, Zoloat, Kindhearted, Corsica Base | 1 / 0 | 12 / 10 | Vittoria di sfinimento in 23 turni; t12 quasi-wipe da un Banshee che si riattiva 3 volte nello stesso turno, ma Barbatos Lupus torna in campo 4 volte distinte nel corso della partita e chiude comunque - miglior prova finora del piano-motore |
| 8 | 07-17 | [GenocidGIC](2026-07-17_kiraya-vs-genocidgic-2.yaml) | **W** | 17 | Blu/Bianco, stesso mazzo Titans/Jupitris + Unicorn Gundam 02 Banshee Norn (rivincita) | 3 / 0 | 8 / 6 | Vittoria netta senza mai pescare Gundam Barbatos Lupus - il piano-motore non è indispensabile quando la curva di apertura regge; Banshee ripete il pattern di riattivazioni multiple ma stavolta non basta |
| 9 | 07-17 | [dogman](2026-07-17_kiraya-vs-dogman.yaml) | **L** | 13 | Verde/Blu, Londo Bell/Zeon (Zaku Ⅱ, Jegan, Rick Dom x2, Gundam/Amuro Ray, Nu Gundam x2, Kayra's Re-GZ, Re-GZ) | 0 / 4 | 8 / 7 | Svolta t7: 3 attacchi consecutivi spazzano via 3 unità in un colpo perché nessuno dei 2 blocker del mazzo (Gusion Rebake/Shiden Custom) era ancora sceso - Shiden Custom infatti blocca poi regolarmente più avanti nella stessa partita; nessun errore tattico isolato dopo revisione |
| 10 | 07-17 | [112t](2026-07-17_kiraya-vs-112t.yaml) | **W** | 14 | Rosso, Earth Alliance/Phantom Pain (Abyss/Chaos/Gaia Gundam, Auel Neider, Sting Oakley, Stellar Loussier, Exass, Girty Lue, Kindhearted) | 4 / 1 | 6 / 6 | Vittoria per resa dell'avversario al t14, non per shield-out - posizione già nettamente favorevole (4 shield contro 1); nessun errore tattico isolato, Lupus mai pescato in partita |
| 11 | 07-17 | [loclee](2026-07-17_kiraya-vs-loclee.yaml) | **L** | 23 | Blu/Rosso, control/removal (Darkness Finger x3, Improved Technique, Close Combat x2, Strike Freedom Gundam, Unicorn Gundam 02 Banshee Destroy Mode) | 0 / 2 | 12 / 4 | Log troncato sul colpo di grazia, risultato impostato a mano; avversario che riunisce quasi tutti i problemi strutturali già noti del mazzo; unico errore reale al t14 (2nd Form sacrificato in un chip che Lupus da solo bastava a completare) |
| 12 | 07-17 | [gogogo](2026-07-17_kiraya-vs-gogogo.yaml) | **W** | 14 | Bianco/Viola, Zaft Destiny/Minerva Squad (Destiny Gundam, famiglia Impulse Gundam, Shinn Asuka) + splash Militia | 5 / 0 | 8 / 6 | Stravinta: 0 shield perse, avversario già a shield zero da fine t13 (probabile resa al t14). Prima vera attivazione di Lupus in partita pulisce entrambe le copie rimaste di Sword Impulse Gundam in un colpo; Widespread Annihilation scartata come shield senza mai essere giocata |
| 13 | 07-17 | [peachique](2026-07-17_kiraya-vs-peachique.yaml) | **W** | 13 | Blu/Verde, Londo Bell (ReZEL, Kayra's Jegan/Kayra Su, Nu Gundam x2 stampe, Amuro Ray, Davao) | 2 / 0 | 6 / 6 | Vittoria pulita per shield-out, nessun errore tattico individuato; t11 saturazione da 4 attacchi nello stesso turno (Flauros, Graze Custom, Ryusei-Go, Hyakuren) distrugge una base e toglie 3 shield in un colpo; Lupus mai pescato e non è servito |
| 14 | 07-17 | [TJL](2026-07-17_kiraya-vs-tjl.yaml) | **W** | 15 | Blu/Bianco, stesso archetipo SEED Kira Yamato + Amuro Ray già visto contro Robotech (Aile Strike Gundam, Freedom Gundam, Strike Rouge Kira's Unit, Gundam ST01-001) | 5 / 0 | 8 / 7 | Vittoria per shield-out netto; unico errore reale al t7 (Activate di Isaribi sprecato su Ryusei-Go già rested, che aveva già attaccato quel turno); Lupus uccide "Gundam" con precisione chirurgica al t13 (4 danni esatti contro HP4 piena) |
| 15 | 07-17 | [Essen](2026-07-17_kiraya-vs-essen.yaml) | **L** | 23 | Blu/Rosso/Bianco, control/removal estremo (Close Combat x3, Improved Technique, Battle of Aces x2, Overwhelming Pressure x4, Darkness Finger, Strike Freedom Gundam x2, Unicorn Gundam 02 Banshee Destroy Mode) + motore di pesca fuori scala (~20+ carte pescate in più) | 0 / 1 | 12 / 4 | Revisione richiesta da Kiraya: nessun errore tattico individuato, la mano di rimozione/pesca dell'avversario è la più pesante vista nel campione, persino più di loclee (partita 11) - board di Essen vuoto fino al t13 |
| 16 | 07-17 | [xDEADHEADx](2026-07-17_kiraya-vs-xdeadheadx.yaml) | **W** | 16 | Viola/Verde, Neo Zeon (Char's Zaku Ⅱ + Char Aznable per High-Maneuver, Zeong con token, Sazabi, Jagd Doga/Geara Doga) | 4 / 0 | 8 / 8 | Vittoria pulita per shield-out; Char's Zaku Ⅱ linkato ottiene High-Maneuver a ogni attacco (t8, t10) - stesso buco di block-bypass già noto; l'abilità Attack di Sazabi al t16 fallisce contro Kiraya perché Lupus era l'unica unità in campo e quindi "impegnata in combattimento", non un bersaglio valido |
| 17 | 07-17 | [jaysanti](2026-07-17_kiraya-vs-jaysanti.yaml) | **L** | 18 | Rosso/Bianco, Shuffle Alliance/G Gundam (Domon Kasshu, Master Asia, Shining Gundam x3 stampe, Rising Gundam, Dragon Gundam, Gundam Maxter) | 0 / 3 | 14 / 8 | Sconfitta per shield-out, non per High-Maneuver (zero istanze nel log, a differenza della diagnosi iniziale di Kiraya): decisa da un errore di blocco al t14 (Shiden Custom disponibile non usato contro Master Asia), dalla tech dell'avversario che resta i blocker di Kiraya prima di attaccare (Domon/Master Asia su Rising Gundam), e da Lupus mai pescato perché milled 2 volte dal proprio Exia Repair |
| 18 | 07-18 | [desi](2026-07-18_kiraya-vs-desi.yaml) | **W** | 18 | Blu/Verde, Earth Federation/Londo Bell/AGE System (Gundam + Amuro Ray, famiglia AGE-1/AGE-2 Double Bullet, Re-GZ, Nu Gundam, Jegan, base Ra Cailum) | 4 / 1 | 8 / 9 | Vittoria per timeout dell'avversario al t18 da una posizione già nettamente vinta (4 shield contro 1); nessun errore tattico individuato; la seconda copia di Barbatos Lupus si attiva due volte nello stesso turno (t15), concatenando ping e attacchi per finire un solo bersaglio invece di disperderli |
| 19 | 07-18 | [Olo](2026-07-18_kiraya-vs-olo.yaml) | **W** | 19 | Blu/Bianco, Earth Alliance/SEED con doppia stampa di Kira Yamato (Rick Dias, famiglia Strike/Aile Strike/Strike Freedom Gundam, Wing Gundam Zero EW, Archangel) | 1 / 0 | 12 / 10 | Vittoria per shield-out netto nonostante il bounce di Strike Freedom Gundam (qui "returned to deck", non in mano) al t16; seconda doppia attivazione di Lupus nello stesso turno in due partite di fila (t13); nessun errore tattico individuato |
| 20 | 07-18 | [MrCross00](2026-07-18_kiraya-vs-mrcross00.yaml) | **W** | 13 | Blu/Verde, Londo Bell/Earth Federation (Gundam + Amuro Ray, Jegan, Nu Gundam, Re-GZ/Re-GZ BWS, Zeong, Ra Cailum) | 6 / 0 | 3 / 2 | Vittoria totale in 13 turni, 0 shield perse ed EX Base mai distrutta, senza mai pescare né Barbatos Lupus né il pacchetto Blocker - solo pressione da apertura; stessa identità ambigua di "Gundam" già vista vs desi lo stesso giorno (poi risolta, vedi sotto), con lo stesso identico numero di danno (6) osservato in entrambe le partite |
| 21 | 07-18 | [Nate](2026-07-18_kiraya-vs-nate.yaml) | **W** | 11 | Blu/Rosso, League Militaire (Gadeel, famiglia Victory Gundam/V2 Gundam + Üso Ewin) | 4 / 0 | 4 / 3 | Vittoria per shield-out netto in 11 turni nonostante un quasi-wipe al t10 (3 unità perse nello stesso turno) e sia Lupus che Barbatos Adapt persi al mill-on-death di Exia Repair fin dal t7 - il piano-motore era morto in partenza, la pressione pura ha chiuso comunque; nessun errore tattico individuato |
| 22 | 07-18 | [KUMA](2026-07-18_kiraya-vs-kuma.yaml) | **L** | 14 | Viola/Bianco, Operation Meteor/G Team Gundam Wing EW (doppio Gundam Heavyarms Custom (EW), Gundam Sandrock Custom (EW), Wing Gundam Zero (EW) + Heero Yuy, GN Armor Type-E) | 1 / 2 | 9 / 1 | Sconfitta per shield-out; revisione richiesta da Kiraya convinto di propri errori, ma nessuna sequenza chiaramente sbagliata trovata - decisa da mill sfortunato (entrambe le copie di Lupus in trash al t6), una combo debuff-poi-distruggi intenzionale (Heavyarms + GN Armor Type-E) e doppio debuff ripetibile (2x Heavyarms + Sandrock) |
| 23 | 07-18 | [Sakurah](2026-07-18_kiraya-vs-sakurah.yaml) | **W** | 13 | Mono-Verde, Earth Federation/Londo Bell (Jegan, Gundam AGE-1 Normal + Asemu Asuno, Re-GZ, Nu Gundam + Amuro Ray) | 1 / 0 | 5 / 4 | Vittoria per shield-out netto; Gundam Barbatos 1st Form pesca almeno 6 volte nel corso della partita grazie a più copie in rotazione, il motore di pesca più prolifico visto finora nel campione; trade decisivo al t11 (Barbatos 1st Form contro Nu Gundam) rimuove la minaccia principale avversaria |
| 24 | 07-18 | [Kumendeng](2026-07-18_kiraya-vs-kumendeng.yaml) | **W** | 15 | Blu/Verde, Zeon rush (Zaku I/II, Guntank, Char Aznable, Zeong + Char, Nu Gundam + Amuro Ray, Corsica Base) | 1 / 0 | 5 / 9 | Vittoria per timeout dell'avversario da una posizione già vinta; High-Maneuver reale e decisivo al t11 (Char Aznable linkato a Zeong); seconda doppia attivazione di Lupus nello stesso turno in due partite di fila (t12); scoperta e corretta un'importante svista nei dati di Amuro Ray (GD05-085) |
| 25 | 07-19 | [Bugs](2026-07-19_kiraya-vs-bugs.yaml) | **W** | 14+ | Blu/Rosso, misto SEED/Unicorn/Neo Zeon (Strike Rouge Ootori/Kira's Unit + Kira Yamato, Zoloat, Gundam Kyrios Flight Mode, Kshatriya, Strike Freedom Gundam) | 5 / 2 | 6 / 6 | Vittoria totale, 0 shield perse; log probabilmente troncato prima del colpo di grazia (come loclee); turno di sfondamento al t9 (2-per-2 che elimina entrambe le minacce principali avversarie); seconda conferma dello stesso errore nei dati carte già trovato su Amuro Ray, stavolta su Kira Yamato (GD05-081) |
| 26 | 07-19 | [Eshaku](2026-07-19_kiraya-vs-eshaku.yaml) | **W** | 24 | Mono-Rosso, "Tekkadan splash Zeon/UC/Clan" - mirror-match parziale (Barbatos 1st Form/Adapt, Hyakuren, Mikazuki Augus) + Sazabi, Kshatriya, GQuuuuuuX Omega Psycommu, doppia Close Combat/Improved Technique | 2 / 0 | 13 / 9+ | Vittoria per shield-out al t24 dopo una partita lunga e logorante, vinta "per un soffio" secondo Kiraya; terza e più estrema istanza di attivazioni multiple di Lupus nello stesso turno (t14, TRE attivazioni consecutive); avversario fortemente orientato alla rimozione diretta (2x Close Combat, 2x Improved Technique, Battle of Aces) |
| 27 | 07-19 | [Juuto](2026-07-19_kiraya-vs-juuto.yaml) | **L** | 20 | Blu/Verde, Earth Federation/Londo Bell (Gundam + Amuro Ray, Nu Gundam LR + Amuro Ray, Re-GZ, ReZEL, Jegan, Kayra Su + Kayra's Jegan) | 0 / 2 | 16 / 8 | Sconfitta per shield-out; revisione richiesta da Kiraya convinto di propri errori, ma nessuna sequenza sbagliata trovata - decisa da un'unica causa strutturale ripetuta tre volte (t14, t18, t20): l'abilità When Paired di Nu Gundam (GD05-017) salta dichiarazione/blocco e colpisce direttamente, usata due volte per eliminare Lupus non appena rischierato (con Breach 5 che distrugge anche Isaribi entrambe le volte) |
| 28 | 07-19 | [1231](2026-07-19_kiraya-vs-1231.yaml) | **W** | 10 | Blu/Rosso, control leggero (Signs of a Revolution x2, Rewloola, Kindhearted) | 6 / 2 | 3 / 1 | Vittoria per resa dell'avversario al t10 da una posizione già completamente vinta (0 shield perse); rimozione diretta ripetuta dell'avversario (2x Signs of a Revolution, self-ping di Rewloola) non intacca il ritmo offensivo; nessun errore tattico individuato |
| 29 | 07-19 | [miii](2026-07-19_kiraya-vs-miii.yaml) | **W** | 13 | Blu/Verde, Earth Federation/Londo Bell + splash OZ/Zeon (Jegan, Re-GZ/Kayra's Re-GZ, Nu Gundam in due stampe, Corsica Base + token Tallgeese, Rick Dom x2) | 1 / 0 | 12 / 8 | Vittoria per shield-out di misura dopo un t12 quasi disastroso (Nu Gundam LR + Tallgeese + Rick Dom spazzano via 4 unità, Isaribi distrutta due volte nello stesso turno); recupero pulito al t13, nessun errore tattico individuato |
| 30 | 07-19 | [CE1117](2026-07-19_kiraya-vs-ce1117.yaml) | **L** | 24 | Blu/Bianco, League Militaire (Gun EZ, Strike Rouge Ootori, Aile Strike/Strike Freedom Gundam + Kira Yamato, famiglia Victory Gundam/V2 Gundam, Zoloat) | 0 / 0 | 14 / 13 | Sconfitta per shield-out nella partita più equilibrata del campione (3 shield perse su 3 per entrambi, 0-0); tripla attivazione di Lupus al t21 elimina sia Strike Freedom Gundam che Victory Gundam ma CE1117 ricostruisce troppo in fretta; nessun errore tattico individuato, decisa dalla velocità di ricostruzione del motore League Militaire avversario |
| 31 | 07-19 | [tinki](2026-07-19_kiraya-vs-tinki.yaml) | **W** | 20 | Blu/Bianco, Earth Federation/SEED ibrido (Rick Dias, Gundam NT-1 + Amuro Ray, Gundam + Kira Yamato, Altron Gundam EW, Freedom Gundam, Industrial 7) | 3 / 0 | 12 / 10 | Vittoria per shield-out in una partita lunga ed equilibrata; risolto un altro caso del rompicapo "Gundam" (stavolta abbinato a Kira Yamato ST04-010); motore di debuff ripetibile di Kira Yamato osservato 4 volte; nessun errore tattico individuato, Isaribi muore una sola volta |
| 32 | 07-19 | [omega](2026-07-19_kiraya-vs-omega.yaml) | **W** | 14 | Viola/Rosso, Neo Zeon (Quess's Jagd Doga + Quess Paraya, Sazabi, Kshatriya + Marida Cruz, Rezin's Geara Doga, base Axis) | 5 / 1 | 10 / 6 | Vittoria per timeout dell'avversario da una posizione già dominante (0 shield perse); turno pesante al t10 (3 unità perse, tutto forzato dalla densità Blocker) recuperato subito al t11; probabile kill silenzioso di Sazabi non registrato dal parser; nessun errore tattico individuato |

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
- **Gundam Barbatos Lupus finalmente pescato e funzionante (game 4,
  vs iceberg)**, dopo 3 partite su 3 senza vederlo: doppia attivazione
  al t13 (uccide Chaos Gundam MA Mode) e una terza al t15 (uccide Chaos
  Gundam base), esattamente il pattern-chiusura già confermato su
  `aggro_mono_p`. Colma il buco di dati più insistente del campione
  finora — resta comunque solo 1 partita su 4 in cui il piano-finisher
  si è visto in azione.
- **Scarto forzato dalla mano (non dal campo) su Lupus/Gusion Rebake**
  (vs iceberg, t6 e t10: Gaia Gundam e Abyss Gundam MA Mode, entrambi
  effetti "l'avversario scarta 1"): ha tolto una copia viva di Lupus
  prima ancora che scendesse in campo. Il mazzo l'ha assorbito senza
  conseguenze (altra copia arrivata più tardi) — ma è una minaccia
  diversa dal removal/bounce già visti: colpisce la mano, non il board,
  quindi nessuna sequenza di gioco la previene.
- **Primo dato su Gundam Barbatos 5th Form (Ground Type)** (vs
  SaintAbbel): mai calato, scartato al t5 come costo dell'abilità di
  Ryusei-Go (pesca 1/scarta 1) — cioè trattato come lo scarto meno
  costoso in mano, non come una minaccia da giocare. La zona (Earth) non
  c'entra: non è un vincolo di gioco attuale (vedi CLAUDE.md), era
  semplicemente la carta più sacrificabile in quella mano. Nessun
  segnale ancora sulla sua reale giocabilità.
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
- **La vittoria vs SaintAbbel si è vinta sui numeri, non su un singolo
  colpo decisivo**: 0 shield perse contro le 6 dell'avversario, pur
  perdendo un'unità in più (5 vs 4) — lo stesso pattern "corsa alle
  shield vinta nonostante trade sfavorevoli" già visto ripetutamente in
  `aggro_mono_p`.
- **Bounce ripetuto su un corpo economico come forma di disinnesco**:
  SaintAbbel ha rimandato Gundam Exia Repair in mano 3 volte (t8, t11,
  t12: Perfect Strike Gundam's ability x2 + Exclusively Defense-Oriented
  Policy) invece di rimuoverlo. Effetto pratico identico al removal
  diretto di Darkness Finger visto contro MMorelli (un corpo economico
  che salta un turno intero di danno), ma via bounce invece che
  rimozione — variante dello stesso tema di inefficienza da tracciare.
- **Doppio pair/link di Mikazuki Augus nello stesso turno su due unità
  diverse** (t11: Link su 1st Form + Pair su Gusion Rebake): 2 ping da 1
  danno nello stesso turno per il solo costo del pilota, la linea di
  danno-passivo più efficiente vista finora nel campione v1_1.
- **Un terzo tipo di block-bypass, distinto da High-Maneuver** (vs liko,
  t14): Nu Gundam LR (GD05-017) inizia una battaglia direttamente dalla
  propria abilità When-Paired, saltando l'intera fase di
  dichiarazione/blocco — non è che il blocco sia vietato (come con
  High-Maneuver), è che lo step in cui sarebbe stato possibile non
  esiste affatto in quella sequenza. Ha ucciso sia Gundam Barbatos Lupus
  che Gundam Barbatos 2nd Form nello stesso turno. Il buco strutturale
  già documentato per High-Maneuver/Wing Zero non copre questo caso —
  è una terza famiglia di minaccia senza contromossa nel mazzo.
- **Seconda vera prova di Gundam Barbatos Lupus** (vs liko): la prima
  copia (t13) fa doppia attivazione ma muore alla battaglia-abilità di
  Nu Gundam prima di attaccare mai; la seconda (t17) fa doppia
  attivazione e sopravvive fino al t19, tradando in combattimento. Il
  piano-finisher regge quando ha un turno per agire indisturbato, molto
  meno se l'avversario ha in mano una risposta diretta.
- **Interwoven Blessings (comando costo 10, "distruggi le prime 2 carte
  nell'area shield nemica") ha distrutto Isaribi (una base in campo, non
  una shield) mentre l'area shield di Kiraya era già vuota** (t20 vs
  liko) — interazione da verificare con le regole ufficiali prima di
  darla per assodata, non ancora confermata come comportamento atteso.
- **Strike Freedom Gundam conferma di essere il problema strutturale
  numero 1 già visto in `aggro_mono_p`, e le 5 copie totali di
  Lupus/Lupus Rex in v1_1 non lo risolvono** (vs Robotech): la sua
  abilità rimanda l'unità nemica di livello più basso in campo, non una
  copia specifica — ha colpito Gundam Barbatos Lupus Rex al t14 (la
  singola copia del pezzo nuovo, mai arrivata ad attaccare) e Gundam
  Barbatos 1st Form al t16. Più copie nel mazzo non cambiano il fatto che
  l'unità più economica in campo in quel momento è sempre a rischio — la
  contromossa resta quella già in checklist (tenere un'unità ancora più
  economica viva insieme a Lupus/Lupus Rex), non il numero di copie.
- **Deficit di pesca ancora presente**: Robotech ha accumulato carte via
  A Show of Resolve, i "Draw a card" ripetuti di Strike Freedom Gundam
  (Deploy/Attack) e di Kira Yamato (When Linked) - lo stesso squilibrio
  strutturale già documentato in `aggro_mono_p/ANALISI.md` ("nessun
  motore di pesca/vantaggio carte"), non ancora affrontato in v1_1.
- **Scoperta di formato per gli import futuri**: il client a volte mostra
  un'unità Linked sotto un nome diverso da quello stampato
  (`<nome> (<Pilota>'s Unit)`), es. "Murasame (Andrew Waldfeld Unit)" è
  in realtà "Waldfeld's Murasame" — vedi CLAUDE.md, sezione data quirks.
- **Miglior prova finora di Gundam Barbatos Lupus come motore ricorrente**
  (vs GenocidGIC): 4 dispiegamenti distinti nella stessa partita (t13,
  t17, t21, t23), 7 uccisioni dirette totali, muore 2 volte e torna
  sempre grazie alle 4 copie nel mazzo. Prima partita in cui il
  piano-motore si vede funzionare a pieno regime per un'intera partita
  invece che in un singolo turno isolato.
- **Un turno di quasi-wipe non è per forza game over**: al t12 Unicorn
  Gundam 02 Banshee Norn (Destroy Mode) (GD04-065, stampa diversa da
  quella vista contro MMorelli) si riattiva 3 volte nello stesso turno
  e uccide Gundam Barbatos 1st Form tre volte più Hyakuren - board quasi
  azzerato. La partita è stata comunque vinta 11 turni dopo, grazie alla
  ridondanza del piano Lupus, non a una risposta diretta a quel turno.
- **Kindhearted ("le unità amiche non possono essere distrutte da
  effetti nemici questo turno" + pesca) è una risposta reale al piano di
  ping/ability-damage del mazzo** (Adapt, Gusion Rebake, Mikazuki
  Augus) - vista 2 volte (t15, t22). Non ha impedito la vittoria ma è
  la prima carta osservata pensata specificamente contro quel piano.
- **Basi che generano token** (Corsica Base, ST02-016): il suo Deploy
  crea automaticamente un Tallgeese token (AP4/HP2) quando è il turno
  del controllore — "X deployed" senza una riga di deploy-da-mano
  separata subito dopo "Played base: Y" è il segnale per riconoscerlo
  nei prossimi import, dato che il risolutore automatico preferisce le
  stampe reali quando esistono e va corretto a mano in questi casi.
- **Il piano-motore (Barbatos Lupus) non è indispensabile ogni partita**
  (rivincita vs GenocidGIC, game 8): vittoria netta (0 shield perse)
  senza che Lupus compaia mai in mano. Bilancia il timore emerso da
  sgd/SaintAbbel (prime 3 partite senza vederlo) — quando l'apertura con
  Exia Repair/corpi economici tiene il ritmo, il mazzo vince anche senza
  il finisher dedicato.
- **Stesso avversario, stesso giorno: pattern ripetuti confermano
  l'identità del mazzo ma non aggiungono nuove informazioni sulle
  stampe ambigue** (Gundam, Forbidden Gundam, Riddhe Marcenas restano
  irrisolte in entrambe le partite vs GenocidGIC, sempre per mancanza
  di prove dirette nel log, non per assenza di indizi circostanziali).
- **Scambio inefficiente segnalato** (game 8): entrambe le copie di
  Gundam Exia Repair spese nello stesso turno per uccidere un singolo
  Messala con Repair (2-per-1 sfavorevole in conteggio carte, anche se
  ogni copia ha comunque attivato il proprio mill-on-death) — da evitare
  quando è disponibile un'alternativa più efficiente.
- **Correzione importante (non solo su questa partita): il mazzo NON è
  privo di Blocker.** Sia Gundam Gusion Rebake (`<Blocker>` esplicito)
  sia Shiden Custom (Ryusei-Go) (stesso testo di redirect, funzionalmente
  identico — ha bloccato 10 volte nel campione) hanno la capacità di
  bloccare, e lo fanno regolarmente quando sono in campo e attivi
  (21 blocchi osservati in totale tra `aggro_mono_p` e v1_1). Il t7 vs
  dogman non era "il mazzo senza Blocker" — era che nessuna delle 6 copie
  totali (3+3 su 50 carte, 12%) era ancora stata pescata/schierata a
  quel punto della partita. Shiden Custom infatti blocca regolarmente
  più avanti nella stessa partita (t11). Il problema reale è di densità
  (12% del mazzo, non garantito entro il t7), non di assenza totale —
  va corretta ogni nota precedente che parlava di "mazzo senza Blocker"
  come limite strutturale assoluto.
- **Due ipotesi di errore ritrattate dopo revisione con Kiraya** (vs
  dogman): lo scarto di Gundam Barbatos Lupus al t12 (via Ryusei-Go) non
  era un rischio — ne aveva un'altra copia in mano. E il non aver
  attaccato con Shiden Custom al t10 non era un turno sprecato, ma una
  scelta deliberata per tenerlo attivo come blocco al turno successivo
  (dove infatti blocca, vedi sotto). Con queste due correzioni, questa
  sconfitta non ha errori tattici individuabili lato Kiraya — il t7 resta
  spiegabile solo dalla varianza di pesca (blocker non ancora disponibile).
- **Buona lettura del blocco quando la scelta è tra due bersagli**
  (vs dogman, t11): con un solo blocker disponibile per due attacchi
  dichiarati, bloccare l'unità che si può davvero uccidere (Nu Gundam,
  trade netto) invece di quella che sopravvivrebbe comunque al colpo
  (Gundam, con Repair 2 e HP5) — lasciando che una base sacrificabile
  assorba il colpo altrimenti inevitabile — è la sequenza corretta.
- **Prima vittoria per resa dell'avversario nel campione** (vs 112t,
  t14): non uno shield-out, ma una resa con Kiraya già a 4 shield contro
  1 e un board nettamente più sano — una posizione da cui la vittoria
  era comunque vicina indipendentemente dal singolo colpo finale. Stesso
  pattern di esecuzione pulita già visto altrove: attaccare le basi di
  valore (Girty Lue, t9) invece del player quando conviene, e spendere
  l'unico blocco disponibile sul trade che uccide qualcosa (t12) anche
  quando non salva l'unità originariamente minacciata.
- **Sconfitta-catalogo contro loclee**: quasi ogni problema strutturale
  già documentato converge in un solo avversario — Darkness Finger
  (rimozione ripetibile), Strike Freedom Gundam (bounce + pesca),
  Unicorn Gundam 02 Banshee (Destroy Mode) (First Strike + riciclo
  trash, stesso schema letale delle partite vs MMorelli in
  `aggro_mono_p`). Unico errore reale isolato in tutta la partita: al
  t14, attaccare con Gundam Barbatos 2nd Form contro un blocker noto
  (Strike Rouge Ootori) prima di verificare se Gundam Barbatos Lupus, da
  solo, sarebbe bastato a completare il kill (lo era: 4 danni contro
  HP4 piena) — un'unità sacrificata per un chip rivelatosi ridondante.
- **Seconda base che genera token dopo Corsica Base**: White Base
  (ST01-015) genera un token Gundam/Guncannon/Guntank in base a quante
  unità ha in campo il controllore quando attivata — stesso segnale già
  noto ("X deployed" subito dopo "Activated: <base> / Rested N
  Resources", senza deploy-da-mano separato) da riconoscere nei
  prossimi import.
- **Prima volta sopra il .500 nel campione (6-6)**: la vittoria più
  netta vista finora (0 shield perse, avversario già a shield zero un
  turno prima della fine). Lupus attivato una sola volta in tutta la
  partita (t13) ma basta a ripulire da solo entrambe le minacce rimaste
  — quando arriva in tempo il piano-motore chiude in fretta anche senza
  bisogno di ripetersi su più turni.
- **Widespread Annihilation (il board wipe generico) scartata come
  shield senza mai essere giocata** (vs gogogo, t11): pura variance, non
  un merito del mazzo — il buco strutturale contro un board wipe
  generico resta quello già documentato in `aggro_mono_p/ANALISI.md`
  (vs IAN), semplicemente non si è materializzato questa volta.
- **Prima vittoria sopra il .500 (7-6)**: partita pulita dall'inizio
  alla fine contro peachique, senza errori tattici individuabili e senza
  bisogno di Lupus (mai pescato). Turno di saturazione da manuale al
  t11 (4 attacchi nello stesso turno, zero bloccanti disponibili per
  l'avversario) — lo stesso principio già in checklist, eseguito bene.
- **Conferma ricorrente: le statistiche del pilota si sommano a quelle
  dell'unità quando è in coppia/Link, sia in AP che in HP** (osservato
  ormai in più partite, es. Nu Gundam AP4/5 + Amuro Ray AP2 = 6/7 danno
  esatto osservato più volte vs peachique; confermato anche sull'HP vs
  Essen, t22: Ryusei-Go a 1 HP sopravvive a un secondo ping da 1 solo
  perché Mikazuki Augus (HP1) gli si abbina nel mezzo, portandolo a 2
  HP residui invece di morire a 0). Non ancora trovata una regola
  esplicita nel Comprehensive Rules con `search_rules`, ma il pattern è
  consistente su entrambe le statistiche ed è lo strumento più
  affidabile per confermare quale stampa di un'unità/pilota è in gioco
  quando l'abilità da sola non basta.
- **Quarta coppia di stampe condivise nella stessa partita** (Nu Gundam,
  dopo Kira Yamato, Sword Impulse Gundam e il caso originale di Nu
  Gundam contro liko) — motivo in più per continuare a verificare
  l'abilità osservata invece di assumere che un nome ripetuto sia
  sempre la stessa stampa.
- **Activate "durante questo turno" sprecato su un'unità già rested**
  (vs TJL, t7): Isaribi buffa Ryusei-Go con AP+2, ma Ryusei-Go aveva
  già attaccato come primissima azione del turno — il bonus non ha
  potuto essere usato. Stesso identico errore-tipo già in checklist,
  ma è la prima volta che si osserva col bersaglio sbagliato per
  ordine-delle-azioni piuttosto che per tipo di unità: controllare
  *quando* nel turno un'unità ha già agito, non solo *se* può
  beneficiare del danno.
- **Seconda conferma di Kira Yamato in due stampe diverse nella stessa
  partita** (dopo Robotech): la copia che applica un modificatore
  AP-2 durante la dichiarazione di battaglia (ST04-010) e quella che
  pesca al Link (GD05-081) continuano a essere distinguibili con
  sicurezza dall'abilità osservata, mai dal colore (entrambe le stampe
  restano legali nei mazzi Blu/Bianco visti finora).
- **Non tutte le sconfitte hanno un errore da correggere** (vs Essen):
  revisione richiesta esplicitamente da Kiraya convinto di aver perso
  per proprio demerito, ma senza una sequenza di gioco individuabile
  come sbagliata — board dell'avversario vuoto fino al t13, ogni unità
  di Kiraya morta a un comando diretto (mai in un trade evitabile), e
  Lupus usato correttamente sia quando aveva un bersaglio (t14, t20)
  sia quando non ne aveva (t18, giustamente non attivato). La mano di
  rimozione/pesca di Essen è la più pesante vista nel campione finora —
  persino più di loclee (partita 11) — e il bounce di Strike Freedom ha
  colpito Lupus entrambe le volte non per una scelta di sequenza ma
  perché la rimozione avversaria aveva già eliminato ogni altro corpo
  che potesse fare da bersaglio alternativo. Stesso principio già
  applicato a やーこん in `aggro_mono_p/ANALISI.md`: distinguere "ho
  giocato male" da "l'avversario aveva la risposta in mano" resta
  importante anche quando chi gioca sospetta il contrario.
- **Terza/quarta conferma del block-bypass come buco strutturale
  ricorrente** (vs xDEADHEADx, t8/t10): Char's Zaku Ⅱ linkato a Char
  Aznable (ST03-011) ottiene High-Maneuver a ogni attacco — stessa
  famiglia di Chaos Gundam+Sting Oakley (sgd) e Wing Gundam Zero (liko).
  Tre avversari diversi, stesso meccanismo, zero contromisura nel mazzo
  in tutti e tre i casi.
- **Un'abilità "distruggi un'unità nemica" può fallire a vuoto per
  condizioni di targeting, non solo per assenza di bersagli** (vs
  xDEADHEADx, t16): l'Attack di Sazabi (GD05-049) avrebbe dovuto forzare
  Kiraya a sacrificare un'unità "non impegnata in combattimento", ma
  Gundam Barbatos Lupus — l'unica unità di Kiraya in campo — era
  proprio quella sotto attacco in quel momento, quindi non qualificava.
  Vale la pena ricordarlo leggendo abilità simili in futuro: il
  wording esatto della condizione conta quanto la sua presenza.
- **La causa percepita di una sconfitta non sempre è quella reale** (vs
  jaysanti): Kiraya ha attribuito la perdita all'High-Maneuver, ma il log
  non ne contiene nessuna istanza - la partita si è decisa su un errore
  di blocco isolato (t14: 2 Shiden Custom (Ryusei-Go) attivi non usati
  contro Master Asia, che avrebbe fatto un trade netto invece di uccidere
  Hyakuren a gratis) più fattori strutturali già noti (Lupus mai pescato
  per doppio mill dal proprio Exia Repair) e uno nuovo (vedi sotto).
  Stesso principio già applicato a Essen: distinguere la diagnosi
  istintiva del giocatore da quella confermata riga per riga nel log.
- **Nuova variante del problema-Blocker: il blocker può esserci ed essere
  comunque disinnescato prima di scegliere** (vs jaysanti, t12/t16):
  Domon Kasshu e poi Master Asia, appaiati su Rising Gundam, restano
  Shiden Custom (Ryusei-Go)/Hyakuren tramite la propria abilità (assieme
  a Shining Finger scartata dalla mano) prima della fase di combattimento
  - risultato "No blockers available" anche se le carte erano fisicamente
  in campo e attive a inizio turno. Distinto dal problema di densità già
  in checklist (item 5): qui il blocker c'era, è stato reso inutile da un
  effetto mirato dell'avversario.
- **Prima doppia attivazione di Barbatos Lupus nello stesso turno** (vs
  desi, t15): la seconda copia di Lupus in campo si attiva due volte
  consecutive (6 carte esiliate in tutto), concatenando 2 ping da 2 danni
  con un attacco di Barbatos Adapt in mezzo per finire un solo bersaglio
  (Gundam AGE-2 Double Bullet, HP5) invece di disperdere il danno su più
  bersagli - tre attivazioni totali nella stessa partita (t13 + t15 x2) da
  due copie distinte, la miglior prova finora del piano-motore ripetuto
  entro una singola partita.
- **Quinta coppia di stampe condivise nella stessa partita** (vs desi,
  dopo Nu Gundam, Kira Yamato, Sword Impulse Gundam, Sazabi): Amuro Ray in
  due print diverse nello stesso turno (t14), distinguibili solo
  dall'abilità osservata (rest su unità nemica <=5 HP vs cura 2 HP
  all'unità abbinata alla distruzione di un nemico), mai dal nome o dal
  colore.
- **Vittoria per timeout, non per shield-out naturale** (vs desi, t18):
  l'avversario esaurisce il tempo a disposizione con ancora 1 shield
  residua - una categoria di vittoria distinta dallo shield-out pulito e
  dalla resa vista contro 112t, anche se la posizione di Kiraya (4 shield
  contro 1) era comunque già decisamente favorevole indipendentemente dal
  timeout.
- **Terza doppia attivazione di Lupus nello stesso turno, seconda partita
  di fila** (vs Olo, t13, dopo desi t15): la copia appena schierata si
  attiva due volte consecutive (6 carte esiliate), concatenando i ping
  con Become a Shield per abbattere un bersaglio quasi a zero e aprire la
  strada a 2 attacchi diretti sulla base nemica. Comincia a sembrare
  un'esecuzione intenzionale ricorrente più che un'eccezione isolata.
- **Variante inedita del bounce di Strike Freedom Gundam** (vs Olo, t16):
  l'unità di livello più basso in campo (Graze Custom) viene "returned to
  deck" invece che rimandata in mano come nelle partite precedenti
  (Robotech, Essen) - un effetto ancora più punitivo, non è nemmeno
  ripescabile a comando. Da verificare se è una stampa diversa
  dell'abilità o solo un wording di log incoerente tra partite.
- **Terza conferma diretta del quirk di visualizzazione Linked-unit già
  in CLAUDE.md** (vs Olo): "Strike Rouge (Kira's Unit)" è la stessa
  istanza citata come esempio nelle istruzioni del progetto - risolta a
  Kira's Strike Rouge (GD05-010) con piena conferma aritmetica di
  combattimento.
- **Vittoria completa senza né il piano-motore né il pacchetto Blocker**
  (vs MrCross00): Barbatos Lupus mai pescato, Gusion Rebake/Shiden Custom
  mai visti - la partita si vince comunque in 13 turni sulla sola
  pressione d'apertura (Graze Custom, Barbatos Adapt, Flauros Ryusei-Go),
  0 shield perse ed EX Base mai distrutta. Stesso principio già visto
  nella rivincita vs GenocidGIC (game 8): nessuno dei due pilastri è
  indispensabile quando la curva iniziale tiene il ritmo.
- **Identità ambigua di "Gundam" — risolta in tutti e tre i casi**
  (aggiornamento finale 2026-07-19, dopo una correzione di un mio
  errore segnalata da Kiraya): è sempre ST01-001, la differenza tra le
  partite era solo quale stampa di Amuro Ray fosse abbinata e se il
  【During Pair】di ST01-001 ("i tuoi Units ottengono AP+1 durante il tuo
  turno") fosse attivo. Vs desi e vs Juuto, abbinato a ST01-010 (AP2/HP1
  propri): AP3+2+1(buff, turno avversario)=6 quando attacca, AP3+2+0
  (turno di Kiraya, buff inattivo)=5 quando difende - entrambi esatti.
  Vs MrCross00, abbinato a GD05-085 (quella con la cura - il cui vero
  bonus è +2/+2, NON 0/0: avevo scritto per errore che fosse
  genuinamente 0/0 in un mio passaggio precedente, corretto da Kiraya):
  AP3+2+1(buff, sempre turno di MrCross00 in questa partita)=6 esatto
  entrambe le volte, HP4+2=6 totali coerenti con ogni numero osservato.
  Nessun mistero residuo su questa carta.
  - "Gundam" potrebbe essere davvero GD04-008 (AP4+2=6 esatto) con la
  prova del Repair-2 da rivedere come coincidenza o interazione non
  ancora chiara.
- **Ennesima conferma che un turno di quasi-wipe non è game over** (vs
  Nate, t10): Kiraya perde 3 unità nello stesso turno (Barbatos 1st Form,
  Hyakuren, Ryusei-Go Graze Custom II) senza mai avere un blocco
  disponibile, ma chiude comunque al turno successivo con 4 attacchi non
  contrastati. Stesso principio già visto vs GenocidGIC (t12) e Robotech.
- **Vittoria col piano-motore morto in partenza** (vs Nate): sia Gundam
  Barbatos Lupus che Gundam Barbatos Adapt finiscono milled dal proprio
  Gundam Exia Repair già al t7 (stesso turno di apertura) - il finisher
  dedicato non è mai stato disponibile per l'intera partita, eppure la
  sola pressione da corpi economici (Exia Repair, Graze Custom x2,
  Ryusei-Go, Hyakuren, Flauros) ha chiuso in 11 turni netti.
- **Non tutte le sconfitte hanno un errore da correggere, di nuovo** (vs
  KUMA): revisione richiesta esplicitamente da Kiraya convinto di aver
  perso per propri errori, ma un'analisi turno per turno non trova
  nessuna sequenza chiaramente sbagliata - il candidato piu vicino (t7:
  due self-ping consecutivi sullo stesso Barbatos 2nd Form invece di
  scaricarne uno sul gia fragile Ryusei-Go II) non ha cambiato l'esito:
  l'unita muore comunque al t8 a un attacco che ne supera gli HP totali,
  e il danno di ritorno dipende dal suo AP, non dagli HP residui. Stesso
  principio gia applicato a Essen.
- **Combo debuff-poi-distruggi intenzionale, non fortuita** (vs KUMA,
  t6): Gundam Heavyarms Custom (EW) attiva un AP-1 su Gundam Exia Repair
  (AP2->1) esplicitamente per farlo qualificare come bersaglio legale del
  Deploy di GN Armor Type-E ("distruggi un'unita nemica Lv.1 o meno o con
  1 o meno AP") - sequenziamento deliberato, non un colpo di fortuna.
- **Doppia copia dello stesso debuffer ripetibile** (vs KUMA): 2 copie di
  Gundam Heavyarms Custom (EW) attivano AP-1 ogni turno ciascuna, mentre
  Gundam Sandrock Custom (EW) applica un AP-2 ripetibile ad ogni sua
  dichiarazione d'attacco - un volume di debuff cumulativo mai visto
  finora nel campione v1_1, distinto dal removal diretto gia catalogato
  (Darkness Finger) perche non consuma la carta, si ripete ogni turno.
- **Quinta+ conferma della tech "blocker disinnescato prima di
  scegliere"** (vs KUMA, t12, dopo jaysanti): Wing Gundam Zero (EW) resta
  Gundam Gusion Rebake con la propria abilita prima che possa essere
  assegnato come blocco - stessa famiglia della tech di Domon/Master Asia
  su Rising Gundam vista due partite fa.
- **Motore di pesca incidentale piu prolifico del campione** (vs
  Sakurah): l'abilita Attack di Gundam Barbatos 1st Form (pesca 1) si
  attiva almeno 6 volte in una singola partita grazie a piu copie in
  rotazione (t9 x2, t11 x2, t13 x2) - non e un vero motore dedicato di
  card-advantage (il problema resta in checklist), ma mostra quanto la
  sola densita di copie di una carta con quell'abilita possa avvicinarsi
  all'effetto di un motore di pesca strutturale.
- **Enigma aritmetico AP/HP di Nu Gundam risolto** (vs Sakurah, poi
  confermato vs Kumendeng): la copia che infligge 7 danni e ha HP totale
  7 è GD05-017 (AP5/HP5) abbinato ad Amuro Ray GD05-085, il cui bonus
  reale è +2/+2 (5+2=7 su entrambe le statistiche, esatto) - il database
  locale aveva GD05-085 sincronizzato erroneamente come AP0/HP0
  dall'unica fonte disponibile per GD05 (egmanevents, apitcg non ha
  ancora questo set), corretto il 2026-07-18 dopo conferma via immagine
  ufficiale della carta. Il caso analogo di "Gundam" vs desi/MrCross00
  è stato risolto separatamente più avanti (vedi la voce più recente
  su questo stesso rompicapo, sotto) - non dallo stesso fix.
- **Terzo caso della stessa giornata di due stampe di Amuro Ray nella
  stessa partita** (dopo desi e MrCross00): stesso pattern di sempre,
  GD05-085 (cura su distruzione) e ST01-010 (rest su unita nemica).
- **Possibile problema sistemico nei dati dei piloti del set GD05** (vs
  Bugs): Kira Yamato (GD05-081) risultava anch'esso sincronizzato come
  AP0/HP0, stesso errore gia trovato su Amuro Ray (GD05-085) - confermato
  via immagine ufficiale e corretto anche questo (+2/+2 reale). Su 21
  piloti GD05 nel database locale, 18 mostrano AP0/HP0 (inclusi questi
  due prima della correzione); non tutti sono necessariamente sbagliati
  (es. Sting Oakley mostra correttamente 1/1), ma con 2 conferme su 2
  controllati vale la pena verificare via immagine ufficiale ogni volta
  che l'aritmetica di un pilota GD05 non torna, prima di lasciarlo
  ambiguo.
- **Turno di sfondamento 2-per-2** (vs Bugs, t9): Barbatos 2nd Form e
  Barbatos Adapt eliminano entrambe le minacce principali dell'avversario
  (Strike Rouge Ootori bloccante e Strike Rouge Kira's Unit) nello stesso
  turno, pur perdendo entrambe le proprie unita nel trade - efficiente
  nonostante il pareggio numerico di carte.
- **Aggiornamento (2026-07-19): tutti i 21 piloti del set GD05 nel
  database locale sono stati controllati manualmente via immagine
  ufficiale.** Solo Sting Oakley aveva il dato corretto; tutti gli altri
  20 (compresi Amuro Ray e Kira Yamato gia corretti in precedenza)
  avevano un bonus AP/HP sbagliato, quasi sempre sincronizzato come 0/0
  dall'unica fonte disponibile per questo set (egmanevents - apitcg non
  ha ancora GD05). Tutti corretti in data/cards/en/gd05.json il
  2026-07-19. Le partite piu vecchie di questa sessione che coinvolgono
  questi piloti (jaysanti/Master Asia, Olo/Domon Kasshu, KUMA/Heero
  Yuy+Quatre Raberba Winner, Kumendeng/Char Aznable, tra le altre) non
  sono state riaudited retroattivamente - i loro appunti di
  aritmetica potrebbero essere superati se rivisitati.
- **Primo mirror-match parziale del campione** (vs Eshaku): l'avversario
  gioca lo stesso nucleo Tekkadan (Barbatos 1st Form, Barbatos Adapt,
  Hyakuren, Mikazuki Augus) con innesti Zeon/UC/Clan (Sazabi, Kshatriya,
  GQuuuuuuX Omega Psycommu) - la prima volta che l'identita delle carte
  ambigue ha richiesto di distinguere copie di ENTRAMBI i giocatori
  invece che solo dell'avversario.
- **Terza e piu estrema istanza di attivazioni multiple di Barbatos
  Lupus nello stesso turno** (vs Eshaku, t14): la stessa copia si attiva
  TRE volte consecutive (9 carte esiliate), spazzando via un intero
  Gundam Barbatos Adapt nemico da sola in tre ping successivi - il
  pattern gia visto vs desi/Olo/Kumendeng ma mai a questa scala.
- **Avversario piu orientato alla rimozione diretta pura vista finora
  in v1_1** (vs Eshaku): 2x Close Combat, 2x Improved Technique, Battle
  of Aces - cinque effetti di rimozione diretta in 24 turni, in un mazzo
  che corre anche lo stesso nucleo Tekkadan di Kiraya, rendendo la
  partita insolitamente simmetrica rispetto al resto del campione.
- **Quarta famiglia di block-bypass, la più letale vista finora** (vs
  Juuto): l'abilità When Paired di Nu Gundam (GD05-017, "esilia 3 carte
  Londo Bell dal trash, poi inizia una battaglia diretta contro
  un'unità scelta, saltando dichiarazione e blocco") non solo bypassa il
  blocco come già visto una volta con questa stessa carta (vs liko), ma
  SCEGLIE il bersaglio - usata due volte in questa partita (t14, t18)
  per eliminare Gundam Barbatos Lupus non appena rischierato, ogni
  volta innescando anche il suo <Breach 5> e distruggendo Isaribi nello
  stesso colpo. A differenza di High-Maneuver/Wing Zero/Nu Gundam LR
  (When-Paired generico), qui il bersaglio è una scelta dell'avversario,
  non casuale - il finisher del mazzo è specificamente a rischio ogni
  volta che l'avversario ha un Nu Gundam LR pronto e 3 carte Londo Bell
  in trash (cosa che si accumula naturalmente).
- **Non tutte le sconfitte hanno un errore da correggere, ancora una
  volta** (vs Juuto): revisione richiesta esplicitamente da Kiraya
  convinto di propri errori multipli, ma nessuna sequenza di gioco
  chiaramente sbagliata trovata - la partita si è decisa per intero
  sulla tech ripetibile sopra descritta. Stesso principio già applicato
  a Essen e KUMA.
- **Buona lettura del non-blocco quando entrambi gli esiti sono
  equivalenti** (vs Juuto, t16): con due copie identiche di Gundam
  Gusion Rebake in campo, non bloccare l'attacco su una delle due lascia
  che l'altra sopravviva per il turno successivo, dato che bloccare
  avrebbe comunque significato perdere una copia allo stesso modo - la
  scelta cambia SOLO quale copia sopravvive, non se una sopravvive.
- **Perdite individuali non fermano il ritmo se la pressione regge**
  (vs 1231): 3 unità perse a rimozione diretta avversaria (2x Signs of a
  Revolution, self-ping di Rewloola) non impediscono di chiudere l'EX
  Base al t7 e la base sostitutiva al t9 - resa dell'avversario al t10
  con Kiraya a 0 shield perse. Variante compatta dello stesso principio
  già visto più volte (GenocidGIC, MrCross00): il mazzo aggro non ha
  bisogno di mantenere in vita ogni unità, basta che il ritmo di danno
  netto resti positivo.
- **Seconda conferma ravvicinata del block-bypass-a-bersaglio-scelto di
  Nu Gundam (GD05-017)** (vs miii, t12, dopo Juuto): usato una sola
  volta ma con lo stesso identico effetto composto (uccide un'unità E
  fa scattare Breach 5 sulla base) - due partite di fila nella stessa
  settimana rendono questa carta specifica una minaccia da tenere
  presente esplicitamente, non solo un'altra variante generica di
  block-bypass.
- **Isaribi distrutta due volte nello stesso turno** (vs miii, t12): un
  singolo turno avversario innesca Breach 5 (distrugge Isaribi), poi
  Burst rimpiazza subito una copia dalla propria area shield, che viene
  distrutta di nuovo da un secondo Breach (2) nello stesso turno -
  variante estrema del collo di bottiglia della base singola già in
  checklist, qui raddoppiato entro un solo turno invece che diluito
  su più turni.
- **La partita più equilibrata del campione finora** (vs CE1117):
  entrambi i giocatori chiudono a 3 shield perse su 3, 0-0 - decisa
  letteralmente dall'ultimo pezzo. Nessun errore tattico individuato
  dopo revisione; la differenza è stata la velocità di ricostruzione
  del motore League Militaire avversario (Victory Gundam in più stampe,
  A Show of Resolve, doppio Overflowing Affection) dopo che una tripla
  attivazione di Lupus al t21 aveva eliminato sia Strike Freedom Gundam
  che Victory Gundam in un colpo solo.
- **Seconda conferma della variante "returned to deck" del bounce di
  Strike Freedom Gundam** (vs CE1117, dopo Olo): non un caso isolato -
  la stessa abilità può rimandare l'unità bersaglio nel mazzo invece che
  in mano, un effetto ancora più punitivo perché non è nemmeno
  ripescabile a comando.
- **Un altro caso del rompicapo "Gundam" risolto con lo stesso metodo**
  (vs tinki): stavolta abbinato a Kira Yamato (ST04-010) invece che
  Amuro Ray - AP3+2(Kira)+1(During Pair, proprio turno)=6 esatto, stessa
  meccanica già confermata su desi/MrCross00/Juuto ma con un pilota
  diverso, a conferma che la spiegazione è generale e non specifica di
  un singolo abbinamento. **Correzione**: avevo ipotizzato che una
  seconda copia nella stessa partita non ricevesse il bonus HP del
  pilota perché abbinata via "Paired" invece di "Linked" - ipotesi
  sbagliata, corretta da Kiraya (la somma delle statistiche non dipende
  da questa distinzione). Il dato scoperto sull'HP resta, ma senza una
  spiegazione meccanica proposta - più probabile un errore mio
  nell'attribuire le righe di log alla copia fisica corretta quando
  due unità omonime sono in campo, non un'eccezione reale alla regola.
- **Meccanica chiarita da Kiraya, con conferma nel regolamento
  ufficiale (regola 3-3-8-1): un pilota abbinato somma SEMPRE il
  proprio AP/HP all'unità, senza distinzione tra Paired e Linked.**
  Questo ha permesso di risolvere retroattivamente anche il vecchio
  mistero di Wing Gundam vs liko (partita 5): Heero Yuy è ST02-010, il
  cui box stampato (+2/+1) si somma a una SECONDA abilità testuale
  ("During Link: AP+1/HP+1") che scatta solo quando l'abbinamento è un
  vero Link (non un Pair generico) - la distinzione Paired/Linked conta
  quindi per le abilità testuali condizionate al Link, non per la somma
  base delle statistiche del pilota (regola 3-3-9-2). Con entrambi i
  bonus: AP4+2+1=7, HP5+1+1=7 - tornano esatti, mistero chiuso.

## Rompicapi aritmetici tuttora aperti

- Nessuno al momento (2026-07-19). Tutti i casi di "danno osservato
  non spiegabile dalle statistiche stampate" incontrati finora nel
  campione sono stati ricondotti o a dati sbagliati nel database
  locale (piloti GD05/GD04 sincronizzati come 0/0, poi corretti) o a
  meccaniche di gioco chiarite (bonus del pilota sempre sommato;
  abilità "During Link" come bonus aggiuntivo condizionato). L'unico
  residuo (la seconda copia di "Gundam" vs tinki, partita 31) è quasi
  certamente un errore di attribuzione mio tra due copie omonime nello
  stesso turno, non un'eccezione alla regola.
- **Probabile kill silenzioso non registrato dal parser** (vs omega,
  t11): Sazabi arriva a 1 HP dopo un trade, poi riceve un secondo ping
  da 1 danno (Become a Shield) che dovrebbe ucciderlo, ma il log non
  mostra mai "now destroyed" e la carta sparisce dal resto della
  partita - stesso pattern già documentato in CLAUDE.md (kill da ping
  multi-target talvolta non loggato come distruzione dal client).
- **Interazione Sazabi (GD05-052) + Quess's Jagd Doga confermata** (vs
  omega, t8): il Deploy di Sazabi distrugge un'altra unità propria come
  costo, e se quella unità è Quess's Jagd Doga la sua stessa abilità
  Destroyed la rimanda in mano (distrutta da un effetto Neo Zeon amico)
  - due ritorni in mano nello stesso turno per due motivi indipendenti.

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
5. Il mazzo ha solo 2 carte con capacità di blocco (Gundam Gusion
   Rebake, Shiden Custom Ryusei-Go — 6 copie su 50, 12%): se nessuna
   delle due è ancora in campo quando arriva un turno con più attacchi
   consecutivi, va subito per intero. Non è "il mazzo non blocca mai" —
   tienile a mente come prima priorità di schieramento/mantenimento in
   vita contro un avversario che sta sviluppando un board minaccioso.
6. Con effetti "pesca 1, poi scarta 1" (Ryusei-Go e simili): scartare
   una copia di Lupus/Lupus Rex va bene se se ne ha un'altra in mano —
   il rischio reale è solo quando è l'ultima copia rimasta.
7. Tenere un'unità sana inattiva a fine turno per usarla come blocco al
   turno successivo è una scelta legittima, non un turno sprecato —
   valutare caso per caso se attaccare subito o riservarla alla difesa.