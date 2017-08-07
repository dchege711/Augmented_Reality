using UnityEngine;
using System.Collections;

public class Bullet : MonoBehaviour
{
    /// <summary>
    /// Calls the TakeDamage() on the player upon the bullet hitting one.
    /// </summary>
    void OnCollisionEnter(Collision collision)
    {
        var hit = collision.gameObject;
        var health = hit.GetComponent<Health>();
        if (health != null) {
            health.TakeDamage(10);
        }
        // We now need to make this visible on the screen...

        Destroy(gameObject);
    }
}