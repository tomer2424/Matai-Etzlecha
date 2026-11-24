using UnityEngine;

public abstract class WeaponBase : MonoBehaviour
{
    protected PlayerStats playerStats;
    [SerializeField] protected WeaponData weaponData;

    [SerializeField] protected LayerMask whatIsEnemy;

    protected float timerToNextFire = 1f;
    protected float fireInterval;
    protected float minFireInterval;

    protected float damage;

    protected int projectileCount;

    protected int currentLevel = 1;
    protected int maxLevel;

    protected virtual void Awake()
    {
        playerStats = GetComponentInParent<PlayerStats>();
        fireInterval = weaponData.fireInterval;
        minFireInterval = weaponData.minFireInterval;
        damage = weaponData.damage;
        projectileCount = weaponData.projectileCount;
        maxLevel = weaponData.weaponLevelUpgradeList.Count + 1;
    }


    protected virtual void Update()
    {
        HandleFiring();
    }

    // Counts down to the next shot.
    // If TryAttack fails, the attack stays "loaded" and is tried again next frame.
    private void HandleFiring()
    {
        timerToNextFire -= Time.deltaTime;
        if (timerToNextFire <= 0)
        {
            if (TryAttack())
            {
                // Weapon interval x player's global multiplier, but never below this weapon's minimum
                timerToNextFire = Mathf.Max(minFireInterval, fireInterval * playerStats.GetFireIntervalMultiplier());
            }
        }
    }

    protected abstract bool TryAttack();

    protected virtual void ApplyLevel(int level)
    {
        WeaponLevelUpgrade levelUpgrade = weaponData.weaponLevelUpgradeList[level - 2];
        damage += levelUpgrade.damageToAdd;
        projectileCount += levelUpgrade.projectilesToAdd;
        fireInterval *= levelUpgrade.fireIntervalMultiplier;
    }

    public void LevelUp()
    {
        if (currentLevel < maxLevel)
        {
            currentLevel += 1;
            Debug.Log("Level: " + currentLevel);
            ApplyLevel(currentLevel);
        }
    }
}
