using UnityEngine;
using UnityEngine.Networking;

/// <summary>
/// We're using the MultiPlayer Networking High Level API
/// The Server and all of the Clients are executing the same code from the same scripts on the same GameObjects at the same time.
/// 2 clients in the game? We'll have 6 gameobjects running, 2 on each client and 2 on the server
/// </summary>

public class PlayerController : NetworkBehaviour // Was 'MonoBehaviour'. Changed to make the script network-aware
{
    // Initialize publicly accessible references
    // This allows us to attach the game objects to this script in the prefabs folder
    public GameObject bulletPrefab;
    public Transform bulletSpawn;

    void Update()
    {
        // Scripts that derive from NetworkBehaviour will understand what LocalPlayer is.
        // LocalPlayer is the player GameObject 'owned' by the local client.
        if (!isLocalPlayer) {
            // We only want the local player to execute the movement code, hence this check
            return;
        }

        // This code allows the player to use WASD & arrow keys or a controller to move the player.
        var x = Input.GetAxis("Horizontal") * Time.deltaTime * 150.0f;
        var z = Input.GetAxis("Vertical") * Time.deltaTime * 3.0f;
        transform.Rotate(0, x, 0);
        transform.Translate(0, 0, z);

        // We also attached a Network Transform to the player prefab so that there's synchronization.
        // Tradeoff: frequent sync == poor game performance; infrequent sync == poor feel of the game

        // Okay, let's shoot 'em bullets!
        if (Input.GetKeyDown(KeyCode.Space)) {
            CmdFire();
        }
    }

    // The [Command] attribute == this function will be called by the Client, but will be run on the Server
    // Commands can only be sent from the local player object.
    [Command]
    void CmdFire()
    {
        // Create the Bullet from the Bullet Prefab
        var bullet = (GameObject)Instantiate(
            bulletPrefab,
            bulletSpawn.position,
            bulletSpawn.rotation);

        // Add velocity to the bullet
        bullet.GetComponent<Rigidbody>().velocity = bullet.transform.forward * 6;

        // Spawn the bullet on the Clients
        // Spawning 101: Create a game object on the Server and all of the Clients connected to the Server
        // When the game object changes on the Server, all Clients will be told. 
        // If another Client joins, the game objects will also be spawned on that Client in the correct state.
        NetworkServer.Spawn(bullet);

        // Destroy the bullet after 2 seconds
        Destroy(bullet, 2.0f);
    }

    // This function is only called by the LocalPlayer on their Client.
    // Good place for initializing player specifics like cameras and input.
    public override void OnStartLocalPlayer()
    {
        // Each player will see their local player as blue (*insert social commentary*)
        GetComponent<MeshRenderer>().material.color = Color.blue;
    }
}
