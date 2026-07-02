from pydantic import BaseModel


class TicketRequest(BaseModel):

    Priority: str
    Category: str
    Sub_Category: str
    Department: str
    Group: str
    Site: str
    Request_Type: str
    Created_Day: str
    Created_Month: str
    Created_Hour: int