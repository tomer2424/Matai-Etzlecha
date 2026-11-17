using UnityEngine;
using UnityEngine.Pool;

public class EnemyInsistence : MonoBehaviour
{
    private float insistence;
    [SerializeField] private float maxInsistence = 10f;

    private bool isDead = false;

    private ObjectPool<EnemyMovement> pool;
    private EnemyMovement enemyMovement;
    private NotesSpawner noteSpawner;

    [SerializeField] private string[] hitLines;
    [SerializeField] private string[] giveUpLines;
    [SerializeField, Range(0f, 1f)] private float hitLineChance = 0.15f;
    private FloatingTextManager floatingTextManager;

    private void Awake()
    {
        enemyMovement = GetComponent<EnemyMovement>();
    }

    public void SetPool(ObjectPool<EnemyMovement> pool)
    {
        this.pool = pool;
    }

    public void SetFloatingTextManager(FloatingTextManager floatingTextManager)
    {
        this.floatingTextManager = floatingTextManager;
    }

    public void SetNoteSpawner(NotesSpawner noteSpawner)
    {
        this.noteSpawner = noteSpawner;
    }

    // called from an outside bullet gameobject to reduce the insistence
    public void ReduceInsistence(float insistenceToRemove)
    {
        if (!isDead)
        {
            insistence -= insistenceToRemove;
            if (insistence <= 0)
            {
                GiveUp();
            }
            else
            {
                if (Random.value < hitLineChance)
                {
                    floatingTextManager.ShowRandomText(hitLines, transform.position);
                }
            }
        }
    }

    private void GiveUp()
    {
        floatingTextManager.ShowRandomText(giveUpLines, transform.position);
        noteSpawner.SpawnNote(transform.position);
        isDead = true;
        pool.Release(enemyMovement);
    }

    private void OnEnable()
    {
        isDead = false;
        insistence = maxInsistence;
    }
}
