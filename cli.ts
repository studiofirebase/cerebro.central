import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const OLLAMA_URL = "http://localhost:11434/api/generate";
const MODEL = "mistral"; // Altere para deepseek-coder:6.7b se preferir

let context: string[] = [];

console.clear();
console.log('\x1b[35m%s\x1b[0m', '🤖 MiniCopilot CLI Iniciado! (Digite "sair" para encerrar)');
console.log('\x1b[90m%s\x1b[0m', `Modelo: ${MODEL} | Contexto: 2048 (Otimizado para 8GB RAM)`);
console.log('--------------------------------------------------\n');

function ask() {
  rl.question('\x1b[32mVocê:\x1b[0m ', async (input) => {
    if (input.toLowerCase() === 'sair' || input.toLowerCase() === 'exit') {
      console.log('\x1b[90mEncerrando MiniCopilot...\x1b[0m');
      rl.close();
      return;
    }

    if (!input.trim()) {
      ask();
      return;
    }

    const contextStr = context.slice(-10).join('\n');
    const fullPrompt = `You are a senior software engineer assistant.\n\n${contextStr}\nuser: ${input}\nassistant:`;

    try {
      process.stdout.write('\x1b[36mMiniCopilot:\x1b[0m ');
      
      const response = await fetch(OLLAMA_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: MODEL,
          prompt: fullPrompt,
          stream: true,
          options: {
            num_ctx: 2048,
            temperature: 0.7,
            num_predict: 500
          }
        })
      });

      if (!response.ok) {
        console.log(`\n\x1b[31mErro na API do Ollama: Verifique se o Ollama está rodando localmente.\x1b[0m`);
        ask();
        return;
      }

      let fullResponse = '';
      
      if (response.body) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          const chunk = decoder.decode(value);
          const lines = chunk.split('\n').filter(Boolean);
          
          for (const line of lines) {
            try {
              const data = JSON.parse(line);
              process.stdout.write(data.response);
              fullResponse += data.response;
            } catch (e) {
              // Ignore parse errors for incomplete chunks
            }
          }
        }
      }
      
      console.log('\n');
      context.push(`user: ${input}`);
      context.push(`assistant: ${fullResponse}`);
      
    } catch (error: any) {
      console.log(`\n\x1b[31mErro de conexão: Certifique-se de que o Ollama está rodando (ollama serve).\x1b[0m`);
    }

    ask();
  });
}

ask();
