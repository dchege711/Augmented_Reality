using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HitTarget : MonoBehaviour {

	// Public fields become settable properties in the Unity editor

	public GameObject underworld;
	public GameObject objectToHide;

	// Occurs when this object starts colliding with another object
	void OnCollisionEnter(Collision collision) {

		// Hide the stage and show the underworld
		objectToHide.SetActive(false);
		underworld.SetActive (true);

		// Disable Spatial Mapping to let the spheres enter the underworld
		SpatialMapping.Instance.MappingEnabled = false;
	}
}
