# MistyOceanBattleship

## Change Log

### Nov.6

- Websocket adapter (`adapter_main.py`) for connect, disconnect and next round
- Integrate `manual.md` into this `README.md`

### Nov.2

Implemented functionalities of 5 types of artillery

### Nov.1

- Add manual.md
- Defined stats of 5 types of artillery in `utils/Artillery.py`

## Command Lists

- `next`
  - End current round

- `move { unit_index [0,) } { direction str }`
  - move the specified unit at the specified direction on the grid by one block
    - Direction: { up, down, left, right }
    - e.g. `move 0 down` -> move the capital ship down by one block

- `attack { unit_index [0,) } { target_index [0, 24] }`
  - The specified unit of current player attcks the target block on the opponent's board
  - e.g. `attack 1 20` -> unit 1 attack enemy's position 20

- `equip { unit_index [0,) } { artillery_type [?] }`
  - Equip the specified unit with the artillery
  - e.g. `equip 1 4` -> unit 1 equip artillery type 4

- `invoke`
  - Invoke active skill of current player's capital ship

### Format of Reponse

Some ideas

- Status: whether the commend was successful
- Current board
- Units status
- Fuel & bank
- Inventory of artilleries
- Game status: still running or game over
- Winner
- Messeage

## JSON Schema for Networking

### `Action.CONNECT`

```json
{
    "action": "connect",
    "info":
    {
        "name": "Player",
        "init_capital_ship_pos": 1,
        "init_war_ship_1_pos": 2,
        "init_war_ship_2_pos": 3
    }
}
```

在connect之后的所有请求都要带上connect返回的房间号（`id`）。

### `Action.DISCONNECT`

```json
{
    "action": "disconnect",
    "id": 0
}
```

### `Action.NEXT`

```json
{
    "action": "next",
    "id": 0
}
```

### `Action.ATTACK`

```json
{
    "action": "attack",
    "id": 0,
    "unit_index": 0,
    "target_index": 0
}
```

### `Action.EQUIP`

```json
{
    "action": "equip",
    "id": 0,
    "unit_index": 0,
    "artillery_type": 1
}
```

### `Action.INVOKE`

```json
{
    "action": "invoke",
    "id": 0
}
```

### `Action.MOVE`

```json
{
    "action": "move",
    "id": 0,
    "unit_index": 0,
    "direction": "down"
}
```

### Query Game Status

```json
{
    "action": "query",
    "id": 0
}
```

### JSON Response

#### Invalid Request

```json
{
    "status_code": 400,
    "msg": "some error message"
}
```

#### Failed Valid Request

```json
{
    "status_code": 200,
    "is_command_success": false,
    "msg": "some error message"
}
```

#### Successful Valid Request

```json
{
    "status_code": 200,
    "is_command_success": true,
    "msg": "",
    "result": {}
}
```

`Action.DISCONNECT`没有`result`。
