using UnityEngine;

// Third weapon: boiling soup spills on a random enemy in range and hits everyone in the splash.
public class PotWeapon : WeaponBase
{
    [SerializeField] private float range = 6f;


    protected override bool TryAttack()
    {
        Collider2D[] enemiesDetected = Physics2D.OverlapCircleAll(transform.position, range, whatIsEnemy);

        if (enemiesDetected.Length == 0)
        {
            return false;
        }

        for (int i = 0; i < projectileCount; i++)
        {
            int indexToPick = Random.Range(0, enemiesDetected.Length);
            Collider2D enemy = enemiesDetected[indexToPick];

            Collider2D[] enemiesAffected = Physics2D.OverlapCircleAll(enemy.transform.position, areaOfEffect, whatIsEnemy);
            foreach (Collider2D enemyAffected in enemiesAffected)
            {
                if (enemyAffected.TryGetComponent(out EnemyInsistence enemyInsistence))
                {
                    enemyInsistence.ReduceInsistence(damage * playerStats.GetDamageMultiplier());
                }
            }
        }
        return true;
    }

    private void OnDrawGizmos()
    {
        Gizmos.DrawWireSphere(transform.position, range);
    }
}
