using System.Collections.Generic;
using UnityEngine;

// Second weapon: frying pans that spin around the chef and hit whatever they touch.
public class PanWeapon : WeaponBase
{
    [SerializeField] private GameObject panPrefab;
    private List<Transform> panList;                    // every pan this weapon created, so TryAttack knows where they are

    [SerializeField] private float panHitRadius = 0.4f; // size of one pan's hit area (not the orbit radius)

    protected override void Awake()
    {
        base.Awake();

        panList = new List<Transform>();
        CreatePans();
    }


    protected override void Update()
    {
        base.Update();   // keeps WeaponBase's attack timer running
        RotatePans();
    }

    // Spins the whole weapon around its own center, so its child pans orbit the chef
    private void RotatePans()
    {
        transform.Rotate(0f, 0f, speed * Time.deltaTime);
    }

    // Called by WeaponBase every fireInterval (0.5s): hits every enemy touching any pan.
    // Returns false if nothing was hit, so the attack stays "loaded" and the next touch hits right away.
    protected override bool TryAttack()
    {
        bool hitDetected = false;
        foreach (Transform pan in panList)
        {
            // Enemies inside this pan's hit circle, at the pan's position in the world
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

    // Creates projectileCount pans as children of this weapon, evenly spaced around the chef.
    // Each pan is also turned by its angle, so its handle always points at the chef.
    private void CreatePans()
    {
        ClearOldPans();

        float spacingBetweenPans = 360f / projectileCount; // degrees between two neighbouring pans (float, so 7 pans still divide evenly)

        for (int i = 0; i < projectileCount; i++)
        {
            float angle = spacingBetweenPans * i; // this pan's place on the circle (0, 120, 240...)

            GameObject pan = Instantiate(panPrefab, gameObject.transform);
            panList.Add(pan.transform);
            pan.transform.localPosition = Quaternion.Euler(0, 0, angle) * new Vector3(areaOfEffect, 0f, 0f); // turn the "clock hand" to the angle
            pan.transform.localRotation = Quaternion.Euler(0, 0, angle); // turn the pan too, handle toward the chef
        }
    }

    private void ClearOldPans()
    {
        foreach (Transform pan in panList)
        {
            Destroy(pan.gameObject);
        }
        panList.Clear();
    }

    protected override void ApplyLevel(int level)
    {
        base.ApplyLevel(level);
        CreatePans();
    }

    // Shows each pan's hit area in the Scene view (only while playing, when the pans exist)
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