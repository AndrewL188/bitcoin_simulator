import random
import math

# Runs a simulation of an attacker using private chain 
# mining strategy proposed in Bitcoin white paper. Attacker
# will start mining on a private chain when a target transaction
# t appears. Synchronous 0-delay case.
# Attacker has mining power q and commit depth z
# Returns whether attacker was successful in overwriting t.
# Assume that attacker "gives up" after public chain has > 3z lead.
def nakamoto_malicious_simulation(q, z) -> bool:
    public_chain = 0
    private_chain = 0
    while (public_chain < z):
        if (nextBlockMalicious(q)):
            private_chain += 1
        else:
            public_chain += 1
    # Attacker wins
    if (private_chain >= public_chain):
        return True
    # Attacker needs to catch up
    failure_threshold = max(3*z, 100)
    while (public_chain - private_chain < failure_threshold):
        if (nextBlockMalicious(q)):
            private_chain += 1
        else:
            public_chain += 1
        if (private_chain >= public_chain):
            return True
    return False

# Computes empirical probability of attacker success by running many simulations
def computeEmpiricalSuccess(q, z, iter=10000):
    num_success = 0
    for i in range(iter):
        num_success += int(nakamoto_malicious_simulation(q, z))
    return num_success/iter

# Assume q is rounded to two decimal places
def nextBlockMalicious(q) -> bool:
    return (random.randint(1,100) <= (q*100))

# Function that computes actual probability of attacker success under
# 0 delay synchrony assumption
# Params: q - Malicious mining rate
#         z - blocks deep considered "committed" block
def computeAttackerSuccessProb(q, z):
    p = 1 - q
    pwin = 0
    for j in range(0, 2*z+1):
        pwin_numAblocks = 1
        if (j < z):
            pwin_numAblocks = (q/p)**(2*z-2*j)
        p_numAblocks = math.comb(2*z, j)*(q**j)*(p**(2*z-j))
        pwin += pwin_numAblocks*p_numAblocks
    return pwin

def main():
    print("Computed attacker success: " + str(computeAttackerSuccessProb(0.2, 6)))
    print("Empirical attacker success: " + str(computeEmpiricalSuccess(0.2, 6, 100000)))
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()