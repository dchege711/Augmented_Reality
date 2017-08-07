using UnityEngine;
using UnityEngine.Networking;   // As usual, .Networking and NetworkBehaviour is required.

public class EnemySpawner : NetworkBehaviour
{

    public GameObject enemyPrefab;
    public int numberOfEnemies;

    // Remember OnStartLocalPlayer() that's used to set the local player's color to blue?
    // OnStartServer() is called on the Server when the Server starts listening to the Network
    public override void OnStartServer()
    {
        for (int i = 0; i < numberOfEnemies; i++)
        {
            var spawnPosition = new Vector3(
                Random.Range(-8.0f, 8.0f),
                0.0f,
                Random.Range(-8.0f, 8.0f));

            var spawnRotation = Quaternion.Euler(
                0.0f,
                Random.Range(0, 180),
                0.0f);

            var enemy = (GameObject)Instantiate(enemyPrefab, spawnPosition, spawnRotation);
            NetworkServer.Spawn(enemy);
        }
    }
}