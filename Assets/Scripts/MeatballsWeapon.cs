using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Pool;

public class MeatballsWeapon : WeaponBase
{
    [Header("Components")]
    [SerializeField] private BulletBehaviour meatballWeaponPrefab;
    [SerializeField] private Transform meatballWeaponFolder;

    [Header("Shooting parameters")]
    [SerializeField] private float range = 6f;

    private ObjectPool<BulletBehaviour> meatballWeaponPool;

    protected override void Awake()
    {
        base.Awake();
        meatballWeaponPool = new ObjectPool<BulletBehaviour>(CreateNewBullet, OnBulletTaken, OnBulletReturned, DestroyBullet);
    }

    private BulletBehaviour CreateNewBullet()
    {
        BulletBehaviour newBullet = Instantiate(meatballWeaponPrefab, meatballWeaponFolder);
        newBullet.SetPool(meatballWeaponPool);
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

    // Fires projectileCount meatballs at the closest dodas.
    // Returns false (attack stays "loaded") if no doda is in range.
    protected override bool TryAttack()
    {
        List<Collider2D> dodaList = GetClosestDodas();

        // Nobody in range, don't reset the timer
        if (dodaList.Count == 0)
        {
            return false;
        }

        // Each projectile takes the next doda, and starts over when the list ends
        // (3 projectiles, 2 dodas -> A, B, A)
        for (int i = 0; i < projectileCount; i++)
        {
            Fire(dodaList[i % dodaList.Count]);
        }
        return true;
    }



    // Returns up to projectileCount different dodas within range, closest first.
    // The list is empty if no doda is in range.
    private List<Collider2D> GetClosestDodas()
    {
        List<Collider2D> dodaList = new List<Collider2D>();

        // Everyone in range (only colliders on the Enemy layer), in no particular order
        Collider2D[] dodasFound = Physics2D.OverlapCircleAll(transform.position, range, whatIsEnemy);

        // One round per projectile: each round picks the closest doda that wasn't picked yet
        for (int i = 0; i < projectileCount; i++)
        {
            // Reset every round, so each round searches from scratch
            float closestDistanceSquared = Mathf.Infinity;
            Collider2D closestDoda = null;

            // Squared distance, to avoid a square root
            foreach (Collider2D doda in dodasFound)
            {
                float tempDistanceSquared = (doda.transform.position - transform.position).sqrMagnitude;
                if (tempDistanceSquared < closestDistanceSquared && !dodaList.Contains(doda))
                {
                    closestDoda = doda;
                    closestDistanceSquared = tempDistanceSquared;
                }
            }

            if (closestDoda != null)
            {
                dodaList.Add(closestDoda);
            }
            else
            {
                // Every doda in range is already picked, no need for more rounds
                break;
            }
        }
        return dodaList;
    }


    // Takes a bullet from the pool and launches it from the meatball's position toward the target doda
    private void Fire(Collider2D dodaTarget)
    {
        Vector2 direction = dodaTarget.transform.position - transform.position;
        BulletBehaviour meatballWeapon = meatballWeaponPool.Get();
        meatballWeapon.LaunchBullet(direction, transform.position, damage * playerStats.GetDamageMultiplier());
    }


    private void OnDrawGizmos() // Just to see the radius 
    {
        Gizmos.DrawWireSphere(transform.position, range);
    }
}
