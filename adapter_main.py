import random
from pywss import Pyws, route
import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

from Game import Game
from Player import Player
from Utils import Ship


def random_ai_movements(game: Game) -> List[Dict[str, Any]]:
    movements = []

    ACTIONS = random.choices((
        ('invoke', game.Test_random_dissipate),
        ('move', game.move),
        ('attack', game.attack),
        ('equip', game.equip)
    ), k=2)

    for action_type, action_func in ACTIONS:

        if action_type == 'invoke':
            print('[RandomAI] invoke')
            success, msg = action_func()
            if success:
                movements.append({'action': 'invoke', 'msg': msg, 'result': game.to_json()})

        elif action_type == 'move':
            unit_index = random.randint(0, 2)
            direction = random.choice(('up', 'down', 'left', 'right'))
            print(f'[RandomAI] move {unit_index} {direction}')
            success, msg = action_func(unit_index, direction)
            if success:
                movements.append({
                    'action': 'move',
                    'unit_index': unit_index,
                    'direction': direction,
                    'msg': msg,
                    'result': game.to_json()
                })

        elif action_type == 'attack':
            unit_index = random.randint(0, 2)
            target_index = random.randint(0, 24)
            print(f'[RandomAI] attack {unit_index} {target_index}')
            success, msg = action_func(unit_index, target_index)
            if success:
                movements.append({
                    'action': 'attack',
                    'unit_index': unit_index,
                    'target_index': target_index,
                    'msg': msg,
                    'result': game.to_json()
                })

        else: # action_type == 'equip'
            unit_index = random.randint(0, 2)
            artillery_type = random.randint(0, 4)
            print(f'[RandomAI] equip {unit_index} {artillery_type}')
            success, msg = action_func(unit_index, artillery_type)
            if success:
                movements.append({
                    'action': 'equip',
                    'unit_index': unit_index,
                    'artillery_type': artillery_type,
                    'msg': msg,
                    'result': game.to_json()
                })
    
    print('[RandomAI] next')
    game.next_round()
    return movements


def human_ai_movements(game: Game) -> List[Dict[str, Any]]:
    movements = []

    ACTIONS = {
        'next': game.next_round,
        'invoke': game.Test_random_dissipate,
        'move': game.move,
        'attack': game.attack,
        'atk': game.attack,
        'equip': game.equip,
        'quit': game.gameover
    }

    while True:
        try:
            game.draw()

            cmd = input('Your move: ').split()
            action = ACTIONS[cmd[0]]
            args = cmd[1:]
            is_success, msg = action(*args)
            print(msg)
            if is_success:
                if cmd[0] == Action.NEXT.value:
                    return movements
                if cmd[0] == Action.ATTACK.value:
                    movements.append({
                        'action': 'attack',
                        'unit_index': int(cmd[1]),
                        'target_index': int(cmd[2]),
                        'msg': msg,
                        'result': game.to_json()
                    })
                if cmd[0] == Action.MOVE.value:
                    movements.append({
                        'action': 'move',
                        'unit_index': int(cmd[1]),
                        'direction': cmd[2],
                        'msg': msg,
                        'result': game.to_json()
                    })
                if cmd[0] == Action.EQUIP.value:
                    movements.append({
                        'action': 'equip',
                        'unit_index': int(cmd[1]),
                        'artillery_type': int(cmd[2]),
                        'msg': msg,
                        'result': game.to_json()
                    })
                if cmd[0] == Action.INVOKE.value:
                    movements.append(
                        {'action': 'invoke', 'msg': msg, 'result': game.to_json()})

        except KeyError:
            print('Invalid move')


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

    @staticmethod
    def get_room_from_id(id: int) -> Optional['Room']:
        for r in Room.ROOMS:
            if id == r.id:
                return r
        return None

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


