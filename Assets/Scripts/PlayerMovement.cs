using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerMovement : MonoBehaviour
{
    
    private Rigidbody2D rb;
    private SpriteRenderer sr;

    [SerializeField] private float moveSpeed = 4.0f;
    private Vector2 movementVector;
    private bool facingRight = false;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        sr = GetComponent<SpriteRenderer>();
    }

    void Update()
    {
        HandleMovement();
        HandleFlip();
    }

    private void FixedUpdate()
    {
        rb.linearVelocity = movementVector * moveSpeed;
    }

    private void HandleMovement() // Handles the movement vector
    {
        movementVector.x = GetHorizontalAxis();
        movementVector.y = GetVerticalAxis();

        if (movementVector.sqrMagnitude > 1.0f)
        {
            movementVector.Normalize();
        }
    }

    private float GetHorizontalAxis() // Gets the desired horizontal axis based on key presses
    {
        bool right = Keyboard.current.dKey.isPressed;
        bool left = Keyboard.current.aKey.isPressed;

        if (left == right)
        {
            return 0f;
        }

        return (right ? 1.0f : -1.0f);
    }

    private float GetVerticalAxis() // Gets the desired vertical axis based on key presses
    {
        bool up = Keyboard.current.wKey.isPressed;
        bool down = Keyboard.current.sKey.isPressed;

        if (up == down)
        {
            return 0f;
        }

        return (up ? 1.0f : -1.0f);
    }

    private void HandleFlip() // Handles when to flip the sprite of the player
    {
        if (movementVector.x > 0 && !facingRight)
        {
            Flip();
        }
        else if (movementVector.x < 0 && facingRight)
        {
            Flip();
        }

    }
    private void Flip() // Flipping the player's sprite
    {
        facingRight = !facingRight;
        sr.flipX = facingRight;
    }
}
