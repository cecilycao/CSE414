'''
caoy27_Find_the_Number.py
by Ye Cao

Assignment 2, in CSE 415, Winter 2018.

This file contains my problem formulation for the problem of
the Find the Number.
'''

from random import *
import math
from builtins import int

#<METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Find the number"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Ye Cao']
PROBLEM_CREATION_DATE = "17-JAN-2018"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The <b>"Find the number"</b> is a guessing game that user will input a secret number
 and a maximum number. Computer will ask questions in the form of "Is N divisible by m 
 after subtracting k ?" where N denotes the secret number, m is the prime number and
  m >= k >= 0. After user answering the questions, computer will give a guess.
'''
#</METADATA>

#<COMMON_DATA>
try:
    import sys
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
    secret = int(arg2)
    max = int(arg3)
    if(secret>=0):
        print("A new secret number was successfully read in from the command line.")
    if(max >= secret):
        print(" new maximum number (range limit) was successfully read in from the command line.")
except:
    print(" (Type in a secret number and a maximum number on the command line, e.g.,")
    print("python3 ../Int_Solv_Client.py Find_the_Number 7 10")
#</COMMON_DATA>


#<COMMON_CODE>
class State():
  def __init__(self, d=None):
    if d==None: 
        d = {'possibilities':[],
             'last_m':None,
             "phase":0}
    self.d = d

  def __eq__(self,s2):
    for prop in ['possibilities', 'last_m', 'phase']:
        if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    txt = "question_phase:" + str(self.d['phase']) + '\n'
    txt += "last_m: " + str(self.d['last_m']) + '\n'
    txt += "possibilities: " + str(self.d['possibilities'])
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.d['possibilities'] = self.d['possibilities'][:]
    news.d['last_m'] = self.d['last_m']
    news.d['phase'] = self.d['phase']
    return news 

  def can_move(self,m,k,p):
    '''Tests whether it's legal to do the operation.'''
    current_phase = self.d['phase']
    #if current question_phase is 0, return true
    if p == current_phase and p == 0:
        return True
    #if current question phase is 1, return true when k <= last m, 
    #return false otherwise
    if p == current_phase and p == 1:
        get_m = self.d['last_m']
        if k >= get_m:
            return False
        return True
    return False


  def move(self,m,k,p):
    '''If question phase = 0, turn question phase to 1 after moving
     and change nothing else, If question phase = 1, this computes
     the new state resulting from eliminates possible numbers
     that is not divisible by m after subtracting k. Then, turning 
     question phase = 0'''
    if p == 0:
        news = self.copy()
        news.d['last_m'] = m
        news.d['phase'] = 1
        return news
    
    news = self.copy()      # start with a deep copy.
    list = news.d['possibilities']
    m = news.d['last_m']
    newlist = []
    for i in range(len(list)):
        number = int(list[i])
        if(((number - k) % m) == 0):
           newlist.append(number)
    news.d['possibilities'] = newlist
    news.d['phase'] = 0
    return news

def goal_test(s):
  '''If the only number in the list is the secret number, then s is a goal state.'''
  last_number = s.d['possibilities']
  return (len(last_number)==1 and last_number[0] == secret)

def goal_message(s):
  return "Congratulations, you find the secret number!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

#<COMMON_CODE>
#Calculate all the prime numbers from 2 to the maximum
primeList = []
for number in range(2, max+1):
    for i in range(2, number):
        if number % i == 0:
            break
    else:
            primeList += [number]
#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'possibilities':[i for i in range(max+1)],
                                         'last_m':None,
                                         'phase':0})
#</INITIAL_STATE>

#<OPERATORS>
OPERATORS = [Operator(
    "Is N divisible by "+str(m)+" after...",
    lambda s, m1 = m, k1 = None, p1 = 0: s.can_move(m1,k1,p1),
    lambda s, m1 = m, k1 = None, p1 = 0: s.move(m1,k1,p1))
    for m in primeList]

OPERATORS += [Operator(
    "... subtracting " + str(k) + " ?",
    lambda s, m1 = None, k1 = k, p1 = 1: s.can_move(m1,k1,p1),
    lambda s, m1 = None, k1 = k, p1 = 1: s.move(m1,k1,p1))
    for k in range(0, max+1)]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
