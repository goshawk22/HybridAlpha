from Coach import Coach

from tictactoe.TicTacToeGame import TicTacToeGame as Game
from tictactoe.tensorflow.NNet import NNetWrapper as nn

from othello.OthelloGame import OthelloGame as Game1
from othello.tensorflow.NNet import NNetWrapper as nn1

from gobang.GobangGame import GobangGame as Game2
from gobang.tensorflow.NNet import NNetWrapper as nn2

from connect4.Connect4Game import Connect4Game as Game3
from connect4.tensorflow.NNet import NNetWrapper as nn3



from utils import *


'''

    numIters - represents the number of iterations
    
    numEps - the number of games that is played during each iteration
    
    tempThreshold - represents how many moves in each game to be chosen based on temperature=1(for more info
                    check DeepMind paper)
    
    updateThreshold - represents the percentage of games the new network needs to win in order to become the network 
                      that will generate the examples in the next iteration
    
    maxlenOfQueue - represents how many examples do you want to store in the queue
    
    numMCTSSims - represents the number of simultation to be done at every move
    
    arenaCompare - represents the number of matches to play against the old network and against the baselines at every
                    iteration. Baselines are greedy, random, and minimax with alfa-beta pruning
    
    cpuct - represents a coefficient that weights the exploration factor over the exploitation factor
    
    parallel - when you want to evaluate your network against greedy, random and alfa-beta at the same time every iteration
                Be aware that in order to do this you need to set the GPU memory for the main process as to have
                enought memory to run all 4 processes(one for each baseline + one for the main process)
                
    dirAlpha - represent the factor that is passed to dirichlet function in order to generate the dirichlet noise

    epsilon - represents how important dirichlete noise is when added to prior probabilities generated by the network
    
    checkpoint - represents the main folder which contains all weights and examples for all games. Look at temp folder
                 to see how everything is organised
    
    load_model - represents whether you want to continue your training from an weight file or you want to start from 0
    
    
    load_folder_file - is used to point from where to load the example files in order to continue your training. You need
                        to set load_model in order to use this option.
    
    numItersForTraininExampleHistory - represents how many examples will be used for training. After the number of 
                                        iterations exced this number, it will start to delete at every iteration the first
                                        batch of examples from the queue, and in add the new batch(generated in the current
                                        iteration), so you will have in the examples queue
                                        at most numItersForTrainingExampleHIstory batches.
    
    trainExampleCheckpoint - represents the folder used to load the values stored in log files if you want to continue
                             your training. You need to set load_model=True
                             
    name - represents the name of the game and it will be used to generate from a factory the agents coresponding to
            that game (e.g GreedyOthello, MinMaxTicTacToe)
'''


args = dotdict({
    'numIters': 75,
    'numEps': 610,
    'tempThreshold': 15,
    'updateThreshold': 0.55,
    'maxlenOfQueue': 40000,
    'numMCTSSims':850,
    'arenaCompare': 14,
    'cpuct': 2.0,
    'parallel': 0,
    'dirAlpha': 0.75,
    'epsilon': 0.25,
    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('./temp/gobang/','checkpoint_0.pth.tar'),
    'numItersForTrainExamplesHistory': 10,

})

if __name__=="__main__":

    choice="gobang"

    if choice=="tictactoe":
        g = Game(5)
        nnet = nn(g)
        args.update({'trainExampleCheckpoint': './temp/tictactoe/'})
        args.update({'name': 'tictactoe'})
    if choice=="othello":
        g = Game1(6)
        nnet = nn1(g)
        args.update({'trainExampleCheckpoint': './temp/othello/'})
        args.update({'name': 'othello'})
    if choice=="gobang":
        g=Game2(5,3)  # the second parameter is actually the number of continous pieces in order to win
        nnet = nn2(g)
        args.update({'trainExampleCheckpoint': './temp/gobang/'})
        args.update({'name': 'gobang'})
    if choice=="connect4":
        g=Game3(6,7)
        nnet=nn3(g)
        args.update({'trainExampleCheckpoint': './temp/connect4/'})

        args.update({'name': 'connect4'})

    filenameBest = "best" + str(args.numIters) + ":eps" + str(args.numEps) + ":dim" + str(
        g.n) + ".pth.tar"

    if args.load_model:
        nnet.load_checkpoint(args.checkpoint, filenameBest)

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()