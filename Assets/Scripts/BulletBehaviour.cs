using UnityEngine;

public class BulletBehaviour : MonoBehaviour
{
    private Rigidbody2D rb;

    [SerializeField] private float moveSpeed = 8.0f;
    private float timeUntilDestroyed = 5f;

    [SerializeField] private float bulletDamage = 5f;
    private bool hasHit = false;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        Destroy(gameObject, timeUntilDestroyed);
    }

    // Called from an outside script to set the direction of the bullet and fire it
    public void LaunchBullet(Vector2 bulletDirection)
    {
        bulletDirection.Normalize();
        rb.linearVelocity = bulletDirection * moveSpeed;
    }

    private void OnTriggerEnter2D(Collider2D collider)
    {
        if (!hasHit && collider.TryGetComponent(out EnemyInsistence enemyInsistence))
        {
            hasHit = true;
            enemyInsistence.ReduceInsistence(bulletDamage);
            Destroy(gameObject);
        }
    }
}
