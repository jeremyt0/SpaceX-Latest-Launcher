import requests
import json
from datetime import datetime, timedelta

from retriever.img_processor import Img_processor

class Retriever(object):

    instance = None

    @staticmethod
    def getInstance():
        if Retriever.instance is None:
            Retriever.instance = Retriever()
        return Retriever.instance

    def __init__(self):
        super().__init__()

        self.base_url = 'https://api.spacexdata.com/v4'
        self.launches_url = self.base_url + '/launches'
        self.ships_url = self.base_url + '/ships'

        self.launch_info = {}               # Dictionary of latest launch information
        self.launch_info_condensed = {}     # Dictionary of only important information of latest launch

        self.ships_id = None                # List containing all ship ids
        self.ships_info = None              # List containing each ship info (dictoinary)



    def set_launch_info(self, latest=True):
        if latest:
            launch_url = self.launches_url + '/latest'
            self.launch_info = self.get_data_json(launch_url)
        else:
            pass
    
        return True

    def set_launch_info_condensed(self):
        name = self.launch_info['name']
        date_unix = int(self.launch_info['date_unix'])
        date = (datetime.fromtimestamp(date_unix) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M')
        details = self.launch_info['details']
        # images = self.launch_info['links']
        logo = self.launch_info['links']['patch']['small']

        self.launch_info_condensed['name'] = name
        self.launch_info_condensed['date'] = date
        self.launch_info_condensed['details'] = details
        self.launch_info_condensed['logo'] = Img_processor.save_image(logo, 'logo.png')
        return True

        
    def set_launch_ships_info(self):
        self.ships_info = []
        for ship in self.ships_id:
            ship_url = f'{self.ships_url}/{ship}' 
            ship_data = self.get_data_json(ship_url)
            
            ship_info = {}
            
            s_name = ship_data['name']
            s_type = ship_data['type']
            s_home_port = ship_data['home_port']
            s_image = ship_data['image']
            
            ship_info['name'] = s_name
            ship_info['type'] = s_type
            ship_info['home_port'] = s_home_port
            ship_info['image'] = Img_processor.save_image(s_image, f'{s_name}.png')

            self.ships_info.append(ship_info)
        
        return True


    def get_launch_info_main(self):
        ''' Main method for setting and returning latest launch info '''
        self.set_launch_info()
        self.set_launch_info_condensed()
        return self.get_launch_info_condensed()

    def get_ships_info_main(self):
        ''' Main method for setting and returning all ships info '''
        self.ships_id = self.launch_info['ships']
        self.set_launch_ships_info()
        return self.get_ships_info()


    def get_launch_info_condensed(self):
        return self.launch_info_condensed

    def get_ships_info(self):
        return self.ships_info

    def get_data_json(self, url):
        r = requests.get(url)        
        return json.loads(r.text)


    