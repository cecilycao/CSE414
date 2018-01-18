'''
caoy27_Farmer_Fox_etc.py
by Ye Cao

Assignment 2, in CSE 415, Winter 2018.

This file contains my problem formulation for the problem of
the Find the Number.
'''
#<METADATA>
SOLUZION_VERSION = "2.0"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "2.0"
PROBLEM_AUTHORS = ['Ye Cao']
PROBLEM_CREATION_DATE = "14-JAN-2018"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The <b>"Farmer, Fox, Chicken, and Grain"</b> problem is a traditional puzzle
in which the player starts off with Farmer, Fox, Chicken, and Grain
on the left bank of a river.  The object is to execute a sequence of legal
moves that transfers them all to the right bank of the river.  In this
version, there is a boat that can carry at most two objects, and one of
them must be the farmer to steer the boat.  It is forbidden to ever
have Fox, Chicken alone, Chicken, Grain alone either on the
left bank, right bank, or in the boat.  In the formulation presented
here, the computer will not let you make a move to such a forbidden situation, and it
will only show you moves that could be executed "safely."
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
Farmer=0  # array index to access farmer counts
C=1  # same idea for chicken
F = 2 #same idea for fox
G = 3 #same idea for grain
LEFT=0 # same idea for left side of river
RIGHT=1 # etc.

class State():

  def __init__(self, d=None):
    if d==None: 
      d = {'people':[[0,0],[0,0],[0,0],[0,0]],
           'boat':LEFT}
    self.d = d

  def __eq__(self,s2):
    for prop in ['people', 'boat']:
      if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    p = self.d['people']
    txt = "\n farmer on left:"+str(p[Farmer][LEFT])+"\n"
    txt += " Chicken on left:"+str(p[C][LEFT])+"\n"
    txt += " Fox on left:"+str(p[F][LEFT])+"\n"
    txt += " Grain on left:"+str(p[G][LEFT])+"\n"
          
    txt = " farmer on right:"+str(p[Farmer][RIGHT])+"\n"
    txt += " Chicken on right:"+str(p[C][RIGHT])+"\n"
    txt += " Fox on right:"+str(p[F][RIGHT])+"\n"
    txt += " Grain on right:"+str(p[G][RIGHT])+"\n"
    side='left'
    if self.d['boat']==1: side='right'
    txt += " boat is on the "+side+".\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.d['people']=[self.d['people'][Farmer_or_C_or_F_or_G][:] for Farmer_or_C_or_F_or_G in [Farmer,C,F,G]]
    news.d['boat'] = self.d['boat']
    return news 

  def can_move(self,farmer,c,f,g):
    '''Tests whether it's legal to move the boat and with farmer number of farmer,
     c chicken, f fox, g grain'''
    side = self.d['boat'] # Where the boat is.
    p = self.d['people']
    if farmer != 1: return False # Need one farmer to steer boat.
    farmer_available = p[Farmer][side]
    if farmer_available < farmer: return False # Can't take more farmer than available
    c_available = p[C][side]
    if c_available < c: return False # Can't take more farmer than available
    f_available = p[F][side]
    if f_available < f: return False # Can't take more farmer than available
    g_available = p[G][side]
    if g_available < g: return False # Can't take more farmer than available
    
    farmer_remaining = farmer_available - farmer
    c_remaining = c_available - c
    f_remaining = f_available - f
    g_remaining = g_available - g
    # no fox-chicken, chicken-grain on either side:
    if farmer_remaining != 0: return False
    if c_remaining == 1 and g_remaining == 1 and f_remaining == 0: return False
    if c_remaining == 1 and f_remaining == 1 and g_remaining == 0: return False
    
    farmer_at_arrival = p[Farmer][1-side]+farmer
    c_at_arrival = p[C][1-side]+c
    f_at_arrival = p[F][1-side]+f
    g_at_arrival = p[G][1-side]+g
    if farmer_at_arrival != 1: return False
    return True


  def move(self,farmer,c,f,g):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the boat carrying
     farmer number of farmer,c chicken, f fox, g grain.'''
    news = self.copy()      # start with a deep copy.
    side = self.d['boat']         # where is the boat?
    p = news.d['people']          # get the array of arrays of people.

    p[Farmer][side] = p[Farmer][side]-farmer     # Remove people from the current side.
    p[C][side] = p[C][side]-c
    p[F][side] = p[F][side]-f
    p[G][side] = p[G][side]-g

    p[Farmer][1-side] = p[Farmer][1-side]+farmer     # Add them at the other side.
    p[C][1-side] = p[C][1-side]+c
    p[F][1-side] = p[F][1-side]+f
    p[G][1-side] = p[G][1-side]+g
    news.d['boat'] = 1-side       # Move the boat itself.
    return news

def goal_test(s):
  '''If all Ms and Cs are on the right, then s is a goal state.'''
  p = s.d['people']
  return (p[Farmer][RIGHT]==1 and p[C][RIGHT]==1 and p[F][RIGHT]==1 and p[G][RIGHT]==1)

def goal_message(s):
  return "Congratulations on successfully guiding the missionaries and cannibals across the river!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'people':[[1,0],[1,0],[1,0],[1,0]], 'boat':LEFT })
#</INITIAL_STATE>

#<OPERATORS>
combinations_in_boat = [(1,0,0,0),(1,1,0,0),(1,0,1,0),(1,0,0,1)]

OPERATORS = [Operator(
  "Cross the river with"+str(farmer)+"farmer, "+str(c)+" chicken, "+str(f)+" fox, "+str(g)+" grain",
  lambda s, farmer1=farmer, c1=c, f1=f, g1=g: s.can_move(farmer1,c1,f1,g1),
  lambda s, farmer1=farmer, c1=c, f1=f, g1=g: s.move(farmer1,c1,f1,g1) ) 
  for (farmer,c,f,g) in combinations_in_boat]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
