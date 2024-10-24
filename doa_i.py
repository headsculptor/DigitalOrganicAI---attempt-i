import random

#Ai vars

freethought_simulator = 0 #Max 1
influenced = True #Use emotion simulated intelligence
neurondict = {}
#ai_state = [happiness, anger, sadness, nervousness]

#Variance vars
construction_rate, destruction_rate, least_likely_rate, unique_rate = 0.8, 0.4,0 .2, 0.1
default_vector = [construction_rate, destruction_rate, least_likely_rate, unique_rate]

#Database CLASS

class DatabaseHandler:
    def __init__(self, databasefilename):
        if databasefilename[-4:] != ".txt":
            self.databasefile = databasefilename + ".txt"
        else:
            self.databasefile = databasefilename
        try:
            open(self.databasefile, "r").close()
        except:
            open(self.databasefile, "a").close()
            newdbwrite = open(self.databasefile, "w")
            newdbwrite.write("UserID,Money,Rank\n")
            newdbwrite.close()

    def changedb(self, newdbcontent):
        content = str(newdbcontent)
        open(self.databasefile, "w").close()
        dbfile = open(self.databasefile, "w")
        dbfile.write(content)
        dbfile.close()

    def datagrab(self, Key):
        self.updaterows()
        key = str(Key)
        with open(self.databasefile, "r") as dbfile:
            dblines = dbfile.readlines()[1:]
            for x in range(len(dblines)):
                dbline = dblines[x].replace("\n", "")
                linedata = dbline.split(",")
                if linedata[0] == key:
                    return [linedata, x]
        return None

    def valueget(self, valueID, Key):
        valID = str(valueID)
        key = str(Key)
        with open(self.databasefile, "r") as dbfile:
            valueids = dbfile.readlines()[0].replace("\n", "")
            valueids = valueids.split(",")
            for x in range(len(valueids)):
                if valueids[x] == valID:
                    return [self.datagrab(key)[0][x], x]
        print("No value id : " + valID)

    def valueupdate(self, valueID, Key, newvalue):
        valID = str(valueID)
        key = str(Key)
        update = str(newvalue)
        self.updaterows()
        try:
            with open(self.databasefile, "r") as dbfile:
                dblines = dbfile.readlines()
            data = self.datagrab(key)
            data[0][self.valueget(valID, key)[1]] = update
            dblines[data[1]+1] = ",".join(data[0]) + "\n"
            self.changedb("".join(dblines))
        except:
            print("Could not update " + valID + " for " + key + " to new value " + update)

    def first_line(self):
        with open(self.databasefile, "r") as dbfile:
            firstline = dbfile.readlines()[0].replace("\n", "")
            firstline = firstline.split(",")
        return firstline

    def get_lines(self):
        with open(self.databasefile, "r") as dbfile:
            lines = dbfile.readlines()
        for x in range(len(lines)):
            lines[x] = lines[x].replace("\n", "")
        return lines

    def newkey(self, newkey):
        nkey = str(newkey)
        tempflag = False
        if self.datagrab(nkey) == None:
            with open(self.databasefile, "r") as dbfile:
                try:
                    dbcoms = dbfile.readlines()[0].count(",")
                except:
                    tempflag = True
            if tempflag == True:
                newdb = open(self.databasefile, "w")
                newdb.write("UserID,Money,Rank\n")
                newdb.close()
                dbcoms = dbfile.readlines()[0].count(",")
            for x in range(dbcoms):
                nkey += ",0"
            with open(self.databasefile, "r") as dbfile:
                dbcontent = dbfile.read() + nkey + "\n"
            self.changedb(dbcontent)
            nkey = str(newkey)
            #New user defaults:

            #self.valueupdate("Money", nkey, 25)
            #self.valueupdate("Commands_Used", nkey, 0)
            
            return True
        else:
            return False

    def delcol(self, valueID):
        valID = str(valueID)
        self.z = 0
        self.tempstr = ""
        self.templine = []
        self.reflag = False
        with open(self.databasefile, "r") as dbfile:
            dbline = str(dbfile.readlines()[0].replace("\n", "")).split(",")
            for x in range(len(dbline)):
                if dbline[x] == valID:
                    self.z = x
                    self.reflag = True
        if self.reflag == True:
            with open(self.databasefile, "r") as dbfile:
                dblines = dbfile.readlines()
            for x in range(len(dblines)):
                self.templine = (dblines[x].replace("\n", "")).split(",")
                self.templine.pop(self.z)
                self.tempstr += ",".join(self.templine) + "\n"
            self.changedb(self.tempstr)
        else:
            return False

    def updaterows(self):
        self.tempstr = ""
        with open(self.databasefile, "r") as dbfile:
            filelines = dbfile.readlines()
            comcount = filelines[0].count(",")
            filelines[0] = filelines[0].replace("\n", "")
        with open(self.databasefile, "r") as dbfile:
            readfile = dbfile.read()
        for x in range(len(filelines)-1):
            filelines[x+1] = filelines[x+1].replace("\n", "")
            if filelines[x+1] != "":
                linecom = filelines[x+1].count(",")
                while linecom < comcount:
                    filelines[x+1] += ",0"
                    linecom = filelines[x+1].count(",")
        newfile = "\n".join(filelines) + "\n"
        self.changedb(newfile)

    def addvalueid(self, ValueID):
        valID = str(ValueID)
        fields = self.get_fields()
        tempflag = False
        for x in range(len(fields)):
            if fields[x] == valID:
                tempflag = True
        if tempflag == True:
            return False
        lines = self.get_alldata()
        lines[0] = lines[0] + "," + valID
        self.changedb("\n".join(lines))
        self.updaterows()

    #Calls--

    #Used to interact with database in a user-friendly method

    def get(self, DataField, Key): #Get a cell value
        return self.valueget(DataField, Key)[0]
    def update(self, DataField, Key, NewValue): #Update a cell value
        self.valueupdate(DataField, Key, NewValue)
    def delid(self, DataField): #Delete a data id column
        self.delcol(DataField)
    def addkey(self, Key): #Creates a new row with given key
        return self.newkey(Key)
    def get_fields(self): #Gets fields
        return self.first_line()
    def get_alldata(self): #Gets all lines from database file
        return self.get_lines()
    def addfield(self, DataField): #Adds new data field
        self.addvalueid(DataField)

