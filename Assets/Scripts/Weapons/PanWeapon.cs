using System.Collections.Generic;
using UnityEngine;

// Second weapon: frying pans that spin around the chef and hit whatever they touch.
public class PanWeapon : WeaponBase
{
    [SerializeField] private GameObject panPrefab;
    private List<Transform> panList;

    [SerializeField] private float radius = 1.8f;      // distance of the pans from the chef
    [SerializeField] private float spinSpeed = 180f;   // degrees per second
    [SerializeField] private float panHitRadius = 0.4f;

    protected override void Awake()
    {
        base.Awake();

        panList = new List<Transform>();

        // Create one pan as a child of this weapon, and push it out to the radius
        GameObject pan = Instantiate(panPrefab, gameObject.transform);
        panList.Add(pan.transform);
        pan.transform.localPosition = new Vector3(radius, 0f, 0f);
    }

    protected override void Update()
    {
        base.Update();   // keeps WeaponBase's attack timer running
        RotatePans();
    }

    // Spins the whole weapon around its own center, so its child pans orbit the chef
    private void RotatePans()
    {
        transform.Rotate(0f, 0f, spinSpeed * Time.deltaTime);
    }

    protected override bool TryAttack()
    {
        bool hitDetected = false;
        foreach (Transform pan in panList)
        {
            Collider2D[] enemies = Physics2D.OverlapCircleAll(pan.transform.position, panHitRadius, whatIsEnemy);

            foreach (Collider2D enemy in enemies)
            {
                if (enemy.TryGetComponent(out EnemyInsistence enemyInsistence))
                {
                    hitDetected = true;
                    enemyInsistence.ReduceInsistence(damage * playerStats.GetDamageMultiplier());
                }
            }
        }
        return hitDetected;
    }


    private void OnDrawGizmos()
    {
        if (panList == null)
        {
            return;
        }    

        foreach (Transform pan in panList)
        {
            Gizmos.DrawWireSphere(pan.transform.position, panHitRadius);
        }
    }
}