def connect_action_handler(client_action: Dict[str, Any]) -> Dict[str, Any]:
    try:
        room = Room.create_room(PlayerInfo.parse_player_info(client_action['info']))
        return {'status_code': 200, 'msg': 'game room created', 'id': room.id, 'game': room.game.to_json()}
    except KeyError as e:
        return {'status_code': 400, 'msg': f'KeyError: {str(e)}'}


def disconnect_action_handler(client_action: Dict[str, Any]) -> Dict[str, Any]:
    room = Room.get_room_from_id(client_action['id'])
    if 'id' not in client_action or room is None:
        return {'status_code': 400, 'msg': 'invalid room id'}

    Room.ROOMS.remove(room)
    return {'status_code': 200, 'msg': 'disconnected'}


def next_action_handler(client_action: Dict[str, Any]) -> Dict[str, Any]:
    room = Room.get_room_from_id(client_action['id'])
    if 'id' not in client_action or room is None:
        return {'status_code': 400, 'msg': 'invalid room id'}

    if not room.game.isRunning():
        return {'status_code': 200, 'is_command_success': False, 'msg': 'game over', 'room_id': room.id}

    if room.game.current_player() != room.player:
        return {'status_code': 200, 'is_command_success': False, 'msg': 'not your turn', 'room_id': room.id}

    is_success, msg = room.game.next_round()

    if not is_success:  # p.s. next round shouldn't fail
        return {
            'status_code': 200,
            'is_command_success': False,
            'msg': msg,
            'room_id': room.id
        }

    opponent_moves = random_ai_movements(room.game)

    return {
        'action_result': {
            'status_code': 200,
            'is_command_success': True,
            'msg': msg,
            'result': room.game.to_json(),  # result of own movement
        },
        'opponent_movements': opponent_moves,  # ai movements and their result
        'room_id': room.id
    }


def attack_action_handler(client_action: Dict[str, Any]) -> Dict[str, Any]:
    room = Room.get_room_from_id(client_action['id'])
    if 'id' not in client_action or room is None:
        return {'status_code': 400, 'msg': 'invalid room id'}

    if 'unit_index' not in client_action or 'target_index' not in client_action:
        return {'status_code': 400, 'msg': 'need specify unit_index and target_index', 'room_id': room.id}

    try:
        if not room.game.isRunning():
            return {'status_code': 200, 'is_command_success': False, 'msg': 'game over', 'room_id': room.id}

        if room.game.current_player() != room.player:
            return {'status_code': 200, 'is_command_success': False, 'msg': 'not your turn', 'room_id': room.id}

        is_success, msg = room.game.attack(
            client_action['unit_index'], client_action['target_index'])
        if not is_success:
            return {
                'status_code': 200,
                'is_command_success': False,
                'msg': msg,
                'room_id': room.id
            }

        return {
            'status_code': 200,
            'is_command_success': True,
            'msg': msg,
            'result': room.game.to_json(),
            'room_id': room.id
        }
    finally:
        room.game.draw()


def equip_action_handler(client_action: Dict[str, Any]) -> Dict[str, Any]:
    room = Room.get_room_from_id(client_action['id'])
    if 'id' not in client_action or room is None:
        return {'status_code': 400, 'msg': 'invalid room id'}

    if 'unit_index' not in client_action or 'artillery_type' not in client_action:
        return {'status_code': 400, 'msg': 'need specify unit_index and artillery_type', 'room_id': room.id}

    if not room.game.isRunning():
        return {'status_code': 200, 'is_command_success': False, 'msg': 'game over', 'room_id': room.id}

    if room.game.current_player() != room.player:
        return {'status_code': 200, 'is_command_success': False, 'msg': 'not your turn', 'room_id': room.id}

    is_success, msg = room.game.equip(
        client_action['unit_index'], client_action['artillery_type'])
    if not is_success:
        return {
            'status_code': 200,
            'is_command_success': False,
            'msg': msg,
            'room_id': room.id
        }

    return {
        'status_code': 200,
        'is_command_success': True,
        'msg': msg,
        'result': room.game.to_json(),
        'room_id': room.id
    }


