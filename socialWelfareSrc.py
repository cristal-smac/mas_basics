import numpy as np
import random
import itertools



def behavior_not_yet_defined(self,tick) :
        raise Exception("The behavior kind of agent "+str(self.name)+" has not been defined yet !")

def random2(self,tick) :
    if (len(self.accointances)==0 or len(self.bag)==0) : return
    
    actualSocialWelfare = self.sma.socialWelfare()
    actualMyWelfare = self.welfare()
    
    friend = self.sma.agentList[np.random.choice(self.accointances)]
    actualFriendWelfare = friend.welfare()
    
    r_given = np.random.choice(self.bag, min(np.random.randint(1,self.nb_ressources+1),len(self.bag)), False)
    r_received = np.random.choice(friend.bag, min(np.random.randint(0,friend.nb_ressources+1),len(friend.bag)), False)
    self.exchange(friend,r_given,r_received)
    
    if(self.acceptability(self,actualMyWelfare,actualSocialWelfare) and friend.acceptability(friend,actualFriendWelfare,actualSocialWelfare)) : return
    else :
        self.exchange(friend,r_received,r_given)
        return


def friend(self,tick) :
    if (len(self.accointances)==0 or len(self.bag)==0) : return
    
    r_possible_given =  self.possible_ressources(1)
    actualSocialWelfare = self.sma.socialWelfare()
    actualMyWelfare = self.welfare()
    
    for f in self.accointances :
        friend = self.sma.agentList[f]
        actualFriendWelfare = friend.welfare()
        r_possible_received = friend.possible_ressources(0)           
        for r in r_possible_given :
            for p in r_possible_received :
                self.exchange(friend,r,p)
                if(self.acceptability(self,actualMyWelfare,actualSocialWelfare) and friend.acceptability(friend,actualFriendWelfare,actualSocialWelfare)) : return
                else : self.exchange(friend,p,r)
                

def resource(self,tick) :
    if (len(self.accointances)==0 or len(self.bag)==0) : return
    
    r_possible_given =  self.possible_ressources(1)
    actualSocialWelfare = self.sma.socialWelfare()
    actualMyWelfare = self.welfare()
    
    for r in r_possible_given :
        for f in self.accointances :
            friend = self.sma.agentList[f]
            actualFriendWelfare = friend.welfare()
            r_possible_received = friend.possible_ressources(0)
            for p in r_possible_received :
                self.exchange(friend,r,p)
                if(self.acceptability(self,actualMyWelfare,actualSocialWelfare) and friend.acceptability(friend,actualFriendWelfare,actualSocialWelfare)) : return
                else : self.exchange(friend,p,r)

def swap_not_yet_defined(self, old_self, old_social) :
    raise Exception("The swap kind of agent "+str(self.name)+" has not been defined yet !")

def irrational(self, old_self, old_social) :
    return True

def social(self, old_self, old_social) :
    return (old_social < self.sma.socialWelfare())

def rational(self, old_self, old_social) :
    return (old_self < self.welfare())
    


class Agent:
    def __init__(self, name, own_sma, behavior_kind, swap_kind, resources, valeurs,maxEx) :
        self.name=name
        self.sma = own_sma
        self.fUtil = {r : random.choice(valeurs) for r in resources}
        self.bag = []
        self.accointances = []
        self.nb_ressources = maxEx  # Nombre de ressources max que l'agent va échanger.

        self.acceptability = eval(swap_kind or 'swap_not_yet_defined')  # Va chercher la fonction d'acceptabilité correspondant a swap_kind
        self.decision = eval(behavior_kind or 'behavior_not_yet_defined')         # Va chercher la fonction de comportement correspondant a behavior_kind
        
    def __str__(self) :
        return "agent "+str(self.name)+" Welfare :"+ str(self.welfare())+"\tbag :"+ str(self.bag)
    def welfare(self):
        return sum([self.fUtil.get(r) for r in self.bag])
    def getSortedBag(self):
        bagval = [ (r,self.fUtil.get(r)) for r in self.bag]
        return [r for r,_ in sorted(bagval, key=lambda x: x[1])]

    def exchange(self,agent2,given,received) :
        for g in given :
            self.bag.remove(g)
            agent2.bag.append(g)
        for r in received :
            agent2.bag.remove(r)
            self.bag.append(r)
        #print(str(self.name) + " echange " + str(given) + " contre " + str(received) + " avec " + str(agent2.name))
        return
    
    def possible_ressources(self,minimum) : 
        r = []
        for i in range (minimum, min(len(self.bag)+1,self.nb_ressources+1)) :
            r = r + list(itertools.combinations(self.getSortedBag(), i))
        return r


class SMA:
    def __init__(self, nb_agents, welfare, behavior_kind , swap_kind, resources, valeurs, maxEx):
        self.agentList = [Agent(i, self, behavior_kind, swap_kind, resources, valeurs, maxEx) for i in range(nb_agents)]
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
            a.acceptability = eval(swap_kind)

    def setGlobalMaxEx(self,maxEx) :
        for a in self.agentList :
            a.nb_ressources =maxEx

    def setGlobalBehaviorKind(self,behavior_kind) :
        for a in self.agentList :
            a.decision = eval(behavior_kind)

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
