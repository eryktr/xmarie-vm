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

#### Direct arithmetics
- **Add X** -> AC = AC + M(X)
- **Subt X** -> AC = AC - M(X)
- **Incr** -> AC = AC + 1
- **Decr** -> AC = AC - 1
- **ShiftL X** -> AC = AC * 2^M(X)
- **ShiftR X** -> AC = floor(AC / 2^M(X))
- **Clear** -> AC = 0

#### Indirect arithmetics
- **AddI X** -> AC = AC + M(M(X))
- **SubtI X** -> AC = AC - M(M(X))

#### Direct data transfer
- **Load X** -> AC = M(X)
- **Store X** -> M(X) := AC
- **StoreX** -> X := AC
- **StoreY** -> Y := AC

#### Indirect data transfer
- **LoadI X** -> AC = M(M(X))
- **StoreI X** -> M(M(X)) := AC

#### I/O
 - **Output** -> Print the content of AC to stdout

#### Control flow
- **JnS X** -> Store current value of PC in X, then set PC to X + 1.
- **Jump X** -> PC := X
- **Halt** -> Stop the program

#### Stack
- **Push**
- **Pop**

## Sample Code
The below code sample reads an integer N from the user and outputs the sum from 1 to N.
```
    Store N
    Loop, Load SUM
    Add N
    Store SUM
    Load N
    Decr
    Store N
    Skipcond 400
    Jump Loop
    Load SUM
    Output
    Halt

    N, DEC 0
    SUM, DEC 0
```

## Api

### MarieVm
The main construction exported by the xmarie-vm project is the **MarieVm** class. Its constructor takes the following arguments:
- `memory` - list of integers. The initial state of the memory
- `input stream` - an object which implements the `read() -> str` method
- `outpt stream` - an object which extends the OutputStream abstract base class 
- `stack` - list of integers - the initial state of the stack - possibly an empty list. The closer an element is to the beginning of the list, the closer to the top of the stack it is.
- `max_num_executed_instrs` - the maximum number of executed instructions, after which the currently running program will be terminated.

### Breakpoints
The module `xmarievm/breakpoints.py` provides provides breakpoint abstractions that will be used for debugging.
The code provided by user is `minified` before being parsed - the main change is that blank lines are removed. To keep track 
of the place in the original code certain breakpoint refers to, each breakpoint needs to consist of these three things: 
1. current line
2. original line
3. instruction

The **current line** is the line number in the minified code and **original line** is the line number certain instruction 
was on in the original code (the one provided by user to be executed)

The list of breakpoints can be conveniently generated using the `parse_breakpoints` function from this module. It takes in two arguments
1. breakpoints - list of integers corresponding to line numbers of instructions that are marked with breakpoints. For example, if you want to put a breakpoint in the second and fifth line in the code provided as argument, you want to pass in the list `[2, 5]`.
2. code - the code to be executed, represented as string.

The function will return a list of `Breakpoint` objects.

### Snapshots
The module `xmarievm/runtime/snapshot_maker.py` provides the implementation of the `Snapshot` object. That is a data transfer object representing the state of the VM at a given point in time. The fields it has correspond to the fields in the VM. The object can therefore easily be converted to formats like JSON.

The `make_snapshot` function is a utility for quick snapshot generation. Its only argument is the `vm` instance whose snapshot will be taken.

## Installation
1. Clone the repository
2. cd into the main directory (the one containing the setup.py file)
3. Run
```
pip install -e .
```
4. If you want to also install development dependencies, instead run
```
pip install -e "[.dev]"
```

`xmarie-vm` is also available as a package, but it's not currently available on PyPi.
