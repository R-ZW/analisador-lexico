import * as readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

export function input(texto: string) {
  return new Promise<string>((resolve, reject) => {
    rl.question(texto, (answer) => {
      resolve(answer);
    });
  });
}

export function closeRL() {
  rl.close();
}