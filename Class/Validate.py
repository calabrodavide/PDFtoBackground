class Validate:

    def __init__(self, row):
        self.__row = row
        self.valid = self.__isValid()

    # checks if the lenght and keywords so that it is valid to exclude empty or corrupted days
    def __isValid(self):
        # add cell for each cell in row if any keyword in [keywords] is found in cell
        return True if len(self.__row) <= 7 and len(self.__row) >= 5 and self.__isFloat(self.__row[2]) and self.__isFloat(self.__row[3]) and len([cell for cell in self.__row if any(keyword in cell.lower() for keyword in ['giorno', 'data', 'sede', 'docente'])]) == 0 else False

    # since they cannot decide if they want to use the extended format for the year, this accounts for both
    def getDate(self):   
        date_components = self.__row[1].split('/')
        if not date_components[-1].startswith('20'):
            date_components[-1] = '20' + date_components[-1]
        return '-'.join(reversed(date_components))

    def getTime(self):
        return [self.__row[2].replace(',', ':').replace('.', ':'), self.__row[3].replace(',', ':').replace('.', ':')]
    
    def getSubject(self):
        if len(self.__row) > 4:
            return self.__row[4]
        else:
            return 'None'
        
    def getLocation(self):
        if len(self.__row) > 5:
            return self.__row[5]
        else:
            return 'None'
    
    def getTeacher(self):
        if len(self.__row) > 6:
            return self.__row[6]
        else:
            return 'None'
    
    def __isFloat(self, num):
        try:
            value = float(num.replace(',', '.'))
            return True
        except ValueError:
            return False