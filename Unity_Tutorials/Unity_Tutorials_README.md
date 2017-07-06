# Unity Tutorials README
* To set up the development environment, follow [these instructions](https://developer.microsoft.com/en-us/windows/mixed-reality/install_the_tools).

----

## [Roll a Ball](https://unity3d.com/learn/tutorials/projects/roll-ball-tutorial/introduction-roll-ball?playlist=17141)
* I followed the tutorial linked in the title.
* Most of the development was done inside Unity, but in the Scripts folder, you can find some C# code.

----

## Notes on [Holograms 101](https://developer.microsoft.com/en-us/windows/mixed-reality/holograms_101)

### Chapter 1 - 'Holo' World
* The Main Camera for HoloApps has a pattern to it:
	* Transform Position = (0, 0, 0); Clear Flags = Solid color; Background RGBA = (0, 0, 0, 0) since black == transparent for HoloLens
* The scene:
	* There was a lot of handwaving in this part of the tutorial, since I merely dragged and dropped already-made GameObjects
	* There's much to learn about how to scale/position the holograms, change the lighting, etc.
* I'm getting compilation errors when trying to export to Visual Studio, so I'll use the HoloLens directly from Unity.