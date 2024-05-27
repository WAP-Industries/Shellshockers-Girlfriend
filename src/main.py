import sys
sys.dont_write_bytecode = True 

from dotenv import load_dotenv
import threading
from girlfriend import *


def main():
    while 1:
        if Girlfriend.Ended:
            return
        
        Girlfriend.Blushing = False
        if len(Girlfriend.Sprites)>1:
            Utils.RemoveSprite()

        prompt = Girlfriend.GetInput()
        response = Girlfriend.GetResponse(prompt) if prompt else "I'm sorry, could you repeat that?"
        Girlfriend.Speak(response)
        
        Girlfriend.Prompt = [Girlfriend.Prompt[0]]
        
        if prompt:
            Girlfriend.SaveMemory(prompt, response)

if __name__=="__main__":
    load_dotenv()
    threading.Thread(target=main).start()
    Girlfriend.Init()
    Girlfriend.Window.mainloop()