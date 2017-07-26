## Objectives
* We want to get a quantitative report of various parameters in different HoloLens use cases.
* The parameters of interest are:
    * Amount of Data Sent by the HoloLens(es)
    * Amount of Data Received by the HoloLens(es)
    * Extent of computational resources used up by HoloLens(es)
        * The CPU Load, Memory Usage, Engines Utilization
    * The type of data being sent by the HoloLens(es)\*
* We'll be comparing the parameters in 2 main configurations:
    * An app running on the laptop, with the HoloLens being used as a display.
    * A fully-fledged app that has been deployed to the HoloLens
* The experiments will feature differing types of data in order to simulate varying levels of computational workloads.

## Additional Considerations
#### Estimating Bandwidth
* It's worth noting that the bandwidth requirements shouldn't be mistaken for the complexity of the objects in the AR environment.
* For instance, a plain sphere and a humanoid avatar will consume the same bandwidth if all that we're tracking is the position of their centroid.
* In our experiments, each HoloLens already has a copy of the object, i.e. if we're playing tennis, each HoloLens has internal copies of the rackets. The actual gameobjects are not broadcasted in our experiments.
* What ultimately counts are the data types that are being broadcasted onto the shared network.
* The frequency of sending data can also be misunderstood. Suppose we're shooting a projectile. Since the projectile's path is deterministic, we only need to broadcast where our projectile is, and its direction of motion. There's no need for a stream of updates.
