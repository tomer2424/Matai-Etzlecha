using UnityEngine;

public class EnemyMovement : MonoBehaviour
{
    private Rigidbody2D playerRB;
    private Rigidbody2D rb;

    private const string playerTag = "Player";
    [SerializeField] private float moveSpeed = 2.5f;

    private void Awake()
    {
        playerRB = GameObject.FindGameObjectWithTag(playerTag).GetComponent<Rigidbody2D>();
        rb = GetComponent<Rigidbody2D>();
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
