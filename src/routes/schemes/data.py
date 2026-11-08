from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_id : str 
    chunk_size : Optional[int] = 1000
    overlap_size : Optional[int] = 150
    reset : Optional[int] = 0
    do_rest  : Optional[int] = 0

