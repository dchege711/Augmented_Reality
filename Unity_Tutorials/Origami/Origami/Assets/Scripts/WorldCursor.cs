using UnityEngine;

public class WorldCursor : MonoBehaviour
{
	private MeshRenderer meshRenderer;

	// Use this for initialization.
	// Start() is called (only once) if a script is enabled. 
	// Start() is called before any of the Update methods is called for the first time.
	void Start()
	{
		// Grab the mesh renderer that's on the same object as this script.
		// In this case, we'll attach the script to cursor gameObject.
		meshRenderer = this.gameObject.GetComponentInChildren<MeshRenderer>();
	}

	// Update is called once per frame
	void Update()
	{
		// Get the user's head position and orientation.
		var headPosition = Camera.main.transform.position;
		var gazeDirection = Camera.main.transform.forward;

		RaycastHit hitInfo;	// Useful for collecting information after a Raycast collides

		// This casts a ray originating from headPosition towards gazeDirection, extending to infinity
		// If there's a collision, hitInfo will bear information about the collision.
		if (Physics.Raycast(headPosition, gazeDirection, out hitInfo))
		{
			// If the raycast hit a hologram...

			// Display the cursor mesh.
			meshRenderer.enabled = true;

			// Move the cursor to the point where the raycast hit.
			this.transform.position = hitInfo.point;

			// Rotate the cursor to hug the surface of the hologram (for authenticity).
			this.transform.rotation = Quaternion.FromToRotation(Vector3.up, hitInfo.normal);
		}
		else
		{
			// If the raycast did not hit a hologram, hide the cursor mesh.
			meshRenderer.enabled = false;
		}
	}
}