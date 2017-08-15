# 03 Laptop as an Anchor and Two Stand-Alone HoloLenses

* Here's an illustration showing the setup for this report.

![Laptop-As-Anchor](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Laptop_as_Anchor.png)

* Unity apps written in C# have the following data types at their disposal:
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

## Protocols Used by the HoloLens
* Tristan Braud's 2017 paper, ['Future Networking Challenges: The Case of Mobile AR'](https://github.com/dchege711/Augmented_Reality/blob/master/Related_Work/2017_Tristan_Braud_Future_Networking_Challenges.md) proposes a need for a protocol designed for AR, lest AR applications prove unsustainable under the current (and projected) infrastructure.
* We thus wanted to know what protocol is used by the HoloLens, and this is what we found:

![Protocol_Distribution](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Chege_to_HL_by_Protocol.png)

* The above data was collected for a HoloLens that was sending 12,000 integers per second to the network.
* Of the 131.45 MB transferred, following distribution was observed:
    * TCP Protocol: 1.66 %
    * TLSv1.2 Protocol : 6.36 %
    * RTCP Protocol : 2.10 %
    * UDP Protocol : 89.88 %
