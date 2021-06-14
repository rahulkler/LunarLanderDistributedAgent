from DatabaseHandler import DatabaseHandler



class ExperienceReplay:

    def __init__(self, agentId, host, user, password, database):
        self.databaseHandler = DatabaseHandler(host, user, password, database)
        self.databaseHandler.updateRWStatus(agentId, False)

        self.agentId = agentId
        agentCount = self.databaseHandler.getAgentCount(agentId)
        if agentCount:
            self.length = agentCount[0][1]
            self.counter = agentCount[0][0] % self.length
        else:
            self.counter = -1
            self.length = 100000


    def remember(self, s, a, r, s_, done):
        self.counter += 1
        self.databaseHandler.addExperience(self.agentId, s.tolist(), a, r, s_.tolist(), done, self.counter, self.length)


