using TMPro;
using UnityEngine;

// Shows the time left as minutes:seconds
public class TimerText : MonoBehaviour
{
    private TextMeshProUGUI timerText;

    private void Awake()
    {
        timerText = GetComponent<TextMeshProUGUI>();
    }

    // Called by GameTimer.OnSecondsLeftChanged
    public void ShowTime(int secondsLeft)
    {
        int minutes = secondsLeft / 60;
        int seconds = secondsLeft % 60;
        timerText.text = minutes + ":" + seconds.ToString("00");
    }
}