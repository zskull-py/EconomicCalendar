from datetime import datetime
import pandas as pd
import requests

#https://economic-calendar.tradingview.com/events?from=2023-07-21T00%3A00%3A00.000Z&to=2023-08-20T00%3A00%3A00.000Z&countries=US #alternative

class EconomicCalendar():
    def __init__(self):
        self.url_ = 'https://economic-calendar.tradingview.com/events' # endpoint tradingview
        self.country_all_codes_ = ['AE', 'AO', 'AR', 'AT', 'AU', 'BD', 'BE', 'BH', 'BR', 'BW', 'CA', 'CH', 'CL', 'CN', 'CO', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EG', 'ES', 'ET', 'EU', 'Fl', 'FR', 'GB', 'GR', 'HK', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JP', 'KE', 'KR', 'KW', 'LK', 'LT', 'LV', 'MA', 'MU', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NG', 'NL', 'NO', 'NZ', 'OM', 'PE', 'PH', 'PK', 'PL', 'PT', 'QA', 'RO', 'RS', 'RU', 'RW', 'SA', 'SC', 'SE', 'SG', 'SK', 'TH', 'TN', 'TR', 'TW', 'TZ', 'UA', 'UG', 'US', 'VE', 'VN', 'ZA', 'ZM', 'ZW'] # all codes
        self.country_default_codes_ = ['US','EU','IT','NZ','CH','AU','FR','JP','ZA','TR','CA','DE','MX','ES','GB'] # TradingView default configuration
        self.countries_ = None
        self.payload_ = None
        self.from_ = None
        self.to_ = None
        self.data_ = None

    def get_calendar(self, from_datetime_ISO8601=None, to_datetime_ISO8601=None, from_datetime_dict=None, to_datetime_dict=None, country_codes=None, return_type='records'):
        """ Get the economic calendar from TradingView.

        Args:
            from_datetime_ISO8601 (str, optional): Date and time in ISO 8601 format . Defaults to None. None to return to the current day's news.
            to_datetime_ISO8601 (str, optional): Date and time in ISO 8601 format. Defaults to None. None to return to the current day's news.
            from_datetime_dict (dict, optional): Dictionary in the following format: {'year':2023, 'month':7, 'day':21, 'hour':0, 'min':0, 'sec':0, 'offset':0}.
                                                 Defaults to None. Will be used if from_datetime_ISO8601 is None.
            to_datetime_dict (dict, optional): Dictionary in the following format: {'year':2023, 'month':7, 'day':21, 'hour':0, 'min':0, 'sec':0, 'offset':0}.
                                               Defaults to None. Will be used if to_datetime_ISO8601 is None.
            country_codes (list, optional): Codes of the countries that will be returned. Defaults to None.
            return_type (str, optional): Return type. Defaults to 'records'.
                                         'records': List of dictionaries.
                                         'raw': Raw data.
                                         'pandas': Pandas object(DataFrame)
                                         'status': Status of the response sent by the server.

        Returns:
            None|list|str|DataFrame: Returns information in the format specified in return_type.
        """
        
        self.data_ = self.get_data_request(from_datetime_ISO8601=from_datetime_ISO8601,
                                           to_datetime_ISO8601=to_datetime_ISO8601,
                                           from_datetime_dict=from_datetime_dict,
                                           to_datetime_dict=to_datetime_dict,
                                           country_codes=country_codes)

        if return_type == 'raw':
            return self.data_
        if return_type == 'records':
            if 'result' in self.data_.keys():
                self.data_ = self.data_['result']
            else:
                self.data_ = None
        elif return_type == 'status':
            if 'status' in self.data_.keys():
                self.data_ = self.data_['status']
            else:
                self.data_ = None
        elif return_type == 'pandas':
            if 'result' in self.data_.keys():
                self.data_ = pd.DataFrame(self.data_['result'])
            else:
                self.data_ = None
        else:
            self.data_ = None

        return self.data_

    def get_data_request(self, from_datetime_ISO8601=None, to_datetime_ISO8601=None, from_datetime_dict=None, to_datetime_dict=None, country_codes=None):
        """
        It can be called directly, or call get_calendar(return_type='raw').
        """
        self.from_, self.to_ = None, None

        if not from_datetime_ISO8601 and not from_datetime_dict:
            self.from_ = datetime.now().strftime('%Y-%m-%dT00:00:00.000Z')
        if not to_datetime_ISO8601 and not to_datetime_dict:
            self.to_ = datetime.now().strftime('%Y-%m-%dT23:59:59.000Z')
    
        if not self.from_:
            from_datetime_dict = {key:str(value) if value>=10 and key!='offset' else str(value).zfill(2) if key!='offset' else str(value).zfill(3) for key,value in from_datetime_dict.items()}
            self.from_ = f"{from_datetime_dict['year']}-{from_datetime_dict['month']}-{from_datetime_dict['day']}T{from_datetime_dict['hour']}:{from_datetime_dict['min']}:{from_datetime_dict['sec']}.{from_datetime_dict['offset']}Z"
        if not self.to_:
            to_datetime_dict = {key:str(value) if value>=10 and key!='offset' else str(value).zfill(2) if key!='offset' else str(value).zfill(3) for key,value in to_datetime_dict.items()}
            self.to_ = f"{to_datetime_dict['year']}-{to_datetime_dict['month']}-{to_datetime_dict['day']}T{to_datetime_dict['hour']}:{to_datetime_dict['min']}:{to_datetime_dict['sec']}.{to_datetime_dict['offset']}Z"
    
        if not country_codes:
            self.countries_ = self.country_default_codes_
        else:
            self.countries_ = country_codes

        self.payload_ = {
            'from': self.from_,
            'to': self.to_,
            'countries': ','.join(self.countries_)
            }

        self.data_ = requests.get(self.url_, params=self.payload_).json()

        return self.data_

if '__main__' == __name__:
    calendar = EconomicCalendar()
    
    # Returns the current day's news.
    #data = calendar.get_calendar()
    
    # Returns news for the specified day.
    data = calendar.get_calendar(from_datetime_dict={'year':2023, 'month':7, 'day':22, 'hour':0, 'min':0, 'sec':0, 'offset':0},
                                 to_datetime_dict={'year':2023, 'month':7, 'day':22, 'hour':23, 'min':59, 'sec':59, 'offset':0},
                                 return_type='pandas')
    print(data)
