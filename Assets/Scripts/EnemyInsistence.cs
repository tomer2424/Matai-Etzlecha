using UnityEngine;

public class EnemyInsistence : MonoBehaviour
{
    [SerializeField] private float insistence = 10f;
    private bool isDead = false;

    public void ReduceInsistence(float insistenceToRemove)
    {
        if (!isDead)
        {
            insistence -= insistenceToRemove;
            Debug.Log("Hit: " + gameObject.name);
            if (insistence <= 0)
            {
                GiveUp();
            }
        }
    }

    private void GiveUp()
    {
        isDead = true;
        Debug.Log("Gave up : " + gameObject.name);
        Destroy(gameObject);
    }
}
