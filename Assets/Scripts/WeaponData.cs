using UnityEngine;

[CreateAssetMenu(fileName = "WeaponData", menuName = "Scriptable Objects/WeaponData")]
public class WeaponData : ScriptableObject
{
    public string weaponName;
    public string description;

    public float fireInterval;
    public float minFireInterval;

    public float damage;

    public int projectileCount;
}
