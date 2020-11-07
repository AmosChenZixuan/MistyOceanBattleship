from pywss import Pyws, route
import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

from Game import Game
from Player import Player
from Utils import Ship


class Action(Enum):
    CONNECT = 'connect'
    DISCONNECT = 'disconnect'
    NEXT = 'next'
    MOVE = 'move'
    ATTACK = 'attack'
    EQUIP = 'equip'
    INVOKE = 'invoke'


@dataclass
class PlayerInfo:
    name: str
    init_capital_ship_pos: int
    init_war_ship_1_pos: int
    init_war_ship_2_pos: int

    @staticmethod
    def parse_player_info(info: Dict[str, Union[str, int]]) -> 'PlayerInfo':
        return PlayerInfo(**info)


class Room:
    NEXT_ROOM_ID: int = 0
    ROOMS: List['Room'] = []

    @staticmethod
    def create_room(host: PlayerInfo) -> 'Room':
        room = Room(host, Room.NEXT_ROOM_ID)
        Room.ROOMS.append(room)
        Room.NEXT_ROOM_ID += 1
        return room

    def __init__(self, player: PlayerInfo, id: int) -> 'Room':
        self.player = Player(
            player.name,
            [
                Ship.CapitalShip(player.init_capital_ship_pos),
                Ship.WarShip(player.init_war_ship_1_pos, 15, 5),
                Ship.WarShip(player.init_war_ship_2_pos, 20, 3)
            ],
            []
        )
        self.ai = Player("ai", [Ship.CapitalShip(
            1), Ship.WarShip(2, 1, 1), Ship.WarShip(3, 1, 1)], [])
        self.game = Game(self.player, self.ai)
        self.id = id


def connect_action_handler(client_action: Dict[str, Any]) -> str:
    try:
        room = Room.create_room(
            PlayerInfo.parse_player_info(client_action['info']))
        return json.dumps({'status_code': 200, 'msg': 'game room created', 'id': room.id, 'game': room.game.to_json()})
    except KeyError as e:
        return json.dumps({'status_code': 400, 'msg': f'KeyError: {str(e)}'})


def get_room_from_id(id: int) -> Optional[Room]:
    for r in Room.ROOMS:
        if id == r.id:
            return r
    return None


def disconnect_action_handler(client_action: Dict[str, Any]) -> str:
    if 'id' not in client_action or (room := get_room_from_id(client_action['id'])) is None:
        return json.dumps({'status_code': 400, 'msg': 'invalid room id'})

    Room.ROOMS.remove(room)
    return json.dumps({'status_code': 200, 'msg': 'disconnected'})


def next_action_handler(client_action: Dict[str, Any]) -> str:
    if 'id' not in client_action or (room := get_room_from_id(client_action['id'])) is None:
        return json.dumps({'status_code': 400, 'msg': 'invalid room id'})

    room.game.next_round()
    game_status = room.game.to_json()

    # TODO: AI movement here
    opponent_action = "next"
    room.game.next_round()

    return json.dumps(
        {
            'status_code': 200,
            'msg': 'next round',
            'result': game_status,  # result of own movement
            'opponent_move':
            {
                'opponent_action': opponent_action,
                'game': room.game.to_json()  # result of opponent movement
            }
        }
    )


def attack_action_handler(client_action: Dict[str, Any]) -> str:
    if 'id' not in client_action or (room := get_room_from_id(client_action['id'])) is None:
        return json.dumps({'status_code': 400, 'msg': 'invalid room id'})

    if 'unit_index' not in client_action or 'target_index' not in client_action:
        return json.dumps({'status_code': 400, 'msg': 'need specify unit_index and target_index'})

    success, msg = room.game.attack(client_action['unit_index'], client_action['target_index'])
    if not success:
        return json.dumps({'status_code': 200, 'msg': msg})
    
    game_status = room.game.to_json()
    
    # TODO: AI movement here
    opponent_action = "next"
    room.game.next_round()

    return json.dumps(
        {
            'status_code': 200,
            'msg': 'attack',
            'result': game_status,  # result of own movement
            'opponent_move':
            {
                'opponent_action': opponent_action,
                'game': room.game.to_json()  # result of opponent movement
            }
        }
    )

@route('/game')
def game(request, data) -> str:
    try:
        client_action: dict = json.loads(data)
    except json.JSONDecodeError as e:
        return json.dumps({'status_code': 400, 'msg': str(e)}, ensure_ascii=False)

    if 'action' not in client_action:
        return json.dumps({'status_code': 400, 'msg': 'invalid json; need specify action'}, ensure_ascii=False)

    if client_action['action'] == Action.CONNECT.value:
        return connect_action_handler(client_action)
    elif client_action['action'] == Action.DISCONNECT.value:
        return disconnect_action_handler(client_action)
    elif client_action['action'] == Action.NEXT.value:
        return next_action_handler(client_action)
    elif client_action['action'] == Action.ATTACK.value:
        return attack_action_handler(client_action)
    else:
        return json.dumps({'status_code': 400, 'msg': 'undefined action'})


if __name__ == "__main__":
    ws = Pyws(__name__, address='127.0.0.1', port=4399)
    ws.serve_forever()
