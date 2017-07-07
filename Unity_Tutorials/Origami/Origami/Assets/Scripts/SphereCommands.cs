using UnityEngine;

public class SphereCommands : MonoBehaviour {

	// Called by GazeGestureManager when the user performs a Select gesture
	void OnSelect()
	{
		// If the sphere has no Rigidbody component, add one to enable physics.
		// Physics makes the GameObject fall down...
		if (!this.GetComponent<Rigidbody>())
		{
			var rigidbody = this.gameObject.AddComponent<Rigidbody>();
			rigidbody.collisionDetectionMode = CollisionDetectionMode.Continuous;
		}
	}
}
