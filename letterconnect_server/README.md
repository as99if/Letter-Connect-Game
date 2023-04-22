Letter Connect API
-------


Run server
---
From 'letterconnect-challenge-as99if' (root of test) directory

Install dependencies

        pip install -r letterconnect_server/requirements.txt

Run server on localhost        

        python -m letterconnect_server

Test server according to specs
---
From 'letterconnect-challenge-as99if' (root of test) directory
    
        pytest -v 


gamesPost
--

Creates a new game.

The request should contain the initial node layout. The allowed values for the node are: a/b/c. Returns the 
id of the game that has been successfully created. The id of each node MUST be sequentially assigned starting from 1, 
in the same order the nodes are provided.

        POST
        /games

Path parameters
        
        Name	                         Description
        -------------------------------------------------------------------------------------------------------
        body                                  {
                                                "nodes": [(3... 50)] The nodes the game 
                                                                    should contain. (List of str)
                                                }
        

Responses

        Status: 200 - The game was created succesfully
        Schema
            {
                "game-id": str
            }

        Status: 400 - Bad Request



gamesIdMovePost
--

Make a move. Takes two node ids (`from`, `to`).

        POST
        /games/{id}/move

Path parameters
        
        Name	                         Description
        ------------------------------------------------------------------------------
        id*                                     String


        body                                  {
                                                "from": int,
                                                "to": int
                                                }

Responses

        Status: 200 - OK
        Schema
            {
                "current-player": str,
                "nodes": [
                    {
                        "connections": list of int,
                        "id": int,
                        "type": str
                    },
                    ...
                    ...
                ],
                "winner": null
            }
        Winner is null until the game is over (there are no moves left).
        

        Status: 400 - game_is_over: the game is already completed. or 
                      invalid_move: the move does not respect the rules of the game.
        Schema
            {
                'error-type': corresponding error
            }
            



gamesIdGet
--



Gets game details.
The response object contains the current snapshot of the provided game.

        GET
        /games/{id}

Path parameters
        
        Name	                         Description
        -----------------------------------------------------------------------------
        id*                                  String
        The id of the game Required

Responses

        Status: 200 - OK
        Schema
            {
                "current-player": str,
                "nodes": [
                    {
                        "connections": list of int,
                        "id": int,
                        "type": str
                    },
                    ...
                    ...
                ],
                "winner": str
            }
        Winner is null until the game is over (there are no moves left).
        

        Status: 404 - Game not found
        Schema
            {
                'error-type': Game not found.
            }


