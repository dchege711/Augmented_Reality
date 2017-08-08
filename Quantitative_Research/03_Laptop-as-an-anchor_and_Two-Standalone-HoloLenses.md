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
* In our experiments, we used ints and vector3's, under the assumption that our findings can be generalized to the other data types.
* The HoloToolkit Sharing utility was rather finicky with the university WiFi. The connection time between the HoloLenses wasn't very predictable. Sometimes one HoloLens would be kept waiting longer than the other.
* Due to time constraints, we considered the connected HoloLens as representative of what the other one would have sent.
* For example, 4kVectors shows a case in which both HoloLenses connected successfully with each other over the Sharing utility.
```shell
4kVectors_data    Chege    Sent :  44.73 MB (259 sec)   Received :  11.97 MB (274 sec)
4kVectors_data    Maria    Sent :  51.34 MB (246 sec)   Received :  13.14 MB (261 sec)
8kVectors_data    Chege    Sent : 110.36 MB (334 sec)   Received :   0.29 MB (334 sec)
8kVectors_data    Maria    Sent :  27.11 MB (120 sec)   Received :   0.06 MB (120 sec)
```


* We aim to answer questions like:
    * Are resources straightforwardly predictable? *e.g. Does sending twice as many Vector3's cost twice as much data?*
    * How 'full' are the packets? Could we save data by aggregating before sending? *e.g. Does sending thrice as many ints as Vector3's use the same data?*

* Questions to keep in mind for later:
    * What are the limitations?
    * Can we transfer more complex structures, like 3D objects, instead of mandating that every HoloLens have its copy of the object?

* The data being broadcasted was varied across different runs of the experiment:
    * 10 Vector3's every second, each Vector3 being sent separately.
    * 30 ints every second, each int being sent separately.
    * 20 Vector3's every second, each Vector3 being sent separately.

* Unity uses the UDP protocol to send messages, so we also filtered based on that.
