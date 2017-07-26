# Notes Taken when Implementing LearningtoShare
* This Unity project follows the [Holograms 240](https://developer.microsoft.com/en-us/windows/mixed-reality/holograms_240) tutorial.
* I've already done the entire tutorial (see [Shared Holograms](https://github.com/dchege711/Augmented_Reality/tree/master/Unity/SharedHolograms)), but this time I want to focus more on how the sharing of data between 2 HoloLens is facilitated. I'll only do some of the steps in Microsoft's tutorial.
* The end-goal is to gain enough understanding to set up a shared holographic experience using an edge-node and edge-device structure.

#### Note: 
* *At the beginning, there's an error about importing NuGet packages. Ignore it, unless you try exporting the project from Unity to Visual Studio and it fails. For reference, I am using Unity 5.6.2f and Visual Studio 2017 Community.*

## Chapter 1 - Holo World
* *This sets up Unity with a holographic app and deploys the app to a HoloLens.*
* The default Main Camera at the root of the hierarchy is replaced by one from the HoloToolkit that's adapted for holograms.
* The HologramCollection is set at (X = 0, Y = -0.25, Z = 2). The holograms, e.g. the EnergyHub, are children of the HologramCollection.
    * X controls lateral displacement, e.g. 2 means 2m to my right.
    * Y controls height, e.g. 2 means 2m above the HoloLens' position, etc.
    * Z controls distance from me, e.g. -2 means 2m behind me
* The EnergyHub asset came with the downloaded folder 'Assets' and is of the form EnergyHub.prefab (1.04 MB) and EnergyHub.prefab.meta (179 bytes). In the GUI, I dragged it and made it a child of the HologramCollection gameobject. **How do I do this using code?**

## Chapter 2 - Interaction
* *This adds a cursor to visualize Gaze, and interprets the tap gesture to allow placement of the holograms.*
#### Managing Gaze Input
* Step 1: Add GazeManager.cs to the HologramCollection gameobject.
    * GazeManager.cs is a script that ships with the HoloToolkit.
    * *GazeManager.cs determines the location of the user's gaze, hit position and normals.*
    * It has 2 public variables: Max Gaze Distance (15.0 by default), and Raycast Layer Mask (Physics.DefaultRaycastLayers by default).
    * Unless changed, these variables have default values.
* Step 2: Add the Cursor asset to the root (hierarchy)
    * Again, this asset shipped with the HoloToolkit.
    * It has a script (CursorManager.cs) that also shipped with the HoloToolkit.
    * *CursorManager.cs takes Cursor gameobjects, one that is on holograms and another off holograms. It shows the appropriate Cursor when a hologram is hit, places the appropriate Cursor at the hit position, and matches the Cursor normal to the hit surface*
    * It has 3 public variables: Cursor On Hologram, Cursor Off Hologram and Distance from Collision. The first 2 are GameObjects that need filling, while the 3rd one is a float that is .01 by default.
#### Managing Gesture
* Step 1: Add GestureManager.cs to the HologramCollection object.
    * GestureManager.cs came with the HoloToolkit. It has no public variables.
    * *GestureManager creates a gesture recognizer which detects tap gestures. When a tap is detected, GestureManager uses GazeManager to find the GameObject. It then sends a message to that GameObject*
* Step 2: Add HologramPlacement.cs to the EnergyHub object.
    * While it takes no variables, this script was specific to the current project.
    * *HologramPlacement tracks if we have been sent a transform for the model. The model is rendered relative to the actual anchor*

## Chapter 3 - Shared Coordinates
* *This sets up a network for a shared experience, establishes a common reference point, shares coordinate systems across devices such that everyone sees the same hologram*
* Note that InternetClientServer and PrivateNetworkClientServer must be declared in Edit > Project Settings > Player > Windows Store > Publishing Settings > Capabilities
* I added the Sharing.prefab to the root (hierarchy).The Sharing prefab came with the ToolKit. It comes with a couple of scripts attached:
    * SharingStage.cs is part of the Toolkit. It comes with a couple of configurable variables:
        * Client Role. Primary can create/join/leave sessions on the Session server. Secondary can't. Set to ClientRole.Primary by default
        * Server Address, which is 'localhost' by default
        * Server Port, which is 20602 by default.
        * IsAudioEndpoint, which sets whether this app should provide audio. True by default.
        * AutoDiscoverServer has no default value.
        * PingIntervalSec determines how often the discovery service should ping the network searching for a server. Set to 2 by default.
    * SharingSessionTracker.cs is also part of the Toolkit. It keeps track of users joining and leaving the session.
    * AutoJoinSession.cs ships with the Toolkit. It has one public variable, SessionName, which is "Default" by default.
    * CustomMessages.cs is a script defined for this project. It imports the HoloToolkit Sharing and Unity namespaces. It's used for sending messages to and receiving messages from the server.
* To launch the sharing service, I ran the executable SharingService.exe that ships with the Toolkit. This gives me an IPv4 address. This step needs to be done on only one of the PCs in the shared experience.
* On the rest of the PCs running Unity, I put this IPv4 address in place of 'localhost' in the variables of SharingStage.cs
* I then added ImportExportAnchorManager.cs to the HologramCollection. This script is custom for this project. It manages creating anchors and sharing the anchors with other clients.
* I also modified HologramPlacement.cs to share the coordinates of the anchor with the rest of the devices on the network. See the code for modifications annotated with 'Step 3'
* I also added AppStateManager.cs, a custom script, to the HologramCollection object. It keeps track of the current state of the experience. It starts at 'WaitingForAnchor', then 'WaitingForStageTransform', and finally 'Ready'.
