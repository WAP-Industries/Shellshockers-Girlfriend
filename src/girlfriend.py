import google.generativeai as genai
import winsound, re, torch
from num2words import num2words
from utils import *


class Girlfriend:
    Model = None
    Prompt = []
    TTS = None
    Memory = None
    
    Window = None
    Sprites = []
    Width = Height = 0

    Name = ""
    BlushSound = "(blushes)"
    Blushing = False
    Ended = False
    
    VoiceFile = f"{Utils.Root}\\voice.wav"
    MemoryFile = "memory"
    MemSep = " ===== "

    @staticmethod
    def Init() -> None:
        genai.configure(api_key=os.environ.get("KEY"))
        Girlfriend.Model = genai.GenerativeModel('gemini-1.0-pro-latest')

        Girlfriend.Name = os.environ.get("NAME")

        with open("assets\\prompt.txt", "r") as f:
            Girlfriend.Prompt = [f.read().strip().replace("GF_NAME", Girlfriend.Name).replace("GF_BLUSHSOUND", Girlfriend.BlushSound)]

        Girlfriend.Width, Girlfriend.Height = map(lambda x: int(os.environ.get(x)), ["WIDTH", "HEIGHT"])
        Girlfriend.Window = Utils.CustomWindow(Girlfriend.Width, Girlfriend.Height)
        Utils.LoadSprite("egg.png", 0, 0, Girlfriend.Width, Girlfriend.Height)

        try:
            Girlfriend.TTS = torch.package.PackageImporter("model.pt").load_pickle("tts_models", "model")
            Girlfriend.TTS.to(torch.device('cpu'))

        except Exception as e:
            return Girlfriend.Error("initialise TTS model", e)

        try:
            Girlfriend.Memory = Utils.Client.get_collection(Girlfriend.MemoryFile)
        except:
            Girlfriend.Memory = Utils.Client.create_collection(Girlfriend.MemoryFile)

    @staticmethod
    def GetInput() -> str:
        with sr.Microphone() as source: 
            audio = Utils.SST.listen(source) 
    
        try: 
            return Utils.SST.recognize_google(audio, language='en-in').lower().strip()
        
        except Exception as e:
            return Girlfriend.Error("record voice", e)

    @staticmethod
    def GetResponse(prompt: str) -> str:
        if prompt=="exit":
            Girlfriend.Close()
            return "Goodbye my pookie wookie"
        if prompt=="reset":
            Girlfriend.Reset()
            return "Successfully resetted"

        try:
            relevant = Girlfriend.Memory.query(
                query_texts=[prompt],
                n_results=3,
            )["documents"][0][::-1]
            
            history = "This is our past conversation"
            for i in relevant:
                conv = i.split(Girlfriend.MemSep)
                history+=f"\nMe: {conv[0]}\n{Girlfriend.Name}: {conv[1]}"

            Girlfriend.Prompt.append(history)
        except:
            ...

        Girlfriend.Prompt.append(prompt)

        try:
            response = Girlfriend.Model.generate_content(
                '\n\n'.join(Girlfriend.Prompt),
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            ).text.lower()
            
            if response.find(Girlfriend.BlushSound)!=-1:
                response = response.replace(Girlfriend.BlushSound, "")
                Girlfriend.Blushing = True

            return response
        
        except Exception as e:
            return Girlfriend.Error("get answer", e)
        
    @staticmethod
    def Speak(text: str) -> None:
        Utils.RemoveVoice()

        try:
            Girlfriend.TTS.save_wav(
                text=re.sub(r"(\d+)", lambda x: num2words(int(x.group(0))), text), 
                speaker="en_21", 
                sample_rate=48000, 
                audio_path=Girlfriend.VoiceFile
            )

            if Girlfriend.Blushing and len(Girlfriend.Sprites)<2:
                Utils.LoadSprite("blush.png", 0, Girlfriend.Height//4, Girlfriend.Width, Girlfriend.Height//2)
                
            winsound.PlaySound(Girlfriend.VoiceFile, winsound.SND_FILENAME)
            Utils.RemoveVoice()

        except Exception as e:
            Girlfriend.Error("speak input", e)

    @staticmethod
    def SaveMemory(input, prompt):
        Girlfriend.Memory.add(
            documents=[f"{input}{Girlfriend.MemSep}{prompt}"],
            ids=[str(len(Girlfriend.Memory.get()["documents"]))]
        )

    @staticmethod
    def Close() -> None:
        Girlfriend.Window.quit() and Girlfriend.Window.destroy()
        for _ in range(len(Girlfriend.Sprites)):
            Utils.RemoveSprite()

        Utils.RemoveVoice()
        Girlfriend.Ended = True

    @staticmethod
    def Reset() -> None:
        for i in Girlfriend.Memory.get()["ids"]:
            Girlfriend.Memory.delete(i)

    @staticmethod
    def Error(action: str, error: str) -> None:
        print(f"Failed to {action}: {error}")