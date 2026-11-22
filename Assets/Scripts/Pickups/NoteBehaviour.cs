using UnityEngine;
using UnityEngine.Pool;

public class NoteBehaviour : MonoBehaviour
{ 
    private ObjectPool<NoteBehaviour> pool;

    private bool wasCollected;
    private int xp;

    public void SetPool(ObjectPool<NoteBehaviour> pool)
    {
        this.pool = pool;
    }

    public void SetXPAmount(int xpAmount)
    {
        xp = xpAmount;
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
