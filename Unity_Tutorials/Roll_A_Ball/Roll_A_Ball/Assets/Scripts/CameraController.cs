using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour {

	// This script was added to move the camera relative to the player
	// Using the GUI provided by Unity would have been too buggy.

	public GameObject player;
	private Vector3 offset;

	// Use this for initialization
	void Start () {
		offset = transform.position - player.transform.position;
	}
	
	// LateUpdate is called once per frame, but after all events
	// That way we're certain that the player has moved
	void LateUpdate () {
		// Before each frame, the camera will be moved appropriately
		transform.position = player.transform.position + offset;
	}
}