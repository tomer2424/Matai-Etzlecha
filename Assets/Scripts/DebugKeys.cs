using UnityEngine;
using UnityEngine.InputSystem;

public class DebugKeys : MonoBehaviour
{
    [SerializeField] private GameTimer gameTimer;
    [SerializeField] private LevelSystem levelSystem;
    [SerializeField] private PlayerPatience playerPatience;
     
    // update only runs in the unity editor, not the exe file.
#if UNITY_EDITOR
    void Update()
    {
        if (Keyboard.current.f1Key.wasPressedThisFrame)
        {
            gameTimer.DebugSkipTime(60f);
        }
        if (Keyboard.current.f2Key.wasPressedThisFrame)
        {
            levelSystem.DebugSkipLevel();
        }
        if (Keyboard.current.f3Key.wasPressedThisFrame)
        {
            playerPatience.DebugToggleInvincible();
        }
    }
#endif
}
