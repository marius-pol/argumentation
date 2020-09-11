# Conflict–Abduction–Negation (CAN) argumentation procedure

Python implementation of the Conflict–Abduction–Negation (CAN) procedure, based on the following paper.

Dessalles JL. (2016) _A Cognitive Approach to Relevant Argument Generation_. In: Baldoni M. et al. (eds) Principles and Practice of Multi-Agent Systems. CMNA 2015, IWEC 2015, IWEC 2014. Lecture Notes in Computer Science, vol 9935. Springer, Cham. [https://doi.org/10.1007/978-3-319-46218-9_1](https://doi.org/10.1007/978-3-319-46218-9_1)

# Overview

The CAN procedure generates dialogues similar to the ones observed in real-life conversations based on domain knowledge about an argumentation world. The argumentation world must support performing abduction (i.e. the reasoning process of looking for a possible cause for a state), and executing actions.

# Example

Here is the example of the real-life conversation to be generated, from the paper cited above:

Context: A is repainting doors. He decided to remove the old paint first, which proves to be a hard work (adapted from French)  
A1 - I have to repaint my doors. I've burned off the old paint. It worked OK, but not everywhere. It's really tough work! \[...\] In the corners, all this, the moldings, it's not feasible!  
B1 - You should use a wire brush.  
A2 - Yes, but that wrecks the wood.  
B2 - It wrecks the wood...  
\[pause 5 seconds\]  
A3 - It's crazy! It's more trouble than buying a new door.  
B3 - Oh, that's why you'd do better just sanding and repainting them.  
A4 - Yes, but if we are the fifteenth ones to think of that!  
B4 - Oh, yeah...  
A5 - There are already three layers of paint.  
B5 - If the old remaining paint sticks well, you can fill in the peeled spots with filler compound.  
A6 - Yeah, but the surface won't look great. It'll look like an old door.  

The output of the CAN procedure implementation that generates the structure of this conversation is the following:

```
(Re)start procedure in argumentation_world  
conflict on -NiceDoors  
- solution Repaint performed  
conflict on -NiceDoors  
- solution BurnOff performed  
conflict on ToughWork  
- solution WireBrush performed  
conflict on -NiceDoors  
- solution -WireBrush performed  
conflict on ToughWork  
- solution -BurnOff performed  
conflict on -NiceDoors  
- solution Sanding performed  
conflict on -NiceDoors  
- solution FillerCompound performed  
no more conflicts  
```

# Implementation details

The Python implementation of the CAN procedure provides an abstract class for an argumentation world supporting performing abduction and executing actions. There are two types of world implementing this abstract class: a logic world, which generates the output above, and an action world, which will be further extended with an application in the smart home domain based on the [icasamanager](https://github.com/marius-pol/icasamanager) project.


# Installation

The Python 3 implementation requires the nltk package for managing the argumentation world, which may be installed with:

```
  pip3 install -r requirements.txt
```
