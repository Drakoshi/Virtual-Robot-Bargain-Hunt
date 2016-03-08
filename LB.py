
import pickle

def leader(Cat):
    try:
        #opening the file to check what the highscore is
        name = Cat.name
        score = value(Cat)
        file = open("leader.txt","rb")
        points= pickle.load(file)
        name = pickle.load(file)
        
        #if the score is higher than old highscore
    
        if score > points :
            print(score)
            print ("You beat the highscore!")
            file = open("leader.txt","wb")
            pickle.dump(score,file)
            pickle.dump(name)
            addleader()
            file.close()
        #if it is not
        else:
            pass
    except:
        file = open("leader.txt","wb")
        pickle.dump(score,file)
        pickle.dump(name,file)
        file.close()
        
        


#caculating the score
def value(Cat):
    score = 0
    for i in Cat.inventory:
        score += i.quality
    return score
