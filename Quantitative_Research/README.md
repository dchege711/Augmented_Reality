* If AR devices are to be abundant in the future, fog computing will help alleviate the costs to running them.
* In this report, we'll aim to quantify the trade-off between data transfer & computational workload of different configurations.

## Configuration 1: Laptop-as-a-server and HoloLens-as-a-display
* We'll start with the simplified case of one laptop and one HoloLens as illustrated below:
![AR without Fog](https://github.com/dchege711/Augmented_Reality/blob/master/Images/AR%20Without%20Fog.png)
* For starters, we'll run the [Origami App](https://github.com/dchege711/Augmented_Reality/tree/master/Unity_Tutorials/Origami) with the code being hosted on the laptop and the HoloLens being used as a screen.
* We used SystemCounter.py to measure the resources* used by our AR app. Sent 21.44 MB, received 1.66 MB in a 60 second period.

* Note: *Currently, I haven't been able to discriminate between traffic sent by Unity to the HoloLens and back from traffic sent by the laptop in general. For now, I'm keeping other activities to a minimum and making repeated measurements.*
