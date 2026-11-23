using UnityEngine;
using UnityEngine.Pool;

public class EnemySpawner : MonoBehaviour
{
    [Header("Components")]
    [SerializeField] private EnemyMovement enemyPrefab;
    [SerializeField] private Camera mainCam;
    [SerializeField] private Transform enemiesFolder;
    [SerializeField] private NotesSpawner notesSpawner;
    [SerializeField] private FloatingTextManager floatingTextManager;
    [SerializeField] private WaveDirector waveDirector;

    private float spawnInterval;
    private float timerToNextSpawn = 1.5f;

    private float spawnMargin = 0.5f; // makes the enemy spawn just outside of the camera view

    private ObjectPool<EnemyMovement> enemyPool;
    [SerializeField] private int maxEnemyAmount = 250;

    private void Awake()
    {
        enemyPool = new ObjectPool<EnemyMovement>(CreateNewEnemy, OnEnemyTaken, OnEnemyReturned, DestroyEnemy);
    }
    private EnemyMovement CreateNewEnemy()
    {
        EnemyMovement newEnemy = Instantiate(enemyPrefab, enemiesFolder);
        EnemyInsistence enemyInsistence = newEnemy.GetComponent<EnemyInsistence>();
        enemyInsistence.SetPool(enemyPool);
        enemyInsistence.SetNoteSpawner(notesSpawner);
        enemyInsistence.SetFloatingTextManager(floatingTextManager);
        return newEnemy;
    }
    private void OnEnemyTaken(EnemyMovement enemy)
    {
        enemy.gameObject.SetActive(true);
    }
    private void OnEnemyReturned(EnemyMovement enemy)
    {
        enemy.gameObject.SetActive(false);
    }
    private void DestroyEnemy(EnemyMovement enemy)
    {
        if (enemy != null)
        {
            Destroy(enemy.gameObject);
        }
    }


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
            if (enemyPool.CountActive < maxEnemyAmount)
            {
                SpawnEnemy();
            }
            timerToNextSpawn += spawnInterval; // keep the leftover time instead of discarding it
        }
    }


    // Gets the current spawn interval from the WaveDirector timeline
    private void HandleSpawnRate() 
    {
        spawnInterval = waveDirector.GetSpawnInterval(); 
    }


    private void SpawnEnemy() 
    {
        Vector3 spawnLocation = GetSpawnLocation();
        EnemyMovement enemy = enemyPool.Get();

        float insistenceMultiplier = waveDirector.GetInsistenceMultiplier();
        EnemyInsistence enemyInsistence = enemy.GetComponent<EnemyInsistence>();
        enemyInsistence.ApplyInsistenceMultiplier(insistenceMultiplier);

        enemy.SetEnemyPosition(spawnLocation);
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
