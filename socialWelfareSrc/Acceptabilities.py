
def not_yet_defined(self, old_self, old_social) :
    raise Exception("The swap kind of agent "+str(self.name)+" has not been defined yet !")

def irrational(self, old_self, old_social) :
    return True

def social(self, old_self, old_social) :
    return (old_social < self.sma.socialWelfare())

def rational(self, old_self, old_social) :
    return (old_self < self.welfare())
    

