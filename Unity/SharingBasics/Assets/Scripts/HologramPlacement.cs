using Academy.HoloToolkit.Sharing;
using Academy.HoloToolkit.Unity;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Windows.Speech;
using System;


// Step 3: Sharing coordinates
public class HologramPlacement : Singleton<HologramPlacement>
{
    /// <summary>
    /// Tracks if we have been sent a transform for the model.
    /// The model is rendered relative to the actual anchor.
    /// </summary>
    public bool GotTransform { get; private set; }

	// Added in step 3: Sharing coordinates
    private string prevDateTime;

    void Start()
    {
        // Start by making the model as the cursor.
        // So the user can put the hologram where they want.
        // GestureManager.Instance.OverrideFocusedObject = this.gameObject;
		// The above line was commented out in step 3: Sharing coordinates

		// Step 3: We care about getting updates for the anchor transform
		CustomMessages.Instance.MessageHandlers[CustomMessages.TestMessageID.StageTransform] = this.OnStageTransfrom;

		// Step 3: And when a new user joins, we will send the anchor transform that we have.
		SharingSessionTracker.Instance.SessionJoined += Instance_SessionJoined;

        // Initialize the datetime variable so that we can send coordinates each second
        prevDateTime = System.DateTime.Now.ToString();
    }

	/// <summary>
	/// When a new user joins, we want to send them the relative transform for the anchor if we have it.
	/// Step 3
	/// </summary>
	/// <param name="sender">Sender.</param>
	/// <param name="e">E.</param>
    private void Instance_SessionJoined (object sender, SharingSessionTracker.SessionJoinedEventArgs e)
    {
		if (GotTransform)
		{
			CustomMessages.Instance.SendStageTransform(transform.localPosition, transform.localRotation);
		}
    }

    void Update()
    {
        string currentTime = System.DateTime.Now.ToString();
        // Send the data every second
        if (currentTime != prevDateTime) {
            prevDateTime = currentTime;
            // print(currentTime + " : Sending test data");
            // sendTestData();
        }

		if (GotTransform) 
		{
            Debug.Log("Received transform");
		}
		else
        {
			// If we've not received a transform, place the gameobject according to the gaze.
			// Vector3.Lerp(a, b, t) interpolates between the vectors a and b by the interpolant t.
            transform.position = Vector3.Lerp(transform.position, ProposeTransformPosition(), 0.2f);
        }
    }

    Vector3 ProposeTransformPosition()
    {
        // Put the model 2m in front of the user.
        Vector3 retval = Camera.main.transform.position + Camera.main.transform.forward * 2;

        return retval;
    }

    /// <summary>
    /// Sends data to help us measure bandwidth and performance
    /// </summary>
    private void sendTestData() {
        Vector3 v = Camera.main.transform.position;
        // Send 10 vector3's
        for (int i = 0; i < 10; i++) {
            CustomMessages.Instance.SendVector3(v);
        }
    }

    public void OnSelect()
    {
        // Note that we have a transform.
        GotTransform = true;
		// And send this transform to our friends in the session
		CustomMessages.Instance.SendStageTransform(transform.localPosition, transform.localRotation);
    }

	/// <summary>
	/// When a remote system has a transform for us, we'll get it here.
	/// Added in Step 3: Sharing coordinates
	/// </summary>
	/// <param name="msg"></param>
	void OnStageTransfrom(NetworkInMessage msg)
	{
		long senderID = msg.ReadInt64();
        Debug.Log(senderID.ToString() + " sent us a stage transform.");

        // Set the hologram according to the received transform
		transform.localPosition = CustomMessages.Instance.ReadVector3(msg);
		transform.localRotation = CustomMessages.Instance.ReadQuaternion(msg);
        
		GotTransform = true;
	}

    // I'm not so sure how these are getting called...

    // Helper method for receiving vector3's
    public void OnExperimentalVector3(NetworkInMessage msg) {
        long senderID = msg.ReadInt64();
        Vector3 v = CustomMessages.Instance.ReadVector3(msg);
        Debug.Log(senderID.ToString() + " sent us a vector3 : " + v.ToString());
    }

    // Helper method for receiving ints
    public void OnExperimentalInt(NetworkInMessage msg)
    {
        long senderID = msg.ReadInt64();
        int sentInt = msg.ReadInt32();
        Debug.Log(senderID.ToString() + " sent us an int : " + sentInt.ToString());
    }

    public void ResetStage()
    {
        // We'll use this later.
    }
}