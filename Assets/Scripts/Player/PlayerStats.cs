using UnityEngine;

// Holds the player's global stats. Weapons and movement read from here.
public class PlayerStats : MonoBehaviour
{
    [Header("Base values")]
    [SerializeField] private float baseMoveSpeed = 4f;

    [Header("Multipliers (1 = no change)")]
    [SerializeField] private float moveSpeedMultiplier = 1f;
    [SerializeField] private float damageMultiplier = 1f;
    [SerializeField] private float fireIntervalMultiplier = 1f;
    [SerializeField] private float damageTakenMultiplier = 1f;

    [Header("Min values")]
    [SerializeField] private float minDamageTakenMultiplier = 0.4f;

    [Header("Upgrade amounts per level")]
    [SerializeField] private float moveSpeedIncreasePerLevel = 0.08f;
    [SerializeField] private float damageIncreasePerLevel = 0.1f;
    [SerializeField] private float fireIntervalDecreasePerLevel = 0.08f;
    [SerializeField] private float damageTakenDecreasePerLevel = 0.08f;

    public float GetMoveSpeed()
    {
        return baseMoveSpeed * moveSpeedMultiplier;
    }

    public float GetDamageMultiplier()
    {
        return damageMultiplier;
    }

    public float GetFireIntervalMultiplier()
    {
        return fireIntervalMultiplier;
    }

    public float GetDamageTakenMultiplier()
    {
        return Mathf.Max(damageTakenMultiplier, minDamageTakenMultiplier);
    }

    public void IncreaseMoveSpeed()
    {
        moveSpeedMultiplier += moveSpeedIncreasePerLevel;
    }

    public void IncreaseDamage()
    {
        damageMultiplier += damageIncreasePerLevel;
    }

    public void DecreaseFireInterval()
    {
        fireIntervalMultiplier -= fireIntervalDecreasePerLevel;
    }

    public void DecreaseDamageTaken()
    {
        damageTakenMultiplier -= damageTakenDecreasePerLevel;
    }
}