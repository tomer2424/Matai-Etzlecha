using UnityEngine;
using UnityEngine.Pool;

public class NoteBehaviour : MonoBehaviour
{ 
    private ObjectPool<NoteBehaviour> pool;

    private bool wasCollected;
    [SerializeField] private int xp = 1;

    public void SetPool(ObjectPool<NoteBehaviour> pool)
    {
        this.pool = pool;
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (!wasCollected && collision.TryGetComponent(out LevelSystem levelSystem))
        {
            wasCollected = true;
            levelSystem.AddXP(xp);
            pool.Release(this);
        }
    }

    private void OnEnable()
    {
        wasCollected = false;
    }
}
