# Bitwrap-machine

A library used by http://getbitwrap.com to use Petri-Net Markup files as a state machine DSL.

#### What is a bitwrap state machine?

![tic-tac-toe state machine](https://bitwrap.github.io/image/octothorpe.png)

(above is a tic-tac-toe state machine )

A Bitwrap machine can be explained as follows:

    1. It declares a single 'state-vector' of size 'n'
       * the machine is said to have 'n' places
       * each place(n) has a pre-defined initial value.
    2. 'transitions' are defined as a set of delta vectors
       * of size 'n' 
       * containing positive or negative integers.
    3. Transactions are applied to the current state vector using vector addition.
    4. The 'state-vector' is stored after each valid transaction.
    5. No place(n) may store a negative value.
       * only valid output states are stored

## References

* [PIPEv5](https://github.com/sarahtattersall/PIPE) - Java Petri-Net Editor
* [pntools](https://github.com/irgangla/pntools/blob/master/LICENSE) - PNML XML parser
