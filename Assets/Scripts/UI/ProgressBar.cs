using UnityEngine;
using UnityEngine.UI;

public class ProgressBar : MonoBehaviour
{
    private Image bar;

    private void Awake()
    {
        bar = GetComponent<Image>();
    }

    public void FillBar(float howFull)
    {
        bar.fillAmount = howFull;
    }
}
