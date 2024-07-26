class BasinClass:
    def __init__(self, basin, external_user):
        self.basin = basin
        self.external_user = external_user

    def get_basin_path(self):
        if self.basin.lower() == "AMZN":
            
            #External user here
            if self.external_user == True:
                search_link = ""
            
            #Tufts user here
            else:
                search_link =  ""
            
            return search_link
        
        elif self.basin.lower() == "CLMB":
            if self.external_user == True:
                search_link = ""
            else:
                search_link = ""
            return search_link
        
        elif self.basin.lower() == "CNGO":
            if self.external_user == True:
                search_link = ""
            else:
                search_link = ""
            return search_link

        elif self.basin.lower() == "DANU":
            if self.external_user == True:
                search_link = ""
                return search_link        
            else:
                search_link = ""
                return search_link
            
        elif self.basin.lower() == "RGNA":
            if self.external_user == True:
                search_link = ""
                return search_link        
            else:
                search_link = ""
                return search_link
            
        elif self.basin.lower() == "YUKN":
            if self.external_user == True:
                search_link = ""
                return search_link        
            else:
                search_link = ""
                return search_link