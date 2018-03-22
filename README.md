# RelayController
Python project for controling relays in a home automation system

Circuit Diagram


VCC   --------------------------------------------------+-----+-----+-------------------------+-------------+
                                                        |     |     |                         |             |
                                                        |     |     |                         |             |
                                                       [ ]   [ ]   [ ] 3x10K                  |             |
                                                       [ ]   [ ]   [ ]                        |             |
                                                       [ ]   [ ]   [ ]                        |             |
                                                        |     |     |                         |             |
                                                        |     |     |                         |             |
    ----------------------------------------------------------------+----------------------------------     |
   |  --------------------------------------------------------+-------------------------------------   |    |
   |  |                                                 |                                     |  |  |  |    |
   |  |     Raspberry Pi                                 ----------------------------------------   |  |    |
   |  |     GPIO Breakout Header                                                              |  |  |  |    |
   |  |      _______________                                                                  |  |  |  |    |
   |  |     |               |                                                                 |  |  |  |    |
   |  |     | 3v3       5v0 |                                                                 |  |  |  |    |
   |  |     | SDA       5v0 |                                                                 |  |  |  |    |
   |  |     | SCLK      GND |                                                                 |  |  |  |    |
   |  |     | 4         TXD |                                                                 |  |  |  |    |
   |  |     | GND       RXD |                                                                 |  |  |  |    |
   |  ------| 17         18 |                                                                 |  |  |  |    |
   |        | 21/27     GND |                                                                 |  |  |  |    |
    --------| 22         23 |-------------------+-------------------                          |  |  |  |    |
            | 3v3        24 |-------------+----------------------- |                          |  |  |  |    |
            | MOSI      GND |             |     |                | |        SN74HC259         |  |  |  |    |
            | MISO       25 |-------+--------------------------- | |      _______________     |  |  |  |    |
            | SCLK      CE0 |       |     |     |              | | |     |               |    |  |  |  |    |
            | GND       CE1 |       |     |     |              | | |     |               |    |  |  |  |    |
            |_______________|      [ ]   [ ]   [ ]  3x220R     | | |-----| S0        Vcc |----   |  |  |    |        Relay Array
                                   [ ]   [ ]   [ ]             | |-------| S1       !CLR |-------   |  |    |      _______________
                                   [ ]   [ ]   [ ]             |---------| S2         !G |----------   |    |     |               |
                                    |     |     |           |------------| Q0          D |-------------     |-----| Vcc           |
                                    |     |     |           |  |---------| Q1         Q7 |------------------------| R7            |
                                    |     |     |           |  |  |------| Q2         Q6 |------------------------| R6            |
                                    |     |     |           |  |  |  |---| Q3         Q5 |------------------------| R5            |
                                    |     |     |           |  |  |  | |-| GND        Q4 |------------------------| R4            |
                                    |     |     |           |  |  |  | | |_______________|                        |               |
                                    |     |     |           |  |  |  |--------------------------------------------| R3            |
                                    |     |     |           |  |  |-----------------------------------------------| R2            |
                                    |     |     |           |  |--------------------------------------------------| R1            |
                                    |     |     |           |-----------------------------------------------------| R0            |
                                    |     |     |                      |                                    |-----| GND           |
                                    |     |     |                      |                                    |     |_______________|
                                    |     |     |                      |                                    |
GND   ------------------------------+-----+-----+----------------------+------------------------------------+
