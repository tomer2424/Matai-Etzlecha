using UnityEngine;

public class EnemyDamage : MonoBehaviour
{
    [SerializeField] private EnemyData enemyData;
    private float damage;

    private void Awake()
    {
        damage = enemyData.damage;
    }

    public float Damage => damage;
}
