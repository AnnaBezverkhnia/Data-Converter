from dataclasses import dataclass

from constants import InputData, VAT_RATES, OutputData, ErrorMessages


@dataclass
class DataConverter:

    data: list[dict]


    def data_validator(self) -> None:
        '''
        Method validates validates input data:
            1. data should contain 4 articles: [cena, mnozstvi, nazev, dph_sazba]
            2. the value of 'cena' article should be float
            3. the value of 'mnozstvi' should be int
            4. the value of 'dph_sazba' should hold one of the option: ['zakladni', 'prvni_snizena','druha_snizena']

        if any of the avove condition is not met:
            set item status to 'ERROR'
        otherwise:
            set the status to 'OK'
        '''

        for item in self.data:
            difference = None
            if len(item) != 4:
                actual_data_keys = item.keys()
                expected_data_keys = [item.value for item in InputData]
                difference = actual_data_keys ^ set(expected_data_keys)  # check if the input data contain all required attributes
                if difference and difference != {OutputData.STATUS.value}:
                    missing_params = ', '.join(difference)
                    item[OutputData.ERROR_MESSAGE.value] = (
                        f'{ErrorMessages.MISSING_PRODUCT_PARAM.value}{missing_params}'
                    )
                    item[OutputData.STATUS.value] = 'ERROR'
            elif type(item[InputData.AMOUNT.value]) is not int:
                item[OutputData.STATUS.value] = 'ERROR'
                item[OutputData.ERROR_MESSAGE.value] = (
                    f'{ErrorMessages.AMOUNT_INPUT_ERROR.value}{item[InputData.AMOUNT.value]}'
                )
            elif type(item[InputData.NET_PER_ITEM.value]) is not float:
                item[OutputData.STATUS.value] = 'ERROR'
                item[OutputData.ERROR_MESSAGE.value] = (
                    f' {ErrorMessages.PRODUCT_PRICE_ERROR.value}{item[InputData.NET_PER_ITEM.value]}'
                )
            elif item[InputData.VAT.value] not in VAT_RATES.keys():
                item[OutputData.STATUS.value] = 'ERROR'
                item[OutputData.ERROR_MESSAGE.value] = (
                    f'{ErrorMessages.VAT_RATE_INPUT_ERROR.value}{item[InputData.VAT.value]}'
                )
            else:
                item[OutputData.STATUS.value] = 'OK'

    def sort_out_items(self) -> None:
        
        ''' method allows removing dublicated products from the list and updating their total amount'''
        
        items_list: list = []  # list of product names
        items_to_remove: list = []  # list to store duplicated items

        # remove objects, holding similar value under the key "nazev" from the input data.
        # after removing dublicated objects, update the amount of this products in data lits
        for item in self.data:
                if item[InputData.NAME.value] in items_list:
                    items_to_remove.append(item)
                else:
                    items_list.append(item[InputData.NAME.value])
        for item in items_to_remove:
            amount = item[InputData.AMOUNT.value]
            duplicate_item_name = item[InputData.NAME.value]
            self.data.remove(item)

            for item in self.data:
                if item[InputData.NAME.value] == duplicate_item_name:
                    item[InputData.AMOUNT.value] += amount

    def calculate_total_price_net(self) -> None:
         for item in self.data:
              if item[OutputData.STATUS.value] != 'ERROR':
                item[OutputData.NET_TOTAL.value] = item[InputData.AMOUNT.value] * item[InputData.NET_PER_ITEM.value]
    
    def calculate_vat(self, item):
        return item[InputData.NET_PER_ITEM.value] * ((VAT_RATES[item[InputData.VAT.value]] / 100))
    
    def calculate_gross_per_item(self) -> None:
         for item in self.data:
              if item[OutputData.STATUS.value] != 'ERROR':
                item[OutputData.GROSS_PER_ITEM.value] = round(item[InputData.NET_PER_ITEM.value] + self.calculate_vat(item),1)
    
    def calculate_gross_total(self) -> None:
         for item in self.data:
              if item[OutputData.STATUS.value] != 'ERROR':
                item[OutputData.GROSS_TOTAL.value] = item[OutputData.GROSS_PER_ITEM.value] * item[InputData.AMOUNT.value ]

    def process_input_data(self):
        '''
        Method performs:
            - removing dublicated items and updating its total number
            - validating data input data
            - calculates products net price in total
            - calculates products gross price per item
            - calculates products gross price in total

        '''
        self.sort_out_items()
        self.data_validator()
        self.calculate_total_price_net()
        self.calculate_gross_per_item()
        self.calculate_gross_total()

    def create_output_data(self) -> list[dict]:
        '''
        Method updates data structure, according to the required output data format.
        The dict keys names are updated according to the list of table rows, defined in OutputData(Enum)
        '''
        self.process_input_data()
        output_data: list[dict] = []
        # Define a mapping of old keys to new keys
        key_mapping = {
            InputData.NAME.value: OutputData.NAME.value,
            InputData.AMOUNT.value: OutputData.AMOUNT.value,
            InputData.NET_PER_ITEM.value: OutputData.NET_PER_ITEM.value,
        }
        for item in self.data:
            del item[InputData.VAT.value]
            updated_item = {key_mapping.get(key, key): value for key, value in item.items()}
            output_data.append(updated_item)
        return output_data


