from enum import Enum


class OutputData(Enum):
    '''
    The list of the output data attributes, which correspond to table rows headers in .csv file,
    holding output data 
    '''
    NAME ='Název produktu'
    AMOUNT ='Zakoupené množství'
    NET_PER_ITEM ='Cena za kus bez DPH'
    NET_TOTAL ='Cena celkem bez DPH'
    GROSS_PER_ITEM ='Cena za kus s DPH'
    GROSS_TOTAL ='Cena celkem s DPH'
    STATUS ='Status'
    ERROR_MESSAGE = 'Popis chyby'


class InputData(Enum):
    '''
    The list of input data attributes. Relevant input products data will be accessed using these attributes.
    '''
    NAME = 'nazev'
    AMOUNT = 'mnozstvi'
    NET_PER_ITEM = 'cena'
    VAT = 'dph_sazba'


# VAT rates, used for calculation products gross prices
VAT_RATES =  {
    'zakladni': 21,
    'prvni_snizena': 15,
    'druha_snizena': 10,
}

class ErrorMessages(Enum):
    '''
    The list of error messages, used to inform the user when there is a mistake in input data
    E.x. wrong data type, missing product parameter etc.
    Used in DataConverter.data_validator()
    '''
    AMOUNT_INPUT_ERROR = 'Chybne zadani mnozstvi produktu: '
    VAT_RATE_INPUT_ERROR = 'Chybne zadani sazby DPH: '
    MISSING_PRODUCT_PARAM = 'U produktu chybi polozky: '
    PRODUCT_PRICE_ERROR = 'Chybne zadani ceny produktu bez DPH: '

