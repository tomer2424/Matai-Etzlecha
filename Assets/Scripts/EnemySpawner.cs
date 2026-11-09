using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    [Header("Components")]
    [SerializeField] private EnemyMovement enemyPrefab;
    [SerializeField] private Camera mainCam;
    [SerializeField] private Transform enemiesFolder;

    [SerializeField] private AnimationCurve spawnAnimationCurve;
    private float spawnInterval;
    private float spawnIntervalMinimum = 0.5f;
    private float globalTimer = 0;
    private float timerToNextSpawn = 1.5f;

    private float spawnMargin = 0.5f; // makes the enemy spawn just outside of the camera view


    private void Update()
    {
        HandleSpawning(); 
    }


    // Updates the spawn rate over time and spawns enemies when the timer runs out
    private void HandleSpawning() 
    {
        HandleSpawnRate();

        timerToNextSpawn -= Time.deltaTime;
        while (timerToNextSpawn <= 0)
        {
            SpawnEnemy();
            timerToNextSpawn += spawnInterval; // keep the leftover time instead of discarding it
        }
    }


    // method for gradually decreasing the spawn Interval
    private void HandleSpawnRate() 
    {
        globalTimer += Time.deltaTime;
        spawnInterval = Mathf.Max(spawnAnimationCurve.Evaluate(globalTimer), spawnIntervalMinimum);
    }


    private void SpawnEnemy() 
    {
        Vector3 spawnLocation = GetSpawnLocation();
        Instantiate(enemyPrefab, spawnLocation, Quaternion.identity, enemiesFolder);
    }


    // Return a random point on a circle that surrounds the visible screen.
    private Vector3 GetSpawnLocation() 
    {
        // Visible area in world units
        float halfScreenHeight = mainCam.orthographicSize;
        float halfScreenWidth = halfScreenHeight * mainCam.aspect;

        // Distance from the screen center to its corner, so the circle is outside the screen in every direction
        float spawnRadius = new Vector2(halfScreenWidth, halfScreenHeight).magnitude;

        // Random direction with length 1 in the circle
        Vector3 spawnDirection = Random.insideUnitCircle.normalized;
        if (spawnDirection == Vector3.zero)
        {
            spawnDirection = Vector3.up;
        }

        Vector3 location = mainCam.transform.position + spawnDirection * (spawnRadius + spawnMargin);
        location.z = 0;

        return location;
    }
}
