using Academy.HoloToolkit.Sharing;
using Academy.HoloToolkit.Unity;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Windows.Speech;


// Step 3: Sharing coordinates
public class HologramPlacement : Singleton<HologramPlacement>
{
    /// <summary>
    /// Tracks if we have been sent a transform for the model.
    /// The model is rendered relative to the actual anchor.
    /// </summary>
    public bool GotTransform { get; private set; }

	// Added in step 3: Sharing coordinates
	private bool animationPlayed = false;

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
		if (GotTransform) 
		{
			// Added in Step 3: Sharing coordinates
			if (ImportExportAnchorManager.Instance.AnchorEstablished && animationPlayed == false) {
				// This triggers the animation sequence for the anchor model and 
				// puts the cool materials on the model.
				GetComponent<EnergyHubBase>().SendMessage("OnSelect");
				animationPlayed = true;
			}
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

    public void OnSelect()
    {
        // Note that we have a transform.
        GotTransform = true;

        // The user has now placed the hologram.
        // Route input to gazed at holograms.
        // GestureManager.Instance.OverrideFocusedObject = null;
		// Commented out in step 3: Sharing our coordinates

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
		// We read the user ID but we don't use it here.
		msg.ReadInt64();

		transform.localPosition = CustomMessages.Instance.ReadVector3(msg);
		transform.localRotation = CustomMessages.Instance.ReadQuaternion(msg);

		// The first time, we'll want to send the message to the anchor to do its animation and
		// swap its materials.
		if (GotTransform == false)
		{
			GetComponent<EnergyHubBase>().SendMessage("OnSelect");
		}

		GotTransform = true;
	}

    public void ResetStage()
    {
        // We'll use this later.
    }
}