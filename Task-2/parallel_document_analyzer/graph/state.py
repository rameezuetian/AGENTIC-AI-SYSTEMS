from typing import List, TypedDict , Annotated
import operator
class DocumentState(TypedDict):
    document : str
    summary : str
    topics : str
    sentiment : str
    report : str
    trace : Annotated[List[str], operator.add]