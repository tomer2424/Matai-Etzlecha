using UnityEngine;
using UnityEngine.Events;

public class LevelSystem : MonoBehaviour
{
    private int currentLevel = 1;
    private int currentXP = 0;

    public UnityEvent<float> OnXPChanged;
    public UnityEvent OnLevelUp;
    [SerializeField, Min(1)] private int xpRequiredPerLevel = 10;

    public void AddXP(int xpAmount)
    {
        currentXP += xpAmount;

        while (currentXP >= GetXPToLevelUp())
        {
            currentXP -= GetXPToLevelUp();
            LevelUp();
        }

        OnXPChanged.Invoke((float)currentXP / GetXPToLevelUp());
    }

    private void LevelUp()
    {
        currentLevel++;
        Debug.Log("Level UP");
        Debug.Log("Level " +  currentLevel);
        OnLevelUp.Invoke();
    }

    private int GetXPToLevelUp()
    {
        return (xpRequiredPerLevel * currentLevel);
    }

    public void DebugSkipLevel()
    {
        AddXP(GetXPToLevelUp() - currentXP);
    }
}
