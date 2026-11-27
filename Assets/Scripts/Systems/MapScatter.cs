using UnityEngine;

public class MapScatter : MonoBehaviour
{
    [SerializeField] private GameObject[] placables;
    [SerializeField] private Transform placablesFolder;
    [SerializeField] private int amountToPlace = 300;

    [SerializeField] private float halfMapSize = 100f;
    [SerializeField] private float offsetFromWalls = 3f;

    [SerializeField] private float safeZoneRadius = 5f;
    [SerializeField] private float prefabZoneRadius = 3f;

    private void Start()
    {
        int maxTriesToPlace = 3000;
        int placed = 0;

        while (placed < amountToPlace && maxTriesToPlace > 0)
        {
            float xPos = Random.Range(-halfMapSize + offsetFromWalls, halfMapSize - offsetFromWalls);
            float yPos = Random.Range(-halfMapSize + offsetFromWalls, halfMapSize - offsetFromWalls);

            Vector2 spawnPos = new Vector2(xPos, yPos);

            if (spawnPos.sqrMagnitude < safeZoneRadius * safeZoneRadius)
            {
                maxTriesToPlace--;
                continue;
            }
            else if (Physics2D.OverlapCircle(spawnPos, prefabZoneRadius) != null)
            {
                maxTriesToPlace--;
                continue;
            }

            int index = Random.Range(0, placables.Length);
            Instantiate(placables[index], spawnPos, Quaternion.identity, placablesFolder);
            placed++;
        }
    }
}
