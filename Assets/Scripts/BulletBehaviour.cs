using UnityEngine;
using UnityEngine.Pool;

public class BulletBehaviour : MonoBehaviour
{
    private Rigidbody2D rb;

    [SerializeField] private float moveSpeed = 8.0f;

    private float timeAlive = 0f;
    [SerializeField] private float maxAliveTime = 5f;

    [SerializeField] private float bulletDamage = 5f;
    private bool hasHit = false;

    private ObjectPool<BulletBehaviour> pool;


    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    private void Update()
    {
        timeAlive += Time.deltaTime;
        if (timeAlive >= maxAliveTime)
        {
            pool.Release(this);
        }
    }

    public void SetPool(ObjectPool<BulletBehaviour> pool)
    {
        this.pool = pool;
    }

    // Called from an outside script to set the direction and spawn position of the bullet and fire it
    public void LaunchBullet(Vector2 bulletDirection, Vector2 bulletPosition)
    {
        bulletDirection.Normalize();
        rb.position =  bulletPosition;
        transform.position = bulletPosition;
        rb.linearVelocity = bulletDirection * moveSpeed;
    }

    private void OnTriggerEnter2D(Collider2D collider)
    {
        if (!hasHit && collider.TryGetComponent(out EnemyInsistence enemyInsistence))
        {
            hasHit = true;
            enemyInsistence.ReduceInsistence(bulletDamage);
            pool.Release(this);
        }
    }

    private void OnEnable()
    {
        hasHit = false;
        timeAlive = 0;
    }
}
