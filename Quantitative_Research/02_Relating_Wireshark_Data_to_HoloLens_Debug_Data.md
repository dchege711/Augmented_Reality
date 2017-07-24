## 02. Relating Wireshark's data to HoloLens Debug data
* [Report 01](https://github.com/dchege711/Augmented_Reality/blob/master/Quantitative_Research/01_Laptop-as-a-server_and_HoloLens-as-a-display.md) measured data transfer over Wi-Fi using the psutil module. However, as noted at the end, we found a better way to filter Wi-Fi data.
* Wireshark allows gives us a data dump from which we can filter results based on IPv4 addresses. Furthermore, by using the Windows Device Portal, https://<HOLOLENS_IP_ADDRESS>/etwmon.htm, we were able to take additional readings.
* I'm pretty sure about Wireshark's readings, but I'm not sure whether the Microsoft-Windows-Kernel-Network is the right provider for network data for the HoloLens.
* If there's a significant correspondence between the two data sets, then I will have more confidence that the Microsoft-Windows-Kernel-Network is the right source for HoloLens Wi-Fi data.
* The overlaps shown below suggest the Microsoft-Windows-Kernel-Network is the right tool for the job.

![HoloLens_to_Laptop_Comparison](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Wireshark_vs_WDP_HL_to_LP.png)

![Laptop_to_HoloLens_Comparison](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Wireshark_vs_WDP_LP_to_HL.png)

* However, the Microsoft-Windows-Kernel-Network truncates data to 50,000 entries, so I can't take prolonged measurements over the Microsoft-Windows-Kernel-Network.
* Therefore, whenever I can collect data from either source, Wireshark will be my first pick.
* Just like [Report 01](https://github.com/dchege711/Augmented_Reality/blob/master/Quantitative_Research/01_Laptop-as-a-server_and_HoloLens-as-a-display.md) had demonstrated, the Origami app sends more data to the laptop than it receives.

![Data_Transfer_Origami](https://github.com/dchege711/Augmented_Reality/blob/master/Images/Wireshark_Origami.png)

#### Sources
* [Data processing script](https://github.com/dchege711/Augmented_Reality/blob/master/Quantitative_Research/Scripts/ProcessDataDumps.py)
* [The Wireshark data](https://github.com/dchege711/Augmented_Reality/tree/master/Quantitative_Research/Data_Dumps/Origami_Wireshark.csv)
* [Microsoft-Windows-Kernel-Network data](https://github.com/dchege711/Augmented_Reality/tree/master/Quantitative_Research/Data_Dumps/Origami_Windows_Device_Portal.csv)
