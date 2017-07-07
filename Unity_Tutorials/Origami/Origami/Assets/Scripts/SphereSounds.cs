using UnityEngine;

public class SphereSounds : MonoBehaviour {

	// Initialize variables
	AudioSource audioSource = null;
	AudioClip impactClip = null;
	AudioClip rollingClip = null;

	bool rolling = false;

	void Start() {
		
		// Add an AudioSource component and set up some of the defaults.
		// This is similar to what we did to OrigamiCollection, but now in C#
		// C# script is necessary because the sphere sounds will be changing.
		audioSource = gameObject.AddComponent<AudioSource>();
		audioSource.playOnAwake = false;
		audioSource.spatialize = true;
		audioSource.spatialBlend = 1.0f;
		audioSource.dopplerLevel = 0.0f;
		audioSource.rolloffMode = AudioRolloffMode.Logarithmic;
		audioSource.maxDistance = 20f;

		// Load the Sphere sounds from the Resources folder
		impactClip = Resources.Load<AudioClip>("Impact");
		rollingClip = Resources.Load<AudioClip> ("Rolling");
	}

	// Occurs when this object starts colliding with another object
	void OnCollisionEnter(Collision collision) {
		
		// Play an impact sound if the sphere impacts strongly enough.
		if (collision.relativeVelocity.sqrMagnitude >= 0.01f) {
			// Note: collision.relativeVelocity.magnitude = .1f requires additional computation
			audioSource.clip = impactClip;
			audioSource.Play ();
		}
	}

	// Occurs each frame that this object continues to collide with another object
	void OnCollisionStay(Collision collision) {
		
		Rigidbody rigid = this.gameObject.GetComponent<Rigidbody> ();

		// Play a rolling sound if the sphere is rolling fast enough.
		if (!rolling && rigid.velocity.magnitude >= 0.01f) {
			rolling = true;
			audioSource.clip = rollingClip;
			audioSource.Play();
		}

		// Stop the rolling sound if rolling slows down
		else if (rolling && rigid.velocity.magnitude < .01f) {
			rolling = false;
			audioSource.Stop ();
		}
	}
}
