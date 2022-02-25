import Agent
import numpy as np
import random

import Decisions
import Acceptabilities


class SMA:
    def __init__(self, nb_agents, welfare, behavior_kind , swap_kind, resources, valeurs, maxEx):
        self.agentList = [Agent.Agent(i, self, behavior_kind, swap_kind, resources, valeurs, maxEx) for i in range(nb_agents)]
        self.welfare_type=welfare
        self.tick=0
        self.history=[]
        

    def __str__(self) :
        s=""
        for i in range(len(self.agentList)):
            s=s+(self.agentList[i].__str__()+"\n")
        s=s+("Social Welfare : " + str(self.socialWelfare())) 
        return(s)

    def redefineSMA(self) :
        for a in self.agentList :
            a.sma = self

    def setResources(self,resources) :
        for r in resources :
            random.choice(self.agentList).bag.append(r)

    def setGlobalSwapKind(self,swap_kind) :
        for a in self.agentList :
            a.acceptability = eval("Acceptabilities."+swap_kind)

    def setGlobalMaxEx(self,maxEx) :
        for a in self.agentList :
            a.nb_ressources =maxEx

    def setGlobalBehaviorKind(self,behavior_kind) :
        for a in self.agentList :
            a.decision = eval("Decisions."+behavior_kind)

    def setAccointances(self,adjacency_matrix) :
        if (len(adjacency_matrix[0]) != len(self.agentList)) :
            raise ValueError("Problem of size in setAccointances :", len(adjacency_matrix[0]) , len(agentList))
        for i in range(len(self.agentList)) :
            self.agentList[i].accointances = np.nonzero(adjacency_matrix[i])[0]

    def run(self, rounds):
        self.tick=0
        self.history=[]
        self.history.append(self.socialWelfare())
        for i in range(0,rounds):
            self.runOnce()
    
    def runOnce(self):
        self.tick += 1
        for agent in self.agentList:
            agent.decision(agent,self.tick)
        #print("tick " + str(self.tick) + " ended")
        self.history.append(self.socialWelfare())
        #print("Le Welfare actuel est de ", self.socialWelfare())

    def socialWelfare(self):
        if self.welfare_type.upper()=='UTILITARIST':
            return sum([a.welfare() for a in self.agentList])
        elif self.welfare_type.upper()=='EGALITARIST':
            return min([a.welfare() for a in self.agentList])
        elif self.welfare_type.upper()=='ELISTIST':
            return max([a.welfare() for a in self.agentList])
        elif self.welfare_type.upper()=='NASH':
            return np.prod([a.welfare() for a in self.agentList])
        else :
            raise ValueError("Unknown method in socialWelfare")
