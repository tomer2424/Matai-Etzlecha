using UnityEngine;
using UnityEngine.Pool;

public class ShiftExcuse : WeaponBase
{
    [Header("Components")]
    [SerializeField] private BulletBehaviour shiftExcusePrefab;
    [SerializeField] private Transform shiftExcuseFolder;

    [Header("Shooting parameters")]
    [SerializeField] private float range = 6f;

    private ObjectPool<BulletBehaviour> shiftExcusePool;

    protected override void Awake()
    {
        base.Awake();
        shiftExcusePool = new ObjectPool<BulletBehaviour>(CreateNewBullet, OnBulletTaken, OnBulletReturned, DestroyBullet);
    }

    private BulletBehaviour CreateNewBullet()
    {
        BulletBehaviour newBullet = Instantiate(shiftExcusePrefab, shiftExcuseFolder);
        newBullet.SetPool(shiftExcusePool);
        return newBullet;
    }

    private void OnBulletTaken(BulletBehaviour bullet)
    {
        bullet.gameObject.SetActive(true);
    }

    private void OnBulletReturned(BulletBehaviour bullet)
    {
        bullet.gameObject.SetActive(false);
    }

    private void DestroyBullet(BulletBehaviour bullet)
    {
        if (bullet != null)
        {
            Destroy(bullet.gameObject);
        }
    }

    protected override bool TryAttack()
    {
        Collider2D doda =  GetClosestDoda();
        if (doda != null)
        {
            Fire(doda);
            return true;
        }
        else
        {
            return false;
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


    // Takes a bullet from the pool and launches it from the excuse's position toward the target doda
    private void Fire(Collider2D dodaTarget)
    {
        Vector2 direction = dodaTarget.transform.position - transform.position;
        BulletBehaviour shiftExcuseBullet = shiftExcusePool.Get();
        shiftExcuseBullet.LaunchBullet(direction, transform.position, damage * playerStats.GetDamageMultiplier());
    }


    private void OnDrawGizmos() // Just to see the radius 
    {
        Gizmos.DrawWireSphere(transform.position, range);
    }

    protected override void ApplyLevel(int newLevel)
    {
        switch(newLevel)
        {
            case 2:
                Debug.Log("TODO: +1 projectile");
                break;
            case 3:
                damage += 5;
                break;
            case 4:
                Debug.Log("TODO: +1 projectile");
                break;
            case 5:
                damage += 5;
                fireInterval *= 0.8f;
                break;
        }
    }
}