def invoke_action_handler(client_action: Dict[str, Any]) -> Dict[str, Any]:
    room = Room.get_room_from_id(client_action['id'])
    if 'id' not in client_action or room is None:
        return {'status_code': 400, 'msg': 'invalid room id'}

    if not room.game.isRunning():
        return {'status_code': 200, 'is_command_success': False, 'msg': 'game over', 'room_id': room.id}

    if room.game.current_player() != room.player:
        return {'status_code': 200, 'is_command_success': False, 'msg': 'not your turn', 'room_id': room.id}

    is_success, msg = room.game.Test_random_dissipate()
    if not is_success:
        return {
            'status_code': 200,
            'is_command_success': False,
            'msg': msg,
            'room_id': room.id
        }

    return {
        'status_code': 200,
        'is_command_success': True,
        'msg': msg,
        'result': room.game.to_json(),
        'room_id': room.id
    }


def move_action_handler(client_action: Dict[str, Any]) -> Dict[str, Any]:
    room = Room.get_room_from_id(client_action['id'])
    if 'id' not in client_action or room is None:
        return {'status_code': 400, 'msg': 'invalid room id'}

    if 'unit_index' not in client_action or 'direction' not in client_action:
        return {'status_code': 400, 'msg': 'need specify unit_index and direction', 'room_id': room.id}

    if not room.game.isRunning():
        return {'status_code': 200, 'is_command_success': False, 'msg': 'game over', 'room_id': room.id}

    if room.game.current_player() != room.player:
        return {'status_code': 200, 'is_command_success': False, 'msg': 'not your turn', 'room_id': room.id}

    is_success, msg = room.game.move(client_action['unit_index'], client_action['direction'])
    if not is_success:
        return {
            'status_code': 200,
            'is_command_success': False,
            'msg': msg,
            'room_id': room.id
        }

    return {
        'status_code': 200,
        'is_command_success': True,
        'msg': msg,
        'result': room.game.to_json(),
        'room_id': room.id
    }


def query_action_handler(client_action: Dict[str, Any]) -> Dict[str, Any]:
    room = Room.get_room_from_id(client_action['id'])
    if 'id' not in client_action or room is None:
        return {'status_code': 400, 'msg': 'invalid room id'}
    
    return {
        'status_code': 200,
        'is_command_success': True,
        'msg': '',
        'room_id': room.id,
        'result': room.game.to_json()
    }


@route('/game')
def game(request, data) -> Dict[str, Any]:
    print("Raw message recv from /game",data)
    try:
        client_action: Dict[str, Any] = json.loads(data)
    except json.JSONDecodeError as e:
        return {'status_code': 400, 'msg': str(e)}

    if 'action' not in client_action:
        return {'status_code': 400, 'msg': 'invalid json; need specify action'}

    if client_action['action'] == Action.CONNECT.value:
        return connect_action_handler(client_action)
    elif client_action['action'] == Action.DISCONNECT.value:
        return disconnect_action_handler(client_action)
    elif client_action['action'] == Action.NEXT.value:
        return next_action_handler(client_action)
    elif client_action['action'] == Action.ATTACK.value:
        return attack_action_handler(client_action)
    elif client_action['action'] == Action.MOVE.value:
        return move_action_handler(client_action)
    elif client_action['action'] == Action.EQUIP.value:
        return equip_action_handler(client_action)
    elif client_action['action'] == Action.INVOKE.value:
        return invoke_action_handler(client_action)
    elif client_action['action'] == 'query':  # just get the game status
        return query_action_handler(client_action)
    else:
        return {'status_code': 400, 'msg': 'undefined action'}


if __name__ == "__main__":
    ws = Pyws(__name__, address='127.0.0.1', port=4399)
    ws.serve_forever()
