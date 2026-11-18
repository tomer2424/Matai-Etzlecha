using UnityEngine;

public abstract class WeaponBase : MonoBehaviour
{
    protected PlayerStats playerStats;

    [SerializeField] protected LayerMask whatIsEnemy;
    protected float timerToNextFire = 1f;
    [SerializeField] protected float fireInterval = 1f;
    [SerializeField] protected float minFireInterval = 0.4f;
    [SerializeField] protected float damage = 5f;

    protected virtual void Awake()
    {
        playerStats = GetComponentInParent<PlayerStats>();
    }


    private void Update()
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
    
    





}
