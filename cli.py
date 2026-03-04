import urllib.request
import json
import sys
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral" # Altere para deepseek-coder:6.7b se preferir

def chat():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[95m🤖 MiniCopilot CLI Iniciado!\033[0m (Digite 'sair' para encerrar)")
    print(f"\033[90mModelo: {MODEL} | Contexto: 2048 (Otimizado para 8GB RAM)\033[0m")
    print("-" * 50 + "\n")
    
    context = []
    
    while True:
        try:
            user_input = input("\033[92mVocê:\033[0m ")
                
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("\033[90mEncerrando MiniCopilot...\033[0m")
                break
                
            if not user_input.strip():
                continue

            context_str = "\n".join(context[-10:])
            full_prompt = f"You are a senior software engineer assistant.\n\n{context_str}\nuser: {user_input}\nassistant:"

            data = json.dumps({
                "model": MODEL,
                "prompt": full_prompt,
                "stream": True,
                "options": {
                    "num_ctx": 2048,
                    "temperature": 0.7,
                    "num_predict": 500
                }
            }).encode('utf-8')

            req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
            
            print("\033[96mMiniCopilot:\033[0m ", end="", flush=True)

            full_response = ""
            try:
                with urllib.request.urlopen(req) as response:
                    for line in response:
                        if line:
                            chunk = json.loads(line.decode('utf-8'))
                            text = chunk.get("response", "")
                            full_response += text
                            print(text, end="", flush=True)
            except Exception as e:
                print(f"\n\033[31mErro de conexão: Certifique-se de que o Ollama está rodando (ollama serve).\033[0m")
                continue
            
            print("\n")
            
            context.append(f"user: {user_input}")
            context.append(f"assistant: {full_response}")

        except KeyboardInterrupt:
            print("\n\033[90mEncerrando MiniCopilot...\033[0m")
            break
        except Exception as e:
            print(f"\n\033[31mErro: {e}\033[0m")

if __name__ == "__main__":
    chat()
