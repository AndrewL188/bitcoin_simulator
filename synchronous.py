import random

# Assume q is rounded to two decimal places
def nextBlockMalicious(q) -> bool:
    return (random.randint(1,100) < (q*100))

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
    print("hey there")
  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()