using UnityEngine;
using UnityEngine.Pool;

public class FloatingTextManager : MonoBehaviour
{
    [SerializeField] private FloatingText floatingTextPrefab;
    private ObjectPool<FloatingText> floatingTextPool;

    [SerializeField] private float textSpawnOffset; // So the text will spawn above the character

    private void Awake()
    {
        floatingTextPool = new ObjectPool<FloatingText>(CreateNewText, OnTextTaken, OnTextReturned, DestroyText);
    }

    private FloatingText CreateNewText()
    {
        FloatingText text = Instantiate(floatingTextPrefab, gameObject.transform);
        text.SetPool(floatingTextPool);
        return text;
    }
    private void OnTextTaken(FloatingText text)
    {
        text.gameObject.SetActive(true);
    }
    private void OnTextReturned(FloatingText text)
    {
        text.gameObject.SetActive(false);
    }
    private void DestroyText(FloatingText text)
    {
        if (text != null)
        {
            Destroy(text.gameObject);
        }
    }


    public void ShowText(string textToWrite, Vector2 spawnPosition)
    {
        FloatingText floatingText = floatingTextPool.Get();
        floatingText.SetFloatingText(textToWrite);
        floatingText.transform.position = spawnPosition + textSpawnOffset * Vector2.up;
    }

    public void ShowRandomText(string[] lines, Vector2 position)
    {
        if (lines.Length == 0)
        {
            return;
        }

        int index = Random.Range(0, lines.Length);
        string lineChosen = lines[index];
        ShowText(lineChosen, position);
    }
}
