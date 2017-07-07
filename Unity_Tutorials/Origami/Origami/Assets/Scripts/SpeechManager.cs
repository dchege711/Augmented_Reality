using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Windows.Speech;

public class SpeechManager : MonoBehaviour {

	// You can have as many keyword recognizers.
	// But no two/more recognizers should be listening for the same keyword
	KeywordRecognizer keywordRecognizer = null;
	Dictionary<string, System.Action> keywords = new Dictionary<string, System.Action>();

	void Start() {
		keywords.Add ("Reset world", () => {
			// Call the OnReset method in every descendant object.
			this.BroadcastMessage("OnReset");
		});

		keywords.Add ("Drop Sphere", () => {
			var focusObject = GazeGestureManager.Instance.FocusedObject;
			if (focusObject != null) {
				// Call the OnDrop method on just the focused object.
				// Note that the receiving method can ignore the argument by having 0 arguments
				focusObject.SendMessage("OnDrop");
			}
		});

		// Tell the KeyWordRecognizer about our keywords. 
		// Uses a medium confidence level by default
		keywordRecognizer = new KeywordRecognizer(keywords.Keys.ToArray());

		// Register a callback for the KeywordRecognizer and start recognizing
		// To understand the += syntax for delegates, see https://youtu.be/RSN-A0NZTO0
		keywordRecognizer.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognized;
		// keywordRecognizer.OnPhraseRecognized is a Delegate object
		// Once it's ran, it's going to run KeywordRecognizer_OnPhraseRecognized
	}

	// Called whenever a phrase is recognized
	void KeywordRecognizer_OnPhraseRecognized (PhraseRecognizedEventArgs args)
	{
		System.Action keywordAction;	// Because we put in System.Action as values
		// A way of trying keys that may not be in the dictionary, without exceptions
		if (keywords.TryGetValue (args.text, out keywordAction)) {
			// Invoke whichever function that's contained at that key
			keywordAction.Invoke ();
		}
	}
}
