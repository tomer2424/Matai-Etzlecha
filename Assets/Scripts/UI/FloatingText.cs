using UnityEngine;
using TMPro;
using UnityEngine.Pool;

public class FloatingText : MonoBehaviour
{
    private TextMeshPro floatingText;
    [SerializeField] private float maxTimeAlive = 0.75f;
    private float timeLeft;
    [SerializeField] private float textMoveSpeed = 1f;
    private Vector3 textMoveDirection = Vector3.up;

    private ObjectPool<FloatingText> pool;

    private void Awake()
    {
        floatingText = GetComponent<TextMeshPro>();
    }
    
    void Update()
    {
        timeLeft -= Time.deltaTime;
        if (timeLeft > 0)
        {
            floatingText.color = new Color(floatingText.color.r, floatingText.color.g, floatingText.color.b, timeLeft / maxTimeAlive);
            transform.Translate(textMoveDirection * textMoveSpeed * Time.deltaTime);
        }
        else
        {
            pool.Release(this);
        }
    }

    public void SetFloatingText(string text)
    {
        floatingText.text = text;
    }

    public void SetPool(ObjectPool<FloatingText> pool)
    {
        this.pool = pool;
    }

    private void OnEnable()
    {
        floatingText.color = new Color(floatingText.color.r, floatingText.color.g, floatingText.color.b, 1f);
        timeLeft = maxTimeAlive;
    }
}
