## Takeaways from Tristan Braud et al., 2017. Future Networking Challenges: The Case of Mobile Augmented Reality
* The HoloLens has a lot of computing power, but mobile devices don't. Hence, for mobile augmented reality (MAR), the optimization problem (computing power vs. latency vs. bandwidth) is more pronounced.
* Typical constraints for MAR: at least 10Mb/s, at most 75ms roundtrip.
* In-app optimizations include pre-processing, compression techniques, pre-fetching & caching from remote databases.
* Uplink is usually lower than downlink, but MAR seeks a balance since the uplink (e.g. video feed) is usually more than the downlink (e.g. computation results).
* 5G is poised for post-2022, but AR is poised for pre-2020. AR content grows faster than infrastructure developments. Furthermore, users may be reluctant to transmit lots of data.
* Authors propose an AR-oriented transport protocol that:
    * Classifies data
    * Controls congestion & degrades gracefully
    * Error-tolerant because of latency constraints
    * Uses multiple paths (e.g. 4G and Wi-Fi)
    * Distributes to n servers and n-way synchronizes
    * Incorporates edge data-centers to handle MAR offloading requests
    * Is secure, because the data is sensitive, e.g. faces.

### To-do items:
* Get bandwidth & latency for university Wi-Fi applications.
* Plot connection protocols used
