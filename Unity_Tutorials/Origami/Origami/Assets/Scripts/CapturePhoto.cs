using System;
using UnityEngine;
using UnityEngine.VR.WSA.WebCam;
using System.Linq;

// Code obtained from https://developer.microsoft.com/en-us/windows/mixed-reality/locatable_camera_in_unity

// Haha! Joke's on me. I should have said, "Hey Cortana, take a picture." And she would have done it all for me.
// Note: This function is buggy. 
// It does take a picture when a hologram is selected, but the field of view and brightness need more debugging.
// Lesson Learned: Don't reinvent the wheel!

// That said, I've pulled this script from all holograms. 
// If you want to use it, attach the script to any holograms that you'd want to activate the taking of photos.

public class CapturePhoto : MonoBehaviour {

	// Start by creating a PhotoCapture Object
	PhotoCapture photoCaptureObject = null;
	bool showHolograms = true;
	// void Start() {
		// PhotoCapture.CreateAsync (showHolograms, OnPhotoCaptureCreated);
	// }

	// Activated when a hologram is selected
	void OnSelect() {
		PhotoCapture.CreateAsync (showHolograms, OnPhotoCaptureCreated);
	}


	// Next, store our object, set our parameters, and start Photo Mode
	void OnPhotoCaptureCreated(PhotoCapture captureObject) {
		
		photoCaptureObject = captureObject;

		// For debug purposes, I want to see the resolutions available...
		foreach (Resolution resolution in PhotoCapture.SupportedResolutions) {
			Debug.Log (resolution);
		}

		Resolution cameraResolution = PhotoCapture.SupportedResolutions.OrderByDescending((res) => res.width * res.height).First();
		CameraParameters c = new CameraParameters();
		c.hologramOpacity = 0.9f;
		c.cameraResolutionWidth = cameraResolution.width;
		c.cameraResolutionHeight = cameraResolution.height;
		c.pixelFormat = CapturePixelFormat.BGRA32;

		captureObject.StartPhotoModeAsync(c, OnPhotoModeStarted);
	}
		

	// We want to capture the photo directly to a PNG file and store it on disk
	// I'll later upload the photos to Github for clearer documentation
	private void OnPhotoModeStarted(PhotoCapture.PhotoCaptureResult result)
	{
		if (result.success)
		{
			string filename = string.Format(@"CapturedImage{0}_n.jpg", Time.time);
			string path = System.Environment.GetFolderPath (System.Environment.SpecialFolder.MyDocuments);
			string filePath = System.IO.Path.Combine(path, filename);

			photoCaptureObject.TakePhotoAsync(filePath, PhotoCaptureFileOutputFormat.PNG, OnCapturedPhotoToDisk);
			Debug.Log (filePath);
		}
		else
		{
			Debug.LogError("Unable to start photo mode!");
		}
	}

	// After capturing photo to disk, exit photo mode and clean up our objects
	void OnCapturedPhotoToDisk(PhotoCapture.PhotoCaptureResult result)
	{
		if (result.success)
		{
			Debug.Log("Saved Photo to disk!");
			photoCaptureObject.StopPhotoModeAsync(OnStoppedPhotoMode);
		}
		else
		{
			Debug.Log("Failed to save Photo to disk");
		}
	}


	// Clean up once you're done. Preserves resources.
	void OnStoppedPhotoMode(PhotoCapture.PhotoCaptureResult result)
	{
		photoCaptureObject.Dispose();
		photoCaptureObject = null;
	}
	
	// Update is called once per frame
	// void Update () {
	//	
	// }
}
