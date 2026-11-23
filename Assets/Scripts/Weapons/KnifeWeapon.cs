using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Pool;

public class KnifeWeapon : WeaponBase
{
    [Header("Components")]
    [SerializeField] private BulletBehaviour knifeWeaponPrefab;
    [SerializeField] private Transform knifeWeaponFolder;

    [Header("Shooting parameters")]
    [SerializeField] private float range = 6f;

    private ObjectPool<BulletBehaviour> knifeWeaponPool;

    protected override void Awake()
    {
        base.Awake();
        knifeWeaponPool = new ObjectPool<BulletBehaviour>(CreateNewBullet, OnBulletTaken, OnBulletReturned, DestroyBullet);
    }

    private BulletBehaviour CreateNewBullet()
    {
        BulletBehaviour newBullet = Instantiate(knifeWeaponPrefab, knifeWeaponFolder);
        newBullet.SetPool(knifeWeaponPool);
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

    // Throws projectileCount knives at the closest enemies.
    // Returns false (attack stays "loaded") if no enemy is in range.
    protected override bool TryAttack()
    {
        List<Collider2D> targetList = GetClosestEnemies();

        // Nobody in range, don't reset the timer
        if (targetList.Count == 0)
        {
            return false;
        }

        // Each knife takes the next enemy, and starts over when the list ends
        // (3 knives, 2 enemies -> A, B, A)
        for (int i = 0; i < projectileCount; i++)
        {
            Fire(targetList[i % targetList.Count]);
        }
        return true;
    }



    // Returns up to projectileCount different enemies within range, closest first.
    // The list is empty if no enemy is in range.
    private List<Collider2D> GetClosestEnemies()
    {
        List<Collider2D> targetList = new List<Collider2D>();

        // Everyone in range (only colliders on the Enemy layer), in no particular order
        Collider2D[] enemiesFound = Physics2D.OverlapCircleAll(transform.position, range, whatIsEnemy);

        // One round per knife: each round picks the closest enemy that wasn't picked yet
        for (int i = 0; i < projectileCount; i++)
        {
            // Reset every round, so each round searches from scratch
            float closestDistanceSquared = Mathf.Infinity;
            Collider2D closestEnemy = null;

            // Squared distance, to avoid a square root
            foreach (Collider2D enemy in enemiesFound)
            {
                float tempDistanceSquared = (enemy.transform.position - transform.position).sqrMagnitude;
                if (tempDistanceSquared < closestDistanceSquared && !targetList.Contains(enemy))
                {
                    closestEnemy = enemy;
                    closestDistanceSquared = tempDistanceSquared;
                }
            }

            if (closestEnemy != null)
            {
                targetList.Add(closestEnemy);
            }
            else
            {
                // Every enemy in range is already picked, no need for more rounds
                break;
            }
        }
        return targetList;
    }


    // Takes a knife from the pool and throws it from the weapon's position toward the target enemy
    private void Fire(Collider2D enemyTarget)
    {
        Vector2 direction = enemyTarget.transform.position - transform.position;
        BulletBehaviour knife = knifeWeaponPool.Get();
        knife.LaunchBullet(direction, transform.position, damage * playerStats.GetDamageMultiplier());
    }


    private void OnDrawGizmos() // Just to see the radius 
    {
        Gizmos.DrawWireSphere(transform.position, range);
    }
}
