import random as rnd
possible_states = [
        list(range(0, 51)) + list(range(52, 58)),  # Blue
        list(range(13, 52)) + list(range(0, 12)) + list(range(58, 64)),  # Red
        list(range(26, 52)) + list(range(0, 25)) + list(range(64, 70)),  # Green
        list(range(39, 52)) + list(range(0, 38)) + list(range(70, 76))  # Yellow
    ]
home_states=[list(range(52, 58)), #b
             list(range(58, 64)), #r
             list(range(64, 70)), #g
             list(range(70, 76))] #y
star_positions=[8,21,34,47]
initial_positions=[0,13,26,39]
home_positions=[57,63,69,75]
current_state=[[-1, 22, -3, -4], # Blue
                [19, 21, 27, -8],   #red
                [26, 35, -11, 47],     #green
                [43, -14, 51, -16]]       #yellow

dice_value=2
c_coin=[1,0]    #blue ko second coin
class Perceptron:
    _inputs=[]

    def __init__(self,current_state,c_coin,dice_value):
        self._weights=[0.8,0.7,0.6,0.4,0.3,0.2,0.5,0.7]
        self._current_state=current_state
        self._c_coin=c_coin
        self._dice_value=dice_value
        self.can_attack_enemy()
        self.can_escape_enemy()
        self.is_safe()
        self.can_reach_home_states()
        self.can_be_attacked()
        self.can_reach_star()
        self.is_it_home()
    
    def can_attack_enemy(self):
        count=0
        if(self._current_state[c_coin[0]][c_coin[1]]>=0):
            pos=possible_states[c_coin[0]][possible_states[c_coin[0]].index(self._current_state[c_coin[0]][c_coin[1]])+self._dice_value]
            for i in self._current_state:
                if i!=self._current_state[c_coin[0]]: #loop through current state except  of which we are computing
                    for j in i:
                        if j==pos and j not in star_positions and j not in initial_positions:
                            count+=1
            if count==1:    #in count is more than 1, then we can't eliminate multistacked coins
                self._inputs.append(1)
            else:
                self._inputs.append(0)
        # print(self._inputs)

    def can_escape_enemy(self): #current position+ dice roll - enempy pos >6,then it can escape enemy,  doesn't account star and home, as it is evaluated in other functions
        count=0
        if(self._current_state[c_coin[0]][c_coin[1]]>=0):
            pos=possible_states[c_coin[0]][possible_states[c_coin[0]].index(self._current_state[c_coin[0]][c_coin[1]])+self._dice_value]
            icount=0
            for i in self._current_state:
                if i!=self._current_state[c_coin[0]]: #loop through current state except  of which we are computing
                    for j in i:
                        if j>=0: # if j is still negative, i.e., its hasn't come outside
                            if possible_states[icount].index(pos)>possible_states[icount].index(j):
                                index_wrt_enemy=possible_states[icount].index(pos) #index in possible states of enemy at where the board position of given coin is
                                index_of_enemy=possible_states[icount].index(j)
                                if index_wrt_enemy-index_of_enemy>6:
                                    count+=1
                icount+=1
            if count>=1:    #could be made such that, the more enemy it can escape, more weight will be there
                self._inputs.append(1)
            else:
                self._inputs.append(0)

    def is_safe(self): # is it in initial position or star position
        if(self._current_state[c_coin[0]][c_coin[1]]>=0):
            pos = self._current_state[c_coin[0]][c_coin[1]] 
            if pos == initial_positions[c_coin[0]] or pos in star_positions:
                self._inputs.append(1)  #safe vayo vani, we wouldn't want to move
            else:
                self._inputs.append(0)
            # if pos in home_states[c_coin[0]] or pos in star_positions:
            #     self._inputs.append(0)  #safe vayo vani, we wouldn't want to move
            # else:
            #     self._inputs.append(1)
        

    def can_reach_home_states(self): #by safety, i mean inside
        if(self._current_state[c_coin[0]][c_coin[1]]>=0):
            pos=possible_states[c_coin[0]][possible_states[c_coin[0]].index(self._current_state[c_coin[0]][c_coin[1]])+self._dice_value]
            if pos in home_states[c_coin[0]]:
                self._inputs.append(1)
            else:
                self._inputs.append(0)

    def can_be_attacked(self): # if current pos - enemy pos <=6, then it can be attacked
        count=0
        if(self._current_state[c_coin[0]][c_coin[1]]>=0):
            pos=possible_states[c_coin[0]][possible_states[c_coin[0]].index(self._current_state[c_coin[0]][c_coin[1]])]
            icount=0
            for i in self._current_state:
                if i!=self._current_state[c_coin[0]]: #loop through current state except  of which we are computing
                    for j in i:
                        if j>=0:
                            if possible_states[icount].index(pos)>possible_states[icount].index(j):
                                index_wrt_enemy=possible_states[icount].index(pos) #index in possible states of enemy at where the board position of given coin is
                                index_of_enemy=possible_states[icount].index(j)
                                # if index_wrt_enemy-index_of_enemy<=6 or pos == initial_positions[c_coin[0]]:
                                if index_wrt_enemy-index_of_enemy<=6:
                                    count+=1
                icount+=1
            if count>=1:    #could be made such that, the more enemy it can escape, more weight will be there
                self._inputs.append(1)
            else:
                self._inputs.append(0)

    def can_reach_star(self):
        if(self._current_state[c_coin[0]][c_coin[1]]>=0):
            pos=possible_states[c_coin[0]][possible_states[c_coin[0]].index(self._current_state[c_coin[0]][c_coin[1]])+self._dice_value]
            if pos in star_positions:
                self._inputs.append(1)
            else:
                self._inputs.append(0)
    
    def is_it_home(self):
        if(self._current_state[c_coin[0]][c_coin[1]]>=0):
            pos=possible_states[c_coin[0]][possible_states[c_coin[0]].index(self._current_state[c_coin[0]][c_coin[1]])+self._dice_value]
            if pos == home_positions[c_coin[0]]:
                self._inputs.append(1)
            else:
                self._inputs.append(0)
            # if pos == home_positions[c_coin[0]]:
            #     self._inputs.append(0)
            # else:
            #     self._inputs.append(1)
        
    def print_inputs(self):
        print(self._inputs)

    


    




per1=Perceptron(current_state,c_coin,dice_value)
per1.print_inputs()
