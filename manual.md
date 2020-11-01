"next"
    End current round 
        

"move {unit_index [0,) } {direction str }"
    move the specified unit at the specified direction on the grid by one block
        Direction: { up, down, left, right }
        e.g. "move 0 down" -> move the capital ship down by one block

"attack {unit_index [0,) } {target_index [0, 24] }"
    The specified unit of current player attcks the target block on the opponent's board

"equip {unit_index [0,) } {artillery_type [?]} "
    Equip the specified unit with the artillery

"invoke"
    Invoke active skill of current player's capital ship


=================
Format of Reponse:
    TBD
    ideas: 
        status: whether the commend was successful
        current board
        units status
        fuel&bank
        inventory of artilleries
        game status: still running or game over
        winner

        