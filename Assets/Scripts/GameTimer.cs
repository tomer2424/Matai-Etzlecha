using UnityEngine;
using UnityEngine.Events;

// Counts the game time down and announces every new second and the end of the game
public class GameTimer : MonoBehaviour
{
    [SerializeField] private float gameDuration = 300f; // 5 minutes

    private float timeLeft;
    private int lastSecondSent = -1; // -1 so the first second is always sent
    private bool hasEnded = false;

    public UnityEvent<int> OnSecondsLeftChanged;
    public UnityEvent OnTimeUp;

    private void Start()
    {
        timeLeft = gameDuration;
    }

    private void Update()
    {
        if (hasEnded)
        {
            return;
        }

        timeLeft -= Time.deltaTime;

        // Round up so the clock shows 5:00 at the start and 0:00 only at the very end
        int secondsLeft = Mathf.CeilToInt(timeLeft);

        // Send only when the shown second changes, not every frame
        if (secondsLeft != lastSecondSent)
        {
            lastSecondSent = secondsLeft;
            OnSecondsLeftChanged.Invoke(secondsLeft);
        }

        if (timeLeft <= 0)
        {
            hasEnded = true;
            OnTimeUp.Invoke();
        }
    }
}