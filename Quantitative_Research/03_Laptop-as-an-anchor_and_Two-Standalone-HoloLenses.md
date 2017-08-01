# 03 Laptop as an Anchor and Two Stand-Alone HoloLenses

* Here's an illustration showing the setup for this report.

![Laptop-As-Anchor](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Laptop_as_Anchor.png)

* We worked with the following (C#) data types:
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
* In this experiment, we send the minimal-data required. For instance, HoloLens #1 will broadcast a Vector3 as 3 floats under the assumption that HoloLens #2 knows how to implement the Vector3 data type.


* We aim to answer questions like:
    * Are resources straightforwardly predictable? *e.g. Does sending twice as many Vector3's cost twice as much bandwidth?*
    * How 'full' are the packets? Could we save bandwidth by aggregating before sending? *e.g. Does sending thrice as many ints as Vector3's use the same bandwidth?*

* Questions to keep in mind for later:
    * What are the limitations?
    * Can we transfer more complex structures, like 3D objects, instead of mandating that every HoloLens have its copy of the object?

* The data being broadcasted was varied across different runs of the experiment:
    * 10 Vector3's every second, each Vector3 being sent separately.
    * 30 ints every second, each int being sent separately.
    * 20 Vector3's every second, each Vector3 being sent separately.

* Unity uses the UDP protocol to send messages, so we also filtered based on that.
