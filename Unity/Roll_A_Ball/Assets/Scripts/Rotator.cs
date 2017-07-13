using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// We want to set up collectible cubes in our game
// To make them spin (so as to attract player's attention), we'll use this script.
public class Rotator : MonoBehaviour {
	
	// Update is called once per frame
	void Update () {
		// Using Time.deltaTime ensures that our rotation is smooth
		transform.Rotate (new Vector3 (15, 30, 45) * Time.deltaTime);
	}
}
