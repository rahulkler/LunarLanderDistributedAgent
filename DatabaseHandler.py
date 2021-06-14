import mysql.connector
import numpy as np

MASTER_ID = 100

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
        self.cursor = self.conn.cursor()

        self.tables = self.getTables()


    def getTables(self):
        sqlFormula = 'SHOW TABLES'
        self.cursor.execute(sqlFormula)
        return [table[0] for table in list(self.cursor)]


    def isAgentExistInCountTable(self, agentId):
        sqlFormula = f"SELECT agentId FROM CountTable WHERE agentId = {agentId}"
        self.cursor.execute(sqlFormula)
        return bool(self.cursor.fetchall())


    def isAgentExistInModelRWTable(self, agentId):
        sqlFormula = f"SELECT agentId FROM ModelRWTable WHERE agentId = {agentId}"
        self.cursor.execute(sqlFormula)
        return bool(self.cursor.fetchall())



    def isIndexExistInAgentTable(self, agentId, index):
        agentTable = f'Agent_{agentId}_ExperienceTable'
        if agentTable in self.tables:
            sqlFormula = f"SELECT id FROM {agentTable} WHERE id = {index}"
            self.cursor.execute(sqlFormula)
            return bool(self.cursor.fetchall())
        else:
            return -1


    def insertIntoCountTable(self, agentId, counter, length):
        sqlFormula = f"INSERT INTO CountTable (agentId, counter, length) " \
                     f"VALUES ({agentId}, {counter}, {length})"
        self.cursor.execute(sqlFormula)


    def updateIntoCountTable(self, agentId, counter, length):
        sqlFormula = f"UPDATE CountTable " + \
                     f"SET counter = {counter}, length = {length} " + \
                     f"WHERE agentId = {agentId}"
        self.cursor.execute(sqlFormula)


    def insertIntoModelRWTable(self, agentId, status):
        sqlFormula = f"INSERT INTO ModelRWTable (agentId, status) " \
                     f"VALUES ({agentId}, {status})"
        self.cursor.execute(sqlFormula)


    def updateIntoModelRWTable(self, agentId, status):
        sqlFormula = f"UPDATE ModelRWTable " + \
                     f"SET status = {status} " + \
                     f"WHERE agentId = {agentId}"
        self.cursor.execute(sqlFormula)


    def insertIntoAgentExperienceTable(self, agentId, index, s, a, r, s_, done):
        agentTable = f'Agent_{agentId}_ExperienceTable'
        sqlFormula = f"INSERT INTO {agentTable} (id, s, a, r, s_, done) " + \
                     f"VALUES ({index}, '{str(s)}', {a}, {r}, '{str(s_)}', {done})"
        self.cursor.execute(sqlFormula)


    def updateIntoAgentExperienceTable(self, agentId, index, s, a, r, s_, done):
        agentTable = f'Agent_{agentId}_ExperienceTable'
        sqlFormula = f"UPDATE {agentTable} " + \
                     f"SET s = '{str(s)}', a = {a}, r = {r}, s_ = '{str(s_)}', done = {done} " + \
                     f"WHERE id = {index}"
        self.cursor.execute(sqlFormula)


    def addExperience(self, agentId, s, a, r, s_, done, counter, length):
        agentTable = f'Agent_{agentId}_ExperienceTable'
        countTable = 'CountTable'

        if (agentTable in self.tables) and (countTable in self.tables):
            index = counter % length

            if self.isIndexExistInAgentTable(agentId, index):
                self.updateIntoAgentExperienceTable(agentId, index, s, a, r, s_, done)
            else:
                self.insertIntoAgentExperienceTable(agentId, index, s, a, r, s_, done)

            if self.isAgentExistInCountTable(agentId):
                self.updateIntoCountTable(agentId, counter, length)
            else:
                self.insertIntoCountTable(agentId, counter, length)

            self.conn.commit()
            return 1

        else:
            return -1


    def updateRWStatus(self, agentId, status):
        modelRWTable = 'ModelRWTable'

        if modelRWTable in self.tables:
            if self.isAgentExistInModelRWTable(agentId):
                self.updateIntoModelRWTable(agentId, status)
            else:
                self.insertIntoModelRWTable(agentId, status)

            self.conn.commit()
            return 1
        else:
            return -1


    def getAgentCount(self, agentId):
        formula = f'SELECT counter, length FROM CountTable where agentId={agentId}'
        self.cursor.execute(formula)
        res = self.cursor.fetchall()
        return res


    def getRWStatus(self):
        formula = f'SELECT * FROM ModelRWTable'
        self.cursor.execute(formula)
        res = self.cursor.fetchall()
        statusDict = {}
        for i in res: statusDict[i[0]] = i[1]
        return statusDict


    def isReadyToWrite(self):
        self.conn.reconnect()
        statusDict = self.getRWStatus()
        for agentId in statusDict:
            if agentId != MASTER_ID:
                if statusDict[agentId]:
                    return False
        return True


    def isReadyToRead(self):
        self.conn.reconnect()
        statusDict = self.getRWStatus()
        return not statusDict[MASTER_ID]


    def getExperienceForAgent(self, agentId, indexes):
        agentTable = f'Agent_{agentId}_ExperienceTable'
        sqlFormula = f"SELECT s, a, r, s_, done FROM {agentTable} WHERE id IN {indexes}"
        self.cursor.execute(sqlFormula)
        return self.cursor.fetchall()


    def getExperiences(self, batchSize=64):
        formula = "SELECT * FROM CountTable"
        self.cursor.execute(formula)
        res = self.cursor.fetchall()
        ids, counters, lengths = zip(*res)
        nEntries = sum(lengths)

        randomBatch = np.random.choice(nEntries, size=batchSize, replace=False)

        batchDict = {}
        for id in ids: batchDict[id] = []

        for val in randomBatch:
            cumLength = 0
            for i, length in enumerate(lengths):
                if val < cumLength + length:
                    id = ids[i]
                    batchDict[id].append(val - cumLength)
                    break

                cumLength += length

        experiences = []

        for agentId in batchDict:
            experience = self.getExperienceForAgent(agentId, tuple(batchDict[agentId]))
            experiences += experience

        return experiences




















