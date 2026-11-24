using UnityEngine;
using UnityEngine.Events;

[System.Serializable]
public class UpgradeOption
{
    [SerializeField] private WeaponBase weapon;

    [SerializeField] private CardType cardType;

    [SerializeField] private string title;
    [SerializeField] private string description;
    [SerializeField] private UnityEvent onChosen;

    private enum CardType
    {
        NewWeapon,
        WeaponUpgrade,
        PassivePlayerUpgrade
    }

    public string Title => title;
    public string Description => description;

    public void Apply()
    {
        onChosen.Invoke();
    }

    public bool IsAvailable()
    {
        if (cardType == CardType.PassivePlayerUpgrade)
        {
            return true;
        }
        else if (cardType == CardType.NewWeapon && !weapon.IsOwned())
        {
            return true;
        }
        else if (cardType == CardType.WeaponUpgrade && weapon.IsOwned() && !weapon.IsMaxLevel())
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}
