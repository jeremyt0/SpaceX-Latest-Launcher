from flask import Flask, render_template, request, redirect, url_for, send_file

from retriever.retriever import Retriever

class Interface(object):

    instance = None

    @staticmethod
    def getInstance():
        if Interface.instance is None:
            Interface.instance = Interface()
        return Interface.instance


    def __init__(self):
        super(Interface, self).__init__()
        
        self.app = Flask(__name__)
        self.setRoutes()
        self.app.config['SECRET_KEY'] = '4513cb7cfb867ef6a7191634da6b8170'


        ## Init retriever instance
        self.data_retriever = Retriever.getInstance()


    def setRoutes(self):

        @self.app.route('/')
        def home():
            # Latest launch information
            latest_launch_info = self.data_retriever.get_launch_info_main()  # Dictionary

            # Latest launch ships information
            latest_launch_ships_info = self.data_retriever.get_ships_info_main()  # List of dictionaries

            # print(latest_launch_info)
            # print(latest_launch_ships_info)

            return render_template('home.html', latest_launch=latest_launch_info, ships=latest_launch_ships_info)


        @self.app.route("/serve_image/<path>")
        def serve_image(path):
            image = path.replace('--2F--','/').replace('--5C--','\\').replace('--3A--', ':').replace('%20',' ')
            
            return send_file(image)


    def run(self):
        try:
            self.app.run(debug=False)
        except:
            # Log exception
            pass

