using UnityEngine;
using UnityEngine.Events;

[System.Serializable]
public class UpgradeOption
{
    [SerializeField] private string title;
    [SerializeField] private string description;
    [SerializeField] private UnityEvent onChosen;
    
    public string Title => title;
    public string Description => description;
    public void Apply()
    {
        onChosen.Invoke();
    }
}
