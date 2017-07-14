* If AR devices are to be abundant in the future, fog computing will help alleviate the costs to running them.
* In this report, we'll aim to quantify the trade-off between data transfer & computational workload of different configurations.

## Configuration 1: Laptop-as-a-server and HoloLens-as-a-display
* We'll start with the simplified case of one laptop and one HoloLens as illustrated below:
![AR without Fog](https://github.com/dchege711/Augmented_Reality/blob/master/Images/AR%20Without%20Fog.png)
* For starters, we'll run the [Origami App](https://github.com/dchege711/Augmented_Reality/tree/master/Unity_Tutorials/Origami) with the code being hosted on the laptop and the HoloLens being used as a screen.
* We used SystemCounter.py to measure the resources\* (see [Origami_Data&Packets_200](https://github.com/dchege711/Augmented_Reality/blob/master/Quantitative_Research/Origami_Data&Packets_200.txt)) used by the Origami app. 

![Origami_DataVsTime](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Origami_DataVsTime.png)
![Origami_PacketsVsTime](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Origami_PacketsVsTime.png)
* For the 200 seconds, 93.21 MBs & 116,504 packets were received from the HoloLens, while 39.75 MBs &	99,586 packets were sent to the HoloLens.
* The peaks at around 50s and 110s show when I made hand gestures. 
* Data transfer varies between different AR apps as illustrated below:

![Compare_Data_Rates](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Static_Cube_vs_Origami.png)

* **Note: *Currently, I haven't been able to discriminate between traffic sent by Unity to the HoloLens and back from traffic sent by the laptop in general. For now, I'm keeping other activities to a minimum and making repeated measurements. As you can see, the data tapers when the HoloLens-Laptop connection is off. Can anyone suggest how to measure process-specific data usage? Thanks in advance!***
