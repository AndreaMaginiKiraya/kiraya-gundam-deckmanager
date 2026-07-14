# data/games/ — base conoscenza partite

Un file YAML per partita, generato dal tool MCP `import_game_log` a partire
dal log testuale del client di gioco (es. Mobile Suit Arena) e poi rifinito
a mano. I record sono indicizzati per mazzo dell'utente:
`<nome deck>/YYYY-MM-DD_<giocatore1>-vs-<giocatore2>.yaml` (es.
`aggro_mono_p/2026-07-14_kiraya-vs-tonii`), così tutte le partite di un
mazzo stanno nella stessa cartella; il mazzo è comunque registrato anche
dentro il record (`game.players.<utente>.deck`). Accanto a ogni `.yaml` il tool salva il log
grezzo come `.log`: è la fonte per rigenerare il record quando parser o
formato migliorano (`overwrite=True` riporta automaticamente id pinnati,
note personalizzate, `study_notes`, `result` e deck — vedi sotto).
`list_games` elenca i record salvati.

## Flusso

1. Incolla il log della chat a `import_game_log`, passando sempre il mazzo
   giocato dall'utente: `decks={"Kiraya": "<nome deck salvato>"}` (chiederlo
   se non dichiarato). Oltre a registrarlo nel record, la lista del deck
   risolve automaticamente le stampe ambigue delle carte di quel giocatore.
   Altri parametri: `result`, `overwrite`.
2. Il tool salva il record e riporta `cards_ambiguous`: i nomi condivisi da
   più stampe restano con `id: null` + `candidates`. Pinna a mano l'id
   giusto deducendolo da effetti/statistiche osservati nel log (aggiorna la
   `note` con l'evidenza usata).
3. Compila `study_notes` (il tool la lascia vuota): osservazioni
   strategiche ricavate dalla partita.
4. `unparsed_lines`, se presente, elenca le righe che il parser non ha
   riconosciuto: righe di quel tipo vanno aggiunte a `src/gamelog.py` (e al
   fixture `tests/fixtures/sample_game_log.txt`); poi si rigenera il record
   dal `.log` con `overwrite=True` senza perdere le annotazioni.

## Schema

- `game` — metadati: id, data import, `source` (header del client),
  `result` (`win:<player>` / `unknown`), e per giocatore first player,
  mulligan, colori dedotti dalle carte risolte, `deck` (nome in
  data/decks/ se passato).
- `cards` — indice "nome come appare nel log" → id del database, con
  statistiche, `owner`, contesti in cui è apparsa (`seen`) e `note` per
  ambiguità/evidenze. Usare `get_card` sull'id per i dettagli completi.
- `setup` — scelte pre-partita (first player, keep/mulligan).
- `turns` — turni con `active_player` e `actions` in ordine. Tipi:
  `deploy`, `pair_pilot` (con `linked` true/false), `play_base`,
  `play_command`, `activate`, `attack` (con `declared_target`,
  `modifiers`, `blockers`, `final_target`, `action_step` per i comandi
  giocati in risposta, `outcome`), `event`. Le righe di effetto restano
  testuali in `effects`/`outcome`, fedeli al log.
- `casualties` — distruzioni esplicite per giocatore (`{card, turn}`,
  cronologiche): solo quelle che il log dichiara con "now destroyed" —
  le morti implicite da ping cumulativi non compaiono (come nel log).
- `shields_tally` — EX Base e conteggio shield per giocatore a fine log
  (6 shield + EX Base in partenza); `shields_deployed` conta le shield
  uscite dall'area come Burst-deploy (es. basi come Nahel Argama).
- `study_notes` — osservazioni strategiche, scritte a mano dopo l'import.

I nomi carta nel log usano i numeri romani stampati (es. "Zaku Ⅱ"): la
ricerca nel DB li normalizza, quindi "Zaku II" funziona comunque.
