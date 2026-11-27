using UnityEngine;

public class CoinMagnet : MonoBehaviour
{
    [SerializeField] private PlayerStats playerStats;
    [SerializeField] private LayerMask whatIsCoin;
    [SerializeField] private float pullSpeed = 8f;

    private void Update()
    {
        HandleMagnet();
    }

    private void HandleMagnet()
    {
        Collider2D[] coins = Physics2D.OverlapCircleAll(transform.position, playerStats.GetPickupRange(), whatIsCoin);

        foreach (Collider2D coin in coins)
        {
            coin.transform.position = Vector3.MoveTowards(coin.transform.position, transform.position, pullSpeed * Time.deltaTime);
        }
    }

    private void OnDrawGizmos()
    {
        Gizmos.DrawWireSphere(transform.position, playerStats.GetPickupRange());
    }
}
