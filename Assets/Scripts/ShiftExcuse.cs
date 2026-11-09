using UnityEngine;

public class ShiftExcuse : MonoBehaviour
{
    [Header("Components")]
    [SerializeField] private BulletBehaviour shiftExcusePrefab;
    [SerializeField] private Transform shiftExcuseFolder;

    [Header("Shooting parameters")]
    [SerializeField] private LayerMask whatIsEnemy;
    [SerializeField] private float range = 5f;

    private float fireInterval = 1f;
    private float timerToNextFire = 1f;


    private void Update()
    {
        HandleFiring();
    }


    // Counts down to the next shot and fires at the closest doda.
    // If no doda is in range, the shot stays "loaded" and fires as soon as one enters.
    private void HandleFiring()
    {
        timerToNextFire -= Time.deltaTime;
        if (timerToNextFire <= 0)
        {
            Collider2D doda = GetClosestDoda();
            if (doda != null)
            {
                timerToNextFire = fireInterval;
                Fire(doda);
            }
        }
    }


    // Returns the closest doda within range, or null if there is none.
    private Collider2D GetClosestDoda()
    {
        // decides who is in range (only colliders on the Enemy layer)
        Collider2D[] dodaList = Physics2D.OverlapCircleAll(transform.position, range, whatIsEnemy);

        // Start with "infinitely far" so the first doda always becomes the closest
        float closestDistanceSquared = Mathf.Infinity;
        Collider2D closestDoda = null;

        // Pick the doda with the smallest distance (squared, to avoid a square root)
        foreach (Collider2D doda in dodaList)
        {
            float tempDistanceSquared = (doda.transform.position - transform.position).sqrMagnitude;
            if (tempDistanceSquared < closestDistanceSquared)
            {
                closestDoda = doda;
                closestDistanceSquared = tempDistanceSquared;
            }
        }
        // Stays null if the list was empty
        return closestDoda;
    }


    // Creates the excuse bullet and calls it's launce method with a direction
    private void Fire(Collider2D dodaTarget)
    {
        Vector2 direction = dodaTarget.transform.position - transform.position;
        BulletBehaviour shiftExcuseBullet = Instantiate(shiftExcusePrefab, transform.position, Quaternion.identity, shiftExcuseFolder);
        
        shiftExcuseBullet.LaunchBullet(direction);
    }


    private void OnDrawGizmos() // Just to see the radius 
    {
        Gizmos.DrawWireSphere(transform.position, range);
    }
}
