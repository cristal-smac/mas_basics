import numpy as np


def not_yet_defined(self,tick) :
        raise Exception("The behavior kind of agent "+str(self.name)+" has not been defined yet !")

def random(self,tick) :
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
