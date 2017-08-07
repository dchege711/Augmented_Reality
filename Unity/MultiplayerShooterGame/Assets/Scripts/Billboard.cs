using System.Collections;
using UnityEngine;

public class Billboard : MonoBehaviour {

    /// <summary>
    /// Keeps the Healthbar looking at the Main Camera
    /// </summary>
    void Update() {
        transform.LookAt(Camera.main.transform);
    }
}
