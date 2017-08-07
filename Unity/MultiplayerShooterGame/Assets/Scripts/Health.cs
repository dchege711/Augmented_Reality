using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

/// <summary>
/// Tracks and displayes the Current Health of the player
/// </summary>
public class Health : NetworkBehaviour
{
    public const int maxHealth = 100;

    // SyncVar makes currentHealth a synchronized variable
    // SyncVar hooks link functions that are invoked on the Server and all clients when SyncVar's value changes
    // Now when currentHealth changes, OnChangedHealth will be called on the Server and all Clients to update the Healthbar
    [SyncVar(hook = "OnChangeHealth")]
    public int currentHealth = maxHealth;

    // Note: We're referencing the Foreground element's RectTransform (the green one)
    public RectTransform healthBar;

    public bool destroyOnDeath; // We'll activate this for the enemy prefab.

    private NetworkStartPosition[] spawnPoints;

    void Start()
    {
        if (isLocalPlayer) {
            // Find all instances of the NetworkStartPosition component
            spawnPoints = FindObjectsOfType<NetworkStartPosition>();
        }
    }

    /// <summary>
    /// Takes damage and reduces health when the player is hit.
    /// </summary>
    /// <param name="amount"></param>
    public void TakeDamage(int amount)
    {
        if (!isServer)
        {
            // We want changes to the player's current health to only be applied on the Server
            // These changes are then Synchronized on the Clients
            // Prevents discrepancies, e.g. bullet getting destroyed before another client registers a collision
            return;
        }

        currentHealth -= amount;
        if (currentHealth <= 0)
        {
            if (destroyOnDeath)
            {
                Destroy(gameObject);
            }
            else {
                // Respawn the player in full health
                currentHealth = maxHealth;
                // If the Server resets the player, the Client would override the Server as the Client has authority
                // This is why the Server instructs the Client to reset the player. Network Transform enables a sync.
                RpcRespawn();
                // Enemies don't get respawned since they don't pass the isLocalPlayer test.
            }
        }
    }

    // We now need to update Bullet.cs to call TakeDamage() on the target player's Health.cs

    /// <summary>
    /// A SyncVar hook function that synchronizes the healthBar across all Clients
    /// </summary>
    /// <param name="health"></param>
    void OnChangeHealth(int health)
    {
        // We need to change the RectTransform's Size Delta as a Vector2 to change the width
        healthBar.sizeDelta = new Vector2(health, healthBar.sizeDelta.y);
    }

    /// <summary>
    /// Respawns the player.
    /// </summary>
    // ClientRpc's are the opposite of Commands. They're called on the Server, but executed on the Client.
    [ClientRpc]
    void RpcRespawn() {
        if (isLocalPlayer) {
            // Set the respawn position to be origin by default.
            Vector3 spawnPoint = Vector3.zero;

            // If there is a spawn point array and the array is not empty, pick a spawn point at random
            if (spawnPoints != null && spawnPoints.Length > 0) {
                spawnPoint = spawnPoints[Random.Range(0, spawnPoints.Length)].transform.position;
            }

            // Set the player’s position to the chosen spawn point
            transform.position = spawnPoint;
        }
    }
}
