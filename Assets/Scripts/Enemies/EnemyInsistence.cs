using UnityEngine;
using UnityEngine.Pool;

public class EnemyInsistence : MonoBehaviour
{
    [SerializeField] private EnemyData enemyData;

    private float insistence;
    private float maxInsistence;

    private bool isDead = false;

    private ObjectPool<EnemyMovement> pool;
    private EnemyMovement enemyMovement;
    private NotesSpawner noteSpawner;

    private string[] hitLines;
    private string[] giveUpLines;
    private float hitLineChance;
    private FloatingTextManager floatingTextManager;

    private int xpDropped;

    private void Awake()
    {
        enemyMovement = GetComponent<EnemyMovement>();
        maxInsistence = enemyData.maxInsistence;
        hitLines = enemyData.hitLines;
        giveUpLines = enemyData.giveUpLines;
        hitLineChance = enemyData.hitLineChance;
        xpDropped = enemyData.xpDropped;
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

    public void ApplyInsistenceMultiplier(float multiplier)
    {
        insistence = maxInsistence * multiplier;
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
        noteSpawner.SpawnNote(transform.position, xpDropped);
        isDead = true;
        pool.Release(enemyMovement);
    }

    private void OnEnable()
    {
        isDead = false;
        insistence = maxInsistence;
    }
}
