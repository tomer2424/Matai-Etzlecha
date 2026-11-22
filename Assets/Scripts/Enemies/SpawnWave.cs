using UnityEngine;

// One row of the spawn timeline.
// A row lasts until the next row starts, so there is no end time.
[System.Serializable]
public class SpawnWave
{
    public float startTimeSeconds; // when this row starts (minute x 60)
    public float spawnInterval;    // seconds between spawns (1 / enemies per second)
}
