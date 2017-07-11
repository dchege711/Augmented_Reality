# [Shared Holograms](https://developer.microsoft.com/en-us/windows/mixed-reality/holograms_240)

* Sets up a holographic experience that can be shared across many HoloLens devices.

## Issues
* Loading the Unity Project after downloading raises this exception:
```
System.Exception: Package directory not found: "C:\Users\dchege711\.nuget\packages\Microsoft.CSharp\4.0.1".
  at UnityEditor.Scripting.Compilers.NuGetPackageResolver.Resolve () <0x2b8a370 + 0x0032b> in <filename unknown>:0 
  at AssemblyUpdater.Core.AssemblyUpdaterContext.AddFrameworkFolderToSearchPath (Mono.Cecil.AssemblyDefinition assemblyDefinition, Mono.Cecil.DefaultAssemblyResolver resolver, IAPIUpdaterListener listener) <0x2b82778 + 0x00263> in <filename unknown>:0 
  at AssemblyUpdater.Core.AssemblyUpdaterContext.ReadAssembly (System.String assemblyPath, IAPIUpdaterListener listener, FileAccess mode, System.String[] searchPaths) <0x2b801e8 + 0x00163> in <filename unknown>:0 
  at AssemblyUpdater.Core.AssemblyUpdaterContext.From (System.String assemblyPath, IConfigurationProvider configuration, System.String[] assemblySearchPaths, UpdaterMode mode, IAPIUpdaterListener listener) <0x2b80100 + 0x00073> in <filename unknown>:0 
  at AssemblyUpdater.Core.AssemblyUpdaterContext.From (System.String assemblyPath, System.String[] assemblySearchPaths, UpdaterMode mode, IAPIUpdaterListener listener) <0x2b800c0 + 0x0002f> in <filename unknown>:0 
  at AssemblyUpdater.Application.Program.CheckForObsoleteAPIUsage (AssemblyUpdater.Application.CommandLineSpec config) <0x2b61890 + 0x00043> in <filename unknown>:0 
  at AssemblyUpdater.Application.Program.Main (System.String[] args) <0x2b00f18 + 0x000fb> in <filename unknown>:0 
UnityEditor.Scripting.APIUpdaterHelper:DoesAssemblyRequireUpgrade(String)
```
* Deploying to Visual Studio allows me to deploy to the HoloLens as a standalone app.
* However, when I try to deploy from Unity to a Visual Studio .sln file, I get these 2 errors:
```
UnityException: Failed to run reference rewriter with command --target="Temp\StagingArea\AudioIO2.dll" --additionalreferences="Temp\StagingArea","Temp\StagingArea\Plugins\ARM","Temp\StagingArea\Plugins\X64","Temp\StagingArea\Plugins\X86","Temp\StagingArea\Plugins\X64","Temp\StagingArea\Plugins\X86","Temp\StagingArea\Plugins\ARM","C:\Program Files (x86)\Windows Kits\10\UnionMetadata\Facade" --platform="C:\Program Files (x86)\Windows Kits\10\UnionMetadata\Facade\Windows.winmd" --support="Temp\StagingArea\WinRTLegacy.dll" --supportpartialns=Unity.Partial --system=System --dbg=pdb --lock=UWP\project.lock.json --alt=System.Xml.Serialization;System.Collections,System.Collections.NonGeneric;System.Reflection,System.Reflection.TypeExtensions;System.IO,System.IO.FileSystem;System.Net,System.Net.Primitives;System.Net.Sockets,System.Net.Primitives;System.Xml,System.Xml.XmlDocument;<winmd>,Windows.winmd --ignore=System.IConvertible,mscorlib.
Error: type `Windows.ApplicationModel.Core.CoreApplication` doesn't exist in target framework. It is referenced from AudioIO2.dll at System.Void AudioIO_DLL.IO.MicrophoneInternal/<Start>d__12::MoveNext().
Error: type `Windows.ApplicationModel.Core.CoreApplicationView` doesn't exist in target framework. It is referenced from AudioIO2.dll at System.Void AudioIO_DLL.IO.MicrophoneInternal/<Start>d__12::MoveNext().
Catastrophic failure while running rrw: Mono.Cecil.AssemblyResolutionException: Failed to resolve assembly: 'Windows.Foundation.UniversalApiContract, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null'
   at Unity.SearchPathAssemblyResolver.Resolve(AssemblyNameReference name, ReaderParameters parameters)
   at Unity.NuGetAssemblyResolver.Resolve(AssemblyNameReference name, ReaderParameters parameters)
   at Unity.SearchPathAssemblyResolver.Resolve(AssemblyNameReference name)
   at Mono.Cecil.MetadataResolver.Resolve(TypeReference type) in g:\git\Unity-Technologies\cecil\Mono.Cecil\MetadataResolver.cs:line 106
   at Mono.Cecil.MetadataResolver.Resolve(MethodReference method) in g:\git\Unity-Technologies\cecil\Mono.Cecil\MetadataResolver.cs:line 216
   at Mono.Cecil.MethodReference.Resolve() in g:\git\Unity-Technologies\cecil\Mono.Cecil\MethodReference.cs:line 170
   at Unity.ReferenceRewriter.RewriteTypeReferences.Visit(MethodReference method, String referencingEntityName)
   at Unity.ReferenceRewriter.ReferenceDispatcher.Visit(MethodReference method, String referencingEntityName)
   at Unity.ReferenceRewriter.ReferenceDispatcher.DispatchMethodBody(MethodBody body)
   at Unity.ReferenceRewriter.ReferenceDispatcher.DispatchMethod(MethodDefinition method)
   at Unity.ReferenceRewriter.ReferenceDispatcher.DispatchMethods(TypeDefinition type)
   at Unity.ReferenceRewriter.ReferenceDispatcher.Dispatch()
   at Unity.ReferenceRewriter.RewriteTypeReferences.Run()
   at Unity.ReferenceRewriter.RewriteOperation.Execute(RewriteContext context)
   at Unity.ReferenceRewriter.Program.Main(String[] args)

PostProcessWinRT.RunReferenceRewriter () (at C:/buildslave/unity/build/PlatformDependent/WinRT/SharedSources/CSharp/PostProcessWinRT.cs:545)
PostProcessWinRT.Process () (at C:/buildslave/unity/build/PlatformDependent/WinRT/SharedSources/CSharp/PostProcessWinRT.cs:127)
UnityEditor.WSA.BuildPostprocessor.PostProcess (BuildPostProcessArgs args) (at C:/buildslave/unity/build/PlatformDependent/MetroPlayer/Extensions/Managed/ExtensionModule.cs:155)
UnityEditor.PostprocessBuildPlayer.Postprocess (BuildTarget target, System.String installPath, System.String companyName, System.String productName, Int32 width, Int32 height, System.String downloadWebplayerUrl, System.String manualDownloadWebplayerUrl, BuildOptions options, UnityEditor.RuntimeClassRegistry usedClassRegistry, UnityEditor.BuildReporting.BuildReport report) (at C:/buildslave/unity/build/Editor/Mono/BuildPipeline/PostprocessBuildPlayer.cs:186)
UnityEditor.HostView:OnGUI()
```
* and...
```
UnityException: Failed to run reference rewriter with command --target="Temp\StagingArea\AudioIO2.dll" --additionalreferences="Temp\StagingArea","Temp\StagingArea\Plugins\ARM","Temp\StagingArea\Plugins\X64","Temp\StagingArea\Plugins\X86","Temp\StagingArea\Plugins\X64","Temp\StagingArea\Plugins\X86","Temp\StagingArea\Plugins\ARM","C:\Program Files (x86)\Windows Kits\10\UnionMetadata\Facade" --platform="C:\Program Files (x86)\Windows Kits\10\UnionMetadata\Facade\Windows.winmd" --support="Temp\StagingArea\WinRTLegacy.dll" --supportpartialns=Unity.Partial --system=System --dbg=pdb --lock=UWP\project.lock.json --alt=System.Xml.Serialization;System.Collections,System.Collections.NonGeneric;System.Reflection,System.Reflection.TypeExtensions;System.IO,System.IO.FileSystem;System.Net,System.Net.Primitives;System.Net.Sockets,System.Net.Primitives;System.Xml,System.Xml.XmlDocument;<winmd>,Windows.winmd --ignore=System.IConvertible,mscorlib.
Error: type `Windows.ApplicationModel.Core.CoreApplication` doesn't exist in target framework. It is referenced from AudioIO2.dll at System.Void AudioIO_DLL.IO.MicrophoneInternal/<Start>d__12::MoveNext().
Error: type `Windows.ApplicationModel.Core.CoreApplicationView` doesn't exist in target framework. It is referenced from AudioIO2.dll at System.Void AudioIO_DLL.IO.MicrophoneInternal/<Start>d__12::MoveNext().
Catastrophic failure while running rrw: Mono.Cecil.AssemblyResolutionException: Failed to resolve assembly: 'Windows.Foundation.UniversalApiContract, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null'
   at Unity.SearchPathAssemblyResolver.Resolve(AssemblyNameReference name, ReaderParameters parameters)
   at Unity.NuGetAssemblyResolver.Resolve(AssemblyNameReference name, ReaderParameters parameters)
   at Unity.SearchPathAssemblyResolver.Resolve(AssemblyNameReference name)
   at Mono.Cecil.MetadataResolver.Resolve(TypeReference type) in g:\git\Unity-Technologies\cecil\Mono.Cecil\MetadataResolver.cs:line 106
   at Mono.Cecil.MetadataResolver.Resolve(MethodReference method) in g:\git\Unity-Technologies\cecil\Mono.Cecil\MetadataResolver.cs:line 216
   at Mono.Cecil.MethodReference.Resolve() in g:\git\Unity-Technologies\cecil\Mono.Cecil\MethodReference.cs:line 170
   at Unity.ReferenceRewriter.RewriteTypeReferences.Visit(MethodReference method, String referencingEntityName)
   at Unity.ReferenceRewriter.ReferenceDispatcher.Visit(MethodReference method, String referencingEntityName)
   at Unity.ReferenceRewriter.ReferenceDispatcher.DispatchMethodBody(MethodBody body)
   at Unity.ReferenceRewriter.ReferenceDispatcher.DispatchMethod(MethodDefinition method)
   at Unity.ReferenceRewriter.ReferenceDispatcher.DispatchMethods(TypeDefinition type)
   at Unity.ReferenceRewriter.ReferenceDispatcher.Dispatch()
   at Unity.ReferenceRewriter.RewriteTypeReferences.Run()
   at Unity.ReferenceRewriter.RewriteOperation.Execute(RewriteContext context)
   at Unity.ReferenceRewriter.Program.Main(String[] args)

PostProcessWinRT.RunReferenceRewriter () (at C:/buildslave/unity/build/PlatformDependent/WinRT/SharedSources/CSharp/PostProcessWinRT.cs:545)
PostProcessWinRT.Process () (at C:/buildslave/unity/build/PlatformDependent/WinRT/SharedSources/CSharp/PostProcessWinRT.cs:127)
UnityEditor.WSA.BuildPostprocessor.PostProcess (BuildPostProcessArgs args) (at C:/buildslave/unity/build/PlatformDependent/MetroPlayer/Extensions/Managed/ExtensionModule.cs:155)
UnityEditor.PostprocessBuildPlayer.Postprocess (BuildTarget target, System.String installPath, System.String companyName, System.String productName, Int32 width, Int32 height, System.String downloadWebplayerUrl, System.String manualDownloadWebplayerUrl, BuildOptions options, UnityEditor.RuntimeClassRegistry usedClassRegistry, UnityEditor.BuildReporting.BuildReport report) (at C:/buildslave/unity/build/Editor/Mono/BuildPipeline/PostprocessBuildPlayer.cs:186)
UnityEditor.HostView:OnGUI()
```
* These errors persist even for the HoloLens apps that I deployed earlier. 
* It seems this is a problem independent of the Unity scene that I'm working on.
* For now, I'll keep working with a non-standalone Unity app (i.e. to run the app, the HoloLens will need to be tethered via WiFi).
* 10.8.227.69