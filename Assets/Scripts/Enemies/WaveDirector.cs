using UnityEngine;

// Decides WHAT spawns and WHEN.
// EnemySpawner only does the spawning itself (pool + position).
public class WaveDirector : MonoBehaviour
{
    [SerializeField] private float insistenceIncreasePerMinute = 0.1f;

    [SerializeField] private GameTimer gameTimer; // the single source of game time

    // Rows must be sorted by startTimeSeconds, and the first row should start at 0
    [SerializeField] private SpawnWave[] spawnWaveList;

    // Returns the spawn interval of the current row:
    // the last row whose start time has already passed
    public float GetSpawnInterval()
    {
        float currentTime = gameTimer.GetTimePassed();
        SpawnWave tempSpawnWave = null;
        foreach (SpawnWave wave in spawnWaveList)
        {
            if (wave.startTimeSeconds <= currentTime)
            {
                // this row has started, it's the current candidate
                tempSpawnWave = wave;
            }
            else
            {
                // this row hasn't started yet, and the rows after it start even later
                break;
            }
        }

        // Safety net: empty list, or the first row doesn't start at 0
        if (tempSpawnWave == null)
        {
            Debug.LogWarning("WaveDirector: no spawn row found for time " + currentTime + ". Check that spawnWaveList is not empty and the first row starts at 0.");
            return 1f;
        }
        return tempSpawnWave.spawnInterval;
    }


    public float GetInsistenceMultiplier()
    {
        float minute = Mathf.FloorToInt(gameTimer.GetTimePassed() / 60);
        return (1 + insistenceIncreasePerMinute * minute);
    }
}
