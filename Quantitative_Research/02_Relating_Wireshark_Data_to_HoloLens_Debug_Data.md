## 02. Relating Wireshark's data to HoloLens Debug data
* [Report 01](https://github.com/dchege711/Augmented_Reality/blob/master/Quantitative_Research/01_Laptop-as-a-server_and_HoloLens-as-a-display.md) measured data transfer over Wi-Fi using the psutil module. However, as noted at the end, we found a better way to filter Wi-Fi data.
* Wireshark allows gives us a data dump from which we can filter results based on IPv4 addresses. Furthermore, by using the Windows Device Portal, https://<HOLOLENS_IP_ADDRESS>/etwmon.htm, we were able to take additional readings.
* I'm pretty sure about Wireshark's readings, but I'm not sure whether the Microsoft-Windows-Kernel-Network is the right provider for network data for the HoloLens.
* If there's a significant correspondence between the two data sets, then I will have more confidence that the Microsoft-Windows-Kernel-Network is the right source for HoloLens Wi-Fi data.
