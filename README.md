# xmarie-vm
Virtual machine emulator targetting the eXtended MARIE (XMARIE) architecture.

## Architecture overview
XMARIE is an extension of the [MARIE](http://cf.linnbenton.edu/bcs/cs/parisj/upload/cs271-marie.pdf) architecture.
XMARIE offers an extended set of instructions, as well as new features missing in the original architecture.

### Numbers
XMARIE works with integers (both positive and negative). They are represented using the [Two's Complement](https://en.wikipedia.org/wiki/Two%27s_complement) method.

### Memory
Each memory address is **12 bits** long. The memory is not automatically nullified - the original content is undefined. It is up to the programmer to assure that the memory is zeroed out when necessary.

### Registers
XMARIE consists of seven registers. They fall into two categories - internal and general use registers.

#### Internal registers
- **PC** (Program Counter) - Stores the address of the instruction currently being executed.
- **MAR** (Memory Address Register) - Stores the address from which data will be read.
- **MBR** (Memory Buffer Register) - Upon each read operation, the content of the address stored in MAR will be fetched into MBR.
- **IR** (Instruction Register) - Stores the currently executed instruction.
- **AC** (Accumulator) - Stores the current state of calculation. Many instructions implicitly alter the content stored in AC.

#### General registers
- **X**
- **Y**

### Stack
XMARIE features a LIFO stack which supports two opearations.
- **Push** - Puts the content of AC on the top of the stack.
- **Pop** Removes the topmost element from the stack and stores it in AC.

### Instructions
Each instruction takes **20 bits** (8 for opcode, 12 for argument)
To simplify the description of instructions, let me introduce a shorthand notation.
Let **M(X)** denote the value stored at address *X* in memory. 

#### Direct arichmetics
- **Add X** -> AC = AC + M(x)
- **


## Features

## Api

## Installation
