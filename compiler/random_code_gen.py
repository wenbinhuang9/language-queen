#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 22:00:38 2019

@author: ben
"""
import random
import string
from bisect import bisect_left 
"""
definition of interface and data strucuture
todo add depth indentation
if I want to impement indent , how to do it? 
"""
### only one production class is ok
class Production():
    def __init__(self, lhs):
        ##basic data structure below     
        #production, left non-terminal， string
        self.lhs = lhs 
        #produciton, right rules, list (its element can be list too)
        self.rhs_options=[]
        #probability for each rule
        self.rhs_probs=[]

    #add a rule and the probability
    def add(self, rhs, prob):
        self.rhs_options.append(rhs)
        
        last_probs = self.rhs_probs[-1] if len(self.rhs_probs ) > 0 else 0 
        ## add accumulative probability
        self.rhs_probs.append(last_probs + prob)
        return self
    
    ## this is the core function, generate the code here 
    def expand(self):
        cur_production = self.random_select()
        if type(cur_production) is list:
            ret = ""
            for rule in cur_production:
                ret += rule.expand()
            return ret
        
        return cur_production.expand()
    
    ## random selects a rule, and return the rule
    def random_select(self):
        ran = (random.randint(0, 1000) % 1000)/1000.0
        ## binary search, a better way is using dict
        idx = bisect_left(self.rhs_probs, ran)       
        return self.rhs_options[idx]

    def __str__(self):
        return self.lhs
    
class Char(Production):
     def expand(self):
        return random.choice(string.ascii_letters)
    
class Digit(Production):
     def expand(self):
        return str(random.randint(0, 10))
### the keyword, for example , we can define "if" "else" here
class Str(Production):
     def expand(self):
        return self.lhs 

if __name__ == '__main__':
    empty = Str("")
    IF = Str("if ")
    left_par = Str("( ")
    right_par = Str(" )\n")
    ELSE = Str("else\n")
    semicolon = Str(";\n")
     
     ##terminal 
    digit = Digit("digit")
    char = Char("char")
    
    op = Production("op").add(Str("+"), 0.5).add(Str("-"), 0.2).add(Str("*"), 0.2).add(Str("/"), 0.1)
    
    TYPE = Production("type").add(Str("int "), 0.7).add(Str("double "), 0.3)
    
    digit_seq = Production("digit_seq")
    digit_seq.add(empty, 0.7).add([digit, digit_seq], 0.3)
    
    char_digit_seq = Production("char_digit_seq")
    char_digit_seq.add(empty, 0.5).add([char, char_digit_seq], 0.3).add([digit, char_digit_seq], 0.2)
    
    const = Production("const").add([digit, digit_seq], 1.0)
    ID = Production("ID").add([char, char_digit_seq], 1.0)
    
    exp = Production("exp").add(ID, 0.35).add(const, 0.35)
    exp.add([exp, op, exp], 0.3)
    
    assg_stat = Production("assg_stat").add([ID, Str(" = "), exp, semicolon], 1.0)
    
    decl_stat = Production("decl_stat").add([TYPE, ID, semicolon], 0.5).add([ TYPE, assg_stat], 0.5)
  
    cmpd_stat = Production("cmpd_stat")
    stat = Production("stat")
    
    if_stat = Production("if_stat") \
              .add([IF, left_par, exp, right_par, cmpd_stat], 0.2) \
              .add([IF, left_par, exp, right_par, stat, ELSE, stat], 0.5) \
              .add([IF, left_par, exp, right_par, cmpd_stat, ELSE, stat], 0.1) \
              .add([IF, left_par, exp, right_par, stat, ELSE, cmpd_stat], 0.1) \
              .add([IF, left_par, exp, right_par, cmpd_stat, ELSE, cmpd_stat], 0.1)
    
    iter_stat = Production("iter_stat") \
                .add([Str("while ( "), exp, Str(" )\n"),cmpd_stat], 0.5)\
                .add([Str("while ( "), exp, Str(" )\n"), stat], 0.5) 

    stat_list = Production("stat_list").add([stat], 0.3)
    stat_list.add([stat_list, stat], 0.7)

    cmpd_stat = cmpd_stat.add([Str("{\n"), stat_list, Str("}\n")], 1.0)

    stat.add(cmpd_stat, 0.05).add(if_stat, 0.15) \
        .add(iter_stat, 0.1).add(assg_stat, 0.35) .add(decl_stat, 0.35)
    
    prog = Production("prog").add([Str("int main()\n{\n"), stat_list, Str("\nreturn 0; \n}\n")], 1.0)

    ret = exp.expand()
    #ret = prog.expand()
    print(ret)
    f= open("./random_code.txt","w+")
    f.write(ret)
    
    f.close() 

    
