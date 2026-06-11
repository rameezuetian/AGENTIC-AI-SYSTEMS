from typing import TypedDict , Annotated , List
import operator

class EssayState(TypedDict):
    topic : str
    essay : str
    score : int
    feedback : str
    iteration : int
    logs : Annotated[List[str] , operator.add]
    