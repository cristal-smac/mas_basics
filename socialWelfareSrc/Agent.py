import random
import numpy as np
import itertools



import Acceptabilities
import Decisions

class Agent:
    def __init__(self, name, own_sma, behavior_kind, swap_kind, resources, valeurs,maxEx) :
        self.name=name
        self.sma = own_sma
        self.fUtil = {r : random.choice(valeurs) for r in resources}
        self.bag = []
        self.accointances = []
        self.nb_ressources = maxEx  # Nombre de ressources max que l'agent va échanger.

        self.acceptability = eval("Acceptabilities."+(swap_kind or 'not_yet_defined'))  # Va chercher la fonction d'acceptabilité correspondant a swap_kind
        self.decision = eval("Decisions."+(behavior_kind or 'not_yet_defined'))         # Va chercher la fonction de comportement correspondant a behavior_kind
        
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
