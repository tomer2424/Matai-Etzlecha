using UnityEngine;

// Why there is no EnemyBase (like WeaponBase):
// - Weapons differ in BEHAVIOUR (how they attack), which is code -> inheritance (WeaponBase + TryAttack override).
// - Enemy types (pizza, burger, fries...) mostly differ in NUMBERS (speed, insistence, damage) -> one EnemyData
//   asset per type is enough, and the same EnemyMovement / EnemyInsistence / EnemyDamage scripts read from it.
// - An enemy with special behaviour (e.g. a soda can that shoots, a burger that slows you) gets an EXTRA component on its prefab
//   (e.g. EnemyShooter) next to the usual ones, instead of a child class.
// Rule of thumb: different numbers -> data asset. Different behaviour -> code (a new component, or inheritance for weapons).
[CreateAssetMenu(fileName = "EnemyData", menuName = "Scriptable Objects/EnemyData")]
public class EnemyData : ScriptableObject
{
    public string enemyName;

    public float maxInsistence;
    public float moveSpeed;
    public float damage;
    public int xpDropped;

    [Range(0f, 1f)] public float hitLineChance;
    public string[] hitLines;
    public string[] giveUpLines;
}
