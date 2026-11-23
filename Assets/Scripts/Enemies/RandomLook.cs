using UnityEngine;

public class RandomLook : MonoBehaviour
{
    private SpriteRenderer sr;

    [SerializeField] private Sprite[] sprites;

    private void Awake()
    {
        sr = GetComponent<SpriteRenderer>();
    }

    private void OnEnable()
    {
        int index = Random.Range(0, sprites.Length);
        sr.sprite = sprites[index];
    }
}