db = DatabaseHandler('neuronlist')

class ai_state:
    def __init__(self):
        self.default_state = [1,1,1,1]
        self.state = self.default_state
    def get_state(self):
        return self.state

class neuron:
    def __init__(self, neuroninfo):
        global neurondict
        self.state_influence = []
        self.id = neuroninfo[0]
        neurondict[int(self.id)] = self
        self.uplink = neuroninfo[1]
        self.downlink = neuroninfo[2]
        self.leftlink = neuroninfo[3]
        self.rightlink = neuroninfo[4]
        self.link_types = [self.uplink, self.downlink, self.leftlink, self.rightlink]
    def influence(self, ai_state):
        self.state_influence = ai_state
        

    def fire(self):
        global freethought_simulator
        res = [0, 0]
        if self.state_influence == []:
            return self.uplink
        for i in self.link_types:
            factori = freethought_simulator * random.random()
            if factori != 0:
                inf1 = self.state_influence[self.link_types.index(i)]
                if factori * inf1 > res[0]:
                    res = [factori * inf1, i]
            else:
                inf1 = self.state_influence[self.link_types.index(i)]
                if inf1 > res[0]:
                    res = [inf1, i]
        return res[1]


def load_all_neurons():
    global influenced
    emotion_state = ai_state().get_state()
    for n in db.get_alldata()[1:]:
        new_neuron = neuron(n)
        if influenced:
            new_neuron.influence(emotion_state)

load_all_neurons()
print(neurondict)
