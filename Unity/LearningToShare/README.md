## Notes Taken when Implementing LearningtoShare
* This Unity project follows the [Holograms 240](https://developer.microsoft.com/en-us/windows/mixed-reality/holograms_240) tutorial.
* I've already done the entire tutorial (see [Shared Holograms](https://github.com/dchege711/Augmented_Reality/tree/master/Unity/SharedHolograms)), but this time I want to focus more on how the sharing of data between 2 HoloLens is facilitated. I'll only do some of the steps in Microsoft's tutorial.
* The end-goal is to gain enough understanding to set up a shared holographic experience using an edge-node and edge-device structure.

#### Note:
* *At the beginning, there's an error about importing NuGet packages. Ignore it, unless you try exporting the project from Unity to Visual Studio and it fails. For reference, I am using Unity 5.6.2f and Visual Studio 2017 Community.*

### Chapter 1 - Holo World
* This sets up Unity with a holographic app and deploys the app to a HoloLens.
* The default Main Camera at the root of the hierarchy is replaced by one from the HoloToolkit that's adapted for holograms.
* The HologramCollection is set at (X = 0, Y = -0.25, Z = 2). The holograms, e.g. the EnergyHub, are children of the HologramCollection.
    * X controls lateral displacement, e.g. 2 means 2m to my right.
    * Y controls height, e.g. 2 means 2m above the HoloLens' position, etc.
    * Z controls distance from me, e.g. -2 means 2m behind me
* The EnergyHub asset came with the downloaded folder 'Assets' and is of the form EnergyHub.prefab (1.04 MB) and EnergyHub.prefab.meta (179 bytes). In the GUI, I dragged it and made it a child of the HologramCollection gameobject. **How do I do this using code?**
* I completed this step by deploying a standalone app to Visual Studio.

### Chapter 2 - Interaction
