using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

public class EndScreen : MonoBehaviour
{
    [SerializeField] private GameObject endScreenBackground;
    [SerializeField] private PlayerMovement playerMovement;
    [SerializeField] private TextMeshProUGUI endScreenText;

    private bool isEndScreenShowing = false;


    public void ShowEndScreen(string message)
    {
        if (isEndScreenShowing)
        {
            return;
        }

        isEndScreenShowing = true;
        endScreenText.text = message;
        Time.timeScale = 0;
        endScreenBackground.SetActive(true);
        playerMovement.enabled = false;
    }

    public void OnTryAgainPress()
    {
        Time.timeScale = 1f;
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }
}
