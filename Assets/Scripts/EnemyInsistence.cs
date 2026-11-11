using UnityEngine;
using UnityEngine.Pool;

public class EnemyInsistence : MonoBehaviour
{
    private float insistence;
    [SerializeField] private float maxInsistence = 10f;

    private bool isDead = false;

    private ObjectPool<EnemyMovement> pool;
    private EnemyMovement enemyMovement;

    private void Awake()
    {
        enemyMovement = GetComponent<EnemyMovement>();
    }

    public void SetPool(ObjectPool<EnemyMovement> pool)
    {
        this.pool = pool;
    }

    // called from an outside bullet gameobject to reduce the insistence
    public void ReduceInsistence(float insistenceToRemove)
    {
        if (!isDead)
        {
            insistence -= insistenceToRemove;
            if (insistence <= 0)
            {
                GiveUp();
            }
        }
    }

    private void GiveUp()
    {
        isDead = true;
        pool.Release(enemyMovement);
    }

    private void OnEnable()
    {
        isDead = false;
        insistence = maxInsistence;
    }
}
