## [An Introduction for the Uninitiated](https://www.openfogconsortium.org/wp-content/uploads/OpenFog-Reference-Architecture-Executive-Summary.pdf)
* Here's a visual aid from a [IoT for All](https://iot-for-all.com/openfog-consortium-reference-architecture-executive-summary/):
* ![Image from IoT Labs](https://cdn-images-1.medium.com/max/800/0*NtEQXRdirRTpWcOE.png)
* Core idea: We don't need to push all the data to the cloud. By using local inexpensive fog nodes, we can save on latency (some data loses value fast, e.g. an oil leak a minute ago could be a major oil spill right now) and broadband costs.
* The autonomous car [example](https://medium.com/iotforall/cloud-computing-vs-fog-computing-aa94cbc4b827): It's fine for your autonomous car to access Netflix & send logs, but to avoid a near-collision on the highway, the latency demand is best handled at the Edge.
* The players in the game: [Azure IoT (now teamed up with Cisco Fog)](https://azure.microsoft.com/en-us/suites/iot-suite/) , [AWS Greengrass](https://aws.amazon.com/greengrass/) and [Android Things](https://developer.android.com/things/hardware/index.html).
* The SCALE architecture offered by OpenFog architectures: Security (safe, trusted transactions), Cognition (awareness of objectives to enable autonomy), Agility (rapid innovation and affordable scaling), Latency (real-time processing) & Efficiency (pulling together local unused resources from participating end-user devices).
* The complete OpenFog Reference Architecture for Fog Computing document can be found [here](https://www.openfogconsortium.org/wp-content/uploads/OpenFog_Reference_Architecture_2_09_17-FINAL-1.pdf)


## Uses of IoT
* Maybe some [quick reasons](https://iot-for-all.com/internet-of-things-examples-applications/) why we're so into IoT:
    * Predictive maintenance saves manufacturing costs since machines will only be serviced when need be.
    * Smart thermostats and lights can cut energy costs, e.g. [Google's data centers cut energy use by 15%](https://www.theguardian.com/environment/2016/jul/20/google-ai-cut-data-centre-energy-use-15-per-cent)
    * Smart irrigation systems can sense soil moisture and listen to weather updates, thereby only irrigating when necessary.
    * RFID tags in inventories can save search time, and facilitate seamless additions when necessary.
    * Sensors can warn us in advance about earthquakes, tsunamis, drought, etc.
    * Surveillance tools can boost security, but RIP our privacy(?)
    * Agencies can use sensors to fight radiation, pollution and identify pathogens.
