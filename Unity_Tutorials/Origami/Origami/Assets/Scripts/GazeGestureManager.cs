using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.VR.WSA.Input;

// This script can detect the HoloLens Select Gesture
public class GazeGestureManager : MonoBehaviour {

	public static GazeGestureManager Instance { get; private set; }

	// Represents the hologram that is currently being gazed at.
	public GameObject FocusedObject { get; private set; }

	GestureRecognizer recognizer;

	// Use this for initialization
	void Awake()
	{
		Instance = this;

		// Set up a GestureRecognizer to detect Select gestures.
		recognizer = new GestureRecognizer();

		// TappedEvent fires on finger release after a finger press & 
		// after the system voice command "Select" has been processed.
		recognizer.TappedEvent += (source, tapCount, ray) =>
		{
			// Send an OnSelect message to the focused object and its ancestors.
			if (FocusedObject != null)
			{
				FocusedObject.SendMessageUpwards("OnSelect");
			}
		};

		// GestureRecognizers will only receive events after StartCapturingGestures() is called
		recognizer.StartCapturingGestures();
	}

	// Update is called once per frame
	void Update()
	{
		// Figure out which hologram is focused in this frame.
		GameObject oldFocusObject = FocusedObject;

		// Do a raycast into the world based on the user's
		// head position and orientation.
		var headPosition = Camera.main.transform.position;
		var gazeDirection = Camera.main.transform.forward;

		RaycastHit hitInfo;
		if (Physics.Raycast(headPosition, gazeDirection, out hitInfo))
		{
			// If the raycast hit a hologram, use that as the focused object.
			FocusedObject = hitInfo.collider.gameObject;
		}
		else
		{
			// If the raycast did not hit a hologram, clear the focused object.
			FocusedObject = null;
		}

		// If the focused object changed this frame,
		// start detecting fresh gestures again.
		if (FocusedObject != oldFocusObject)
		{
			recognizer.CancelGestures();
			recognizer.StartCapturingGestures();
		}
	}
}
