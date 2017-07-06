using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.VR.WSA.WebCam;
using System.Linq;

// Code obtained from https://developer.microsoft.com/en-us/windows/mixed-reality/locatable_camera_in_unity

public class CapturePhoto : MonoBehaviour {

	// Start by creating a PhotoCapture Object
	PhotoCapture photoCaptureObject = null;
	void Start () {
		PhotoCapture.CreateAsync (false, OnPhotoCaptureCreated);
	}

	// Next, store our object, set our parameters, and start Photo Mode
	void OnPhotoCaptureCreated(PhotoCapture captureObject) {
		
		photoCaptureObject = captureObject;

		Resolution cameraResolution = PhotoCapture.SupportedResolutions.OrderByDescending((res) => res.width * res.height).First();
		CameraParameters c = new CameraParameters();
		c.hologramOpacity = 0.0f;
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
			string filePath = System.IO.Path.Combine(Application.persistentDataPath, filename);

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
