## Notes on [Origami (Holograms 101)](https://developer.microsoft.com/en-us/windows/mixed-reality/holograms_101)

* I followed the tutorial linked above, but "'ve added lots of comments in the C# scripts.
* These notes are useful for a person who knows Python/Java/JS, but new to C#.
* The one (and only) scene in this project is the Origami Scene. Note the organization in the hierarchy.
* To take any pictures of the holograms, use "Hey Cortana, take a picture."
* ![My Image](https://github.com/dchege711/Augmented_Reality/blob/master/Unity_Tutorials/Screenshots/OrigamiScreenShot.PNG)

### Chapter 1 - 'Holo' World
* The Main Camera for HoloApps has a pattern to it:
	* Transform Position = (0, 0, 0); Clear Flags = Solid color; Background RGBA = (0, 0, 0, 0) since black == transparent for HoloLens
* The scene:
	* There was a lot of handwaving in this part of the tutorial, since I merely dragged and dropped already-made GameObjects
	* There's much to learn about how to scale/position the holograms, change the lighting, etc.

### Chapter 2 - Gaze
* This section visualizes my gaze (where I'm currently looking) using a world-locked cursor.
* There's a cursor object at the root level of the Origami Scene. The configurations are as follows:
* ![Cursor Settings](https://github.com/dchege711/Augmented_Reality/blob/master/Unity_Tutorials/Screenshots/CursorSettings.PNG)
* [WorldCursor.cs](Origami/Assets/Scripts/WorldCursor.cs) is used to control the cursor. 
		 
### Chapter 3 - Gestures
* This section makes a selected sphere fall by turning on gravity. Yes, you can switch off gravity in Unity :grin:
* [GazeGestureManager.cs](Origami/Assets/Scripts/GazeGestureManager.cs) can detect gestures, and is attached to the OrigamiCollection object.
* [SphereCommands.cs](Origami/Assets/Scripts/SphereCommands.cs) can listen to GazeGestureManager.cs so as to turn on gravity.
* SphereCommands.cs has been attached to the Sphere1 and Sphere2 objects.

### Chapter 4 - Voice Input
* This section adds support for 2 voice commands: "Reset World" and "Drop Sphere".
* [SpeechManager.cs](Origami/Assets/Scripts/SpeechManager.cs) sets up a KeywordRecognizer for the 2 phrases. It's attached to the OrigamiCollection object.
* I also updated SphereCommands.cs to be able to support calls from SpeechManager.cs

### Chapter 5 - Spatial Sound
* This section adds ambient music and sound effects. It utilizes spatial sound for pseudo-location.
* The ambient music sound was set using the Unity GUI since the music doesn't change much.
* ![OrigamiCollection_Sound](https://github.com/dchege711/Augmented_Reality/blob/master/Unity_Tutorials/Screenshots/OrigamiCollectionSound1.PNG)
* However, for the Sphere1 and Sphere2, sound was addded in [SphereSounds.cs](Origami/Assets/Scripts/SphereSounds.cs) and then attached.

### Chapter 6 - Spatial Mapping
* To introduce a wireframe mesh into the real world, I dragged the Spatial Mapping asset to the root of the hierarchy.
* ![WireMesh](https://github.com/dchege711/Augmented_Reality/blob/master/Unity_Tutorials/Screenshots/WireMesh.jpg)
* To add select and place capabilities, [TapToPlaceParent.cs](Origami/Assets/Scripts/TapToPlaceParent.cs) was attached to the Stage object.

### Chapter 7 - Holographic Fun
* Not much code happened here. I added Underworld as a child to Origami Collection.
* I also attached [HitTarget.cs](Origami/Assets/Scripts/HitTarget.cs) to the Target object, allowing the stage to be replaced by the underworld upon sphere-blue_fan impact.
