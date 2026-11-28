using UnityEngine;
using UnityEngine.Events;

public class PlayerPatience : MonoBehaviour
{
    private float patience;
    [SerializeField] private float maxPatience = 100f;
    [SerializeField] private float maxPatienceIncreasePerLevel = 15f;
    [SerializeField] private float immunityTime = 0.5f;
    private float immunityLeftTimer;
    private bool isDead;
    private bool debugIsInvincible = false;

    private PlayerStats playerStats;

    public UnityEvent<float> onPatienceChanged;
    public UnityEvent onDeath;

    private void Awake()
    {
        playerStats = GetComponent<PlayerStats>();
    }

    private void Update()
    {
        HandleImmunityTimer();
    }

    private void OnCollisionStay2D(Collision2D collision)
    {
        if (collision.gameObject.TryGetComponent(out EnemyDamage enemyDamage))
        {
            ReducePatience(enemyDamage.Damage);
        }
    }

    private void HandleImmunityTimer()
    {
        if (immunityLeftTimer > 0)
        {
            immunityLeftTimer -= Time.deltaTime;
            if (immunityLeftTimer <= 0)
            {
                immunityLeftTimer = 0;
            }
        }
    }

    private void StartImmunity()
    {
        immunityLeftTimer = immunityTime;
    }

    public void ReducePatience(float patienceToRemove)
    {
        if (!debugIsInvincible && !isDead && immunityLeftTimer <= 0)
        {
            StartImmunity();
            patience -= patienceToRemove * playerStats.GetDamageTakenMultiplier();
            onPatienceChanged.Invoke(patience / maxPatience);
            Debug.Log("Patience left: " + patience);
            if (patience <= 0)
            {
                Die();
            }
        }
    }

    private void Die()
    {
        isDead = true;
        onDeath.Invoke();
    }

    public void IncreaseMaxPatience()
    {
        maxPatience += maxPatienceIncreasePerLevel;
        patience += maxPatienceIncreasePerLevel;
        onPatienceChanged.Invoke(patience / maxPatience);
    }

    public void Heal(float amountToHeal)
    {
        patience += Mathf.Min(amountToHeal, maxPatience - patience);
        onPatienceChanged.Invoke(patience / maxPatience);
    }

    public bool IsMaxHealth()
    {
        return (patience >= maxPatience);
    }

    private void OnEnable()
    {
        isDead = false;
        patience = maxPatience;
        immunityLeftTimer = 0;
    }

    public void DebugToggleInvincible()
    {
        debugIsInvincible = !debugIsInvincible;
        Debug.Log("Player invincible: " + debugIsInvincible);
    }
}
