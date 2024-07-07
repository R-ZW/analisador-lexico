import { input, closeRL } from '../input';

async function main() {
    const n1 = await input('n1: ');
    const n2 = await input('n2: ');
    const soma:number = parseInt(n1)+parseInt(n2);

    console.log(`n1 + n2 = ${soma}`);
}

main();