# Kamisado project #

*student : Killian Evouna - 24330*

 ## Strategy : 
- Static dangerosity matrix :
    a matrix representing the number of reachable endpoints
    [2 -> 8]
- dynamic validity matrix : 
    a matrix representing the number of valid moves available 
    for the opponent for each color 
    (after the move has been played) [0 -> 12]

The heuristic simply consists of dividing the number 
of valid moves for a specific color by the number of reachable
endpoints. This value is then used as an indicator to know which
moves are more desirable. The lower the value is the more desirable
the move is. 

## Requirements :
- coverage

All the other libraries are built-ins or the code is written by myself

    
