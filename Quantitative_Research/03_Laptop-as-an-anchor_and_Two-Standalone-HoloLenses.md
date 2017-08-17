# 03 Laptop as an Anchor and Two Stand-Alone HoloLenses

* Here's an illustration showing the setup for this report.

![Laptop-As-Anchor](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Laptop_as_Anchor.png)

* Content:
   * [Overview of Data Types](#overview-of-data-types)
   * [Protocols Used by the HoloLens](#protocols-used-by-the-hololens)

## Overview of Data Types
* The type of data that can be sent/received by the HoloLens depends on how the holograhic application was developed.
* In our case, we used Unity and C#. Unity apps written in C# have the following data types at their disposal:
    * **int**
        * *e.g. 5 (4 bytes)*
        * Useful for identifying few items, e.g. if you want to ID 50 different HoloLenses
    * **long**
        * *e.g. -462863389 (8 bytes)*
        * Assuming you have millions of IoT devices, you may need a long to represent their IDs
    * **byte**
        * Useful for communicating states, e.g. stop showing hologram X
    * **Vector3**
        * *e.g. (3, 2.64, -2) (3 floats --> 12 bytes)*
        * Useful for communicating coordinates; 2 vector3's can denote direction
    * **Quaternion**
        * *e.g. (4, 46, -4.21, -984) (4 floats --> 16 bytes)*
        * Used by Unity to represent rotations of game objects (in our case, holograms).

* The amount of data sent can be reduced by aggregating (with a tradeoff in the AR quality of service, e.g. update rates) since data is padded before being sent. Therefore, sending 30,000 ints will use more data than sending 10,000 vector3's.

## Protocols Used by the HoloLens
* Tristan Braud's 2017 paper, ['Future Networking Challenges: The Case of Mobile AR'](https://github.com/dchege711/Augmented_Reality/blob/master/Related_Work/2017_Tristan_Braud_Future_Networking_Challenges.md) proposes a need for a protocol designed for AR, lest AR applications prove unsustainable under the current (and projected) infrastructure.
* We thus wanted to know what protocol is used by the HoloLens, and this is what we found:

![Protocol_Distribution](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Chege_to_HL_by_Protocol.png)

* The above data was collected for a HoloLens that was sending 12,000 integers per second to the network.
* Of the 131.45 MB transferred, following distribution was observed:

    * **TCP Protocol: 1.66 %**
      * The information in these packets is of the form:
         * *443  >  50362 [FIN, ACK] Seq=2422 Ack=902 Win=66048 Len=0*
      * TCP provides reliable end-to-end connection. Lost packets are re-transmitted.
         
    * **TLSv1.2 Protocol : 6.36 %**
      * Most of the information in these packets is of the form:
         * *Server Hello, Certificate, Server Key Exchange, Server Hello Done*
         * *Change Cipher Spec, Hello Request, Hello Request*
         * *Application Data*
      * TLS is used to secure communications by providing privacy, authentication and data integrity.
         
    * **RTCP Protocol : 2.10 %**
      * Most of the information in these packets is of the form:
         * *Application specific   ( x\007 ) subtype=8[Malformed Packet]*
         * *Payload-specific Feedback   Unknown  [Malformed Packet]*
         * *Sender Report   (PSE:Unknown  PSE:Unknown  PSE:MS - TURN Server Bandwidth  PSE:Unknown  [Malformed Packet]*
         * *Receiver Report   (PSE:Unknown  [Malformed Packet]*
         * *Goodbye*
      * RTCP provides feedback on the Quality of Service, e.g. packet counts, packet loss, etc. RTCP doesn't transport any media data.
 
    * **UDP Protocol : 89.88 %**
      * Most of the information in these packets is of the form:
         * *63380  >  20601 Len=1432*
      * UDP has no connection setup, doesn't recover errors, nor does it guarantee message delivery. 

* Therefore, for transmitting data, UDP is the preferred protocol for the HoloLens. This isn't surprising considering UDP's fast nature and being less of a strain on the network. UDP is also favored in IoT applications.
