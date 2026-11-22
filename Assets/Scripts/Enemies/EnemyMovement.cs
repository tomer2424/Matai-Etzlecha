using UnityEngine;

public class EnemyMovement : MonoBehaviour
{
    private Rigidbody2D playerRB;
    private Rigidbody2D rb;

    [SerializeField] private EnemyData enemyData;

    private const string playerTag = "Player";
    private float moveSpeed;

    private void Awake()
    { 
        playerRB = GameObject.FindGameObjectWithTag(playerTag).GetComponent<Rigidbody2D>();
        rb = GetComponent<Rigidbody2D>();
        moveSpeed = enemyData.moveSpeed;
    }

    private void FixedUpdate()
    {
        Vector2 direction = (playerRB.position - rb.position);
        direction.Normalize();
        rb.linearVelocity = direction * moveSpeed;
    }

    public void SetDodaPosition(Vector2 spawnPosition)
    {
        rb.position = spawnPosition;
        transform.position = spawnPosition;
    }
}
