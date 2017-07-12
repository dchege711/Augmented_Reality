using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class PlayerController : MonoBehaviour {

	// By making it public, we can make changes in the editor without recompiling the code
	public float speed;		// Lest the ball be too slow
	public Text countText;	// Used to display # of collectibles gathered to the game screen.
	public Text winText;	// Lets the gamer know when they've won.

	private Rigidbody rb;	
	private int count;	// Keeps track of the number of collectibles collected


	// Code under Start() is called in the first frame when the script is active
	void Start(){
		// This will find and return a reference to the attached Rigidbody, if there is one.
		rb = GetComponent<Rigidbody>();
		count = 0;
		setCountText ();
		winText.text = "";
	}

	// Update is called before rendering a frame
	// This is where most of our game code will go
	// But we don't need this right now(?)
	// void Update() {
	//	
	// }

	// This is called before performing any Physics calculations.
	// This is where our Physics code will go
	void FixedUpdate(){
		
		// Hint: Use CTRL + single-quote, when highlighting the command that you need help

		// This grabs the input from our player through the keyboard
		// The horizontal and vertical axes are controlled by keys on the keyboard
		float moveHorizontal = Input.GetAxis("Horizontal");
		float moveVertical = Input.GetAxis("Vertical");

		// Create a 3D vector composed of x, y, z values
		Vector3 movement = new Vector3(moveHorizontal, 0.0f, moveVertical);

		// AddForce is a function that allows application of forces to rigid bodies
		rb.AddForce(movement * speed);
	}

	void OnTriggerEnter(Collider other) {
		// CompareTag is more efficient than checking for equality using ==
		if (other.gameObject.CompareTag ("Pick Up")) {
			other.gameObject.SetActive (false);
			count = count + 1;
			setCountText ();
			if (count == 12) {
				winText.text = "You Win!";
			}
		}
	}

	void setCountText() {
		countText.text = "Count: " + count.ToString ();
	}
}