import sys
import numpy as np
import copy
class Interpreter(object):
    ''' 
    Class takes stack in reverse Polish notation and makes computations 
    '''
    def __init__(self,stack,operands,trace=True):
        '''
        stack - stack in reversed polish notation from lexical analizer
        operands - constants and variables from scaner
        trace - show/hide computations stack at each step
        '''
        self.operands=copy.deepcopy(operands)
        self.stack=stack
        self.count_stack=[]
        self.end_symbols=[-100]
        self.trace=trace
    def show(self):
        '''
        Show current operands list
        '''
        print(self.operands)
    def count_reversed_form(self,start_point=0):
        '''
        Main function, that interpretates stack
        output: operands list after computations
        '''
        stack=self.stack
        i=0
        ## Main cycle over stack
        while stack[i] not in self.end_symbols:
            ## Show count_stack at each step
            if self.trace==True: print(i,self.count_stack)  
            
            ## link on constant or variable after scaner's work
            if stack[i] in self.operands.keys(): 
                self.count_stack.append([stack[i],'link'])
            ## symbol jump for condition operator
            elif stack[i]>0: 
                self.count_stack.append([stack[i],'value'])
            ## operator
            else: 
                '''
                Processing of all operators from operators list
                '''
                if operators[stack[i]] in ['+','-','*','/']:
                    operation=operators[stack[i]]
                    to_eval=self.unpack(number=2)
                    types=self.get_type(to_eval)
                    if types[0]=='numeric' and types[1]=='numeric':
                        oper_result=eval(str(to_eval[0])+operation+str(to_eval[1]))
                        #print(oper_result)
                        self.count_stack[-2]=[oper_result,'value']
                        self.count_stack=self.count_stack[:-1]
                    else:
                        print('ERROR: wrong types')
                        return -1
                if operators[stack[i]] in ['=']:
                    values=self.unpack(number=2)
                    types=self.get_type(values)
                    if operators[stack[i]]=='=':
                        if isnan(types[0]) and isnan(types[1]):
                            print('ERROR: both operands are undefined')
                            return -2
                        elif types[0]==types[1] or isnan(types[0]):
                            self.operands[self.count_stack[-2][0]][2]=values[1]
                            self.count_stack[-2]==[values[1],'value']
                            self.count_stack=self.count_stack[:-1]
                        else:
                            print('ERROR: worong types, trying to write {}->{}'.format(values[1],types[0]))
                            return -2
                if operators[stack[i]] in ['--','print','goto']:
                    value=self.unpack(number=1)
                    if operators[stack[i]]=='--' and self.get_type(value):
                        self.count_stack[-1]=[value*-1,'value']
                    if operators[stack[i]]=='print':
                        print(value)
                        self.count_stack=self.count_stack[:-1]
                    if operators[stack[i]]=='goto':
                        adress=self.unpack(number=1)
                        self.count_stack=self.count_stack[:-1]
                        i=adress
                        continue
                if operators[stack[i]] in ['>0','<0','==0','>=0','<=0']:
                    operator=operators[stack[i]]
                    values=self.unpack(number=2) ## value+mark
#                     print(str(values[0])+operator)
                    result=eval(str(values[0])+operator)  ## condition on value
                    if result: ## go further
                        i+=1
                        self.count_stack=self.count_stack[:-2]
                        continue
                    else: # go on mark
                        i=values[1]
                        self.count_stack=self.count_stack[:-2]
                        continue
            i+=1
        return self.operands
    def unpack(self,number=2):
        '''
            Get 1(2) values from count_stack by link or value
        '''
        result=[]
        if number==2:
            for i in self.count_stack[-2:]:
                if i[1]=='link':
                    result.append(self.operands[i[0]][2])
                    continue
                elif i[1]=='value':
                    result.append(i[0])
                    continue
                else:
                    print('Unknown type')
            #print(result)
            return result
        if number==1:
            temp=self.count_stack[-1]
            return (self.operands[temp[0]][2] if self.count_stack[-1][1]=='link' else temp[0])
    def get_type(self,x):
        '''
        input: x - list or single value
        output: list or single string - type of x
        '''
        a=x if isinstance(x,(list,tuple)) else [x]
        to_ret=[]
        for i in a:
            if isnan(i):
                to_ret.append(np.NAN)
            else:
                if isinstance(i, (int, long, float)):
                    to_ret.append('numeric')
                else:
                    to_ret.append('str')
        return(to_ret if len(to_ret)>1 else to_ret[0])
def isnan(x):
    '''
    universal check for nan
    '''
    return x!=x
operators={-1:'+',-2:'-',-3:'*',-4:'/',-10:'=',-5:'--',-6:'print',-7:'goto',
          -20:'>0',-21:'<0',-22:'==0',-23:'>=0',-24:'<=0'}
operands={1:[1,'numb',1],2:[2,'numb',2],3:[3,'numb',3],4:[4.5,'numb',4.5],
          5:['some_string','char','some_string'],6:['a','var',np.NaN],7:['b','var',np.NAN],8:['c','mark',11]}
if __name__ == "__main__":
    st=open(sys.argv[1],'r')
    st=st.read().split(' ')
    if '\n' in st[-1]:
        st[-1]=st[-1][:-1]
    stack=[int(x) for x in st]
    if len(sys.argv)==3:
        if sys.argv[2]=='Trace':
            worker=Interpreter(stack,operands,True)
            print(worker.count_reversed_form(stack))
    else:
        worker=Interpreter(stack,operands,False)
        worker.count_reversed_form(stack)     


