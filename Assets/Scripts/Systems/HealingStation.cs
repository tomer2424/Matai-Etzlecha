using UnityEngine;

public class HealingStation : MonoBehaviour
{
    [SerializeField] private SpriteRenderer healingStationSr;
    [SerializeField] private Sprite[] healingStationSprites;

    private PlayerPatience playerPatience;
    [SerializeField] private float healPerSecond = 5f;
    [SerializeField] private float maxFood = 90f;
    private float currentFood;

    private void Update()
    {
        CheckHeal();
    }

    private void CheckHeal()
    {
        if (playerPatience != null && currentFood > 0 && !playerPatience.IsMaxHealth())
        {
            playerPatience.Heal(healPerSecond * Time.deltaTime);
            currentFood -= healPerSecond * Time.deltaTime;
            CheckFull();
        }
    }

    private void CheckFull()
    {
        if (currentFood >= maxFood / 2)
        {
            healingStationSr.sprite = healingStationSprites[0];
        }
        else if (currentFood > 0)
        {
            healingStationSr.sprite = healingStationSprites[1];
        }
        else
        {
            healingStationSr.sprite = healingStationSprites[2];
        }
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.TryGetComponent(out PlayerPatience playerPatience))
        {
            this.playerPatience = playerPatience;
        }
    }
    private void OnTriggerExit2D(Collider2D collision)
    {
        if (collision.TryGetComponent(out PlayerPatience playerPatience))
        {
            this.playerPatience = null;
        }
    }

    private void OnEnable()
    {
        currentFood = maxFood;
    }
}
