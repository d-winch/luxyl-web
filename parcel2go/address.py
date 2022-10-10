import re
from dataclasses import dataclass

@dataclass
class Address():
    """Class for creating an address"""
    contact_name: str
    #first_name: str
    #last_name: str
    email: str
    phone: str
    property: str
    street: str
    town: str
    county: str
    postcode: str
    country_iso_code: str = "GBR"
    country_id: int = 0
    
    # @property
    # def contact_name(self) -> str:
    #     return f"{self.first_name} {self.last_name}"
    
    @property
    def phoneno(self) -> str:
        return re.sub('/[^0-9]/is', '', self.phone